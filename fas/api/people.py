# -*- coding: utf-8 -*-
#
# Copyright © 2014-2015 Xavier Lamien.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
__author__ = ['Xavier Lamien <laxathom@fedoraproject.org>',
              'Pierre-Yves Chibon <pingou@fedoraproject.org>']

from pyramid.view import view_config

from fas.api import (
    BadRequest,
    NotFound,
    MetaData,
    RequestStatus)
from fas import log
from fas.events import ApiRequest
import fas.models.provider as provider
from fas.forms.people import EditPeopleForm
from fas.security import ParamsValidator


class PeopleAPI(object):

    def __init__(self, request):
        self.request = request
        self.notify = self.request.registry.notify
        # self.params = ParamsValidator(self.request, True)
        self.params = self.request.param_validator
        self.data = MetaData('People')
        self.perm = None

        self.request.param_validator.add_optional('limit')
        self.request.param_validator.add_optional('page')
        self.request.param_validator.add_optional('status')

        self.notify(ApiRequest(self.request, self.data, self.perm))
        self.apikey = self.request.token_validator

    def __get_user__(self, key, value):
        if key not in ['id', 'username', 'email', 'ircnick']:
            raise BadRequest("Invalid key: '%s'" % key)

        method = getattr(provider, 'get_people_by_%s' % key)
        log.debug('Looking for user %s', value)
        user = method(value)

        if not user:
            raise NotFound('No such user: %r' % value)

        return user

    @view_config(
        route_name='api-people-list', renderer='json', request_method='GET')
    def get_people(self):
        """ Returns a JSON's output of people's list. """
        limit = self.params.get_limit()
        page = self.params.get_pagenumber()
        status = self.params.get_value_from_optional('status')

        if self.apikey.validate():
            people = provider.get_people(
                limit=limit,
                page=page,
                status=status
                )

        if people:
            users = []
            for user in people:
                log.debug('Processing account %s' % user.username)
                users.append(user.to_json(self.apikey.get_perm()))

            self.data.set_pages(provider.get_people(count=True), page, limit)
            self.data.set_data(users)

        return self.data.get_metadata()

    @view_config(
        route_name='api-people-get', renderer='json', request_method='GET')
    def get_person(self):
        user = None

        if self.apikey.validate():
            key = self.request.matchdict.get('key')
            value = self.request.matchdict.get('value')

            try:
                user = self.__get_user__(key, value)
                self.data.set_data(user.to_json(self.apikey.get_perm()))
            except BadRequest as err:
                log.debug('Having a bad request here!')
                self.request.response.status = '400 bad request'
                self.data.set_status(RequestStatus.FAILED.value)
                self.data.set_error_msg('Bad request', err.message)
            except NotFound as err:
                log.debug('Having a not found keyword here!')
                self.request.response.status = '404 page not found'
                self.data.set_status(RequestStatus.FAILED.value)
                self.data.set_error_msg('Item not found', err.message)

        return self.data.get_metadata()

    @view_config(
        route_name='api-people-get', renderer='json', request_method='POST')
    def edit_person(self):
        key = self.request.matchdict.get('key')
        value = self.request.matchdict.get('value')

        if self.apikey.validate():
            try:
                user = self.__get_user__(key, value)
            except BadRequest as err:
                self.request.response.status = '400 bad request'
                self.data.set_error_msg('Bad request', err.message)
            except NotFound as err:
                self.request.response.status = '404 page not found'
                self.data.set_error_msg('Item not found', err.message)

            form = EditPeopleForm(self.request.POST)

            if form.validate():
                # Handle the latitude longitude that needs to be number or None
                form.latitude.data = form.latitude.data or None
                form.longitude.data = form.longitude.data or None

                form.populate_obj(user)
                self.data.set_status('stored', 'User updated')
                self.data.set_data(user.to_json(self.apikey.get_perm()))
            else:
                self.request.response.status = '400 bad request'
                self.data.set_error_msg('Invalid request', form.errors)

        return self.data.get_metadata()
