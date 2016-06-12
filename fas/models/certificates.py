# -*- coding: utf-8 -*-
#
# Copyright © 2015 Xavier Lamien.
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
# __author__ = 'Xavier Lamien <laxathom@fedoraproject.org>'

from . import Base

from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    UnicodeText,
    DateTime,
    Boolean,
    ForeignKey,
    Index,
    func,
    )

from sqlalchemy.orm import relation
from fas.util import utc_iso_format


class Certificates(Base):

    __tablename__ = 'certificates'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255), nullable=False)
    description = Column(UnicodeText, nullable=True)
    cert = Column(UnicodeText(), nullable=False)
    cert_key = Column(UnicodeText(), nullable=False)
    client_cert_desc = Column(UnicodeText(), nullable=False)
    enabled = Column(Boolean(), default=False)
    creation_timestamp = Column(
        DateTime,
        nullable=False,
        default=func.current_timestamp()
    )

    __table_args__ = (
        Index('certificates_idx', id),
    )

    def to_json(self):
        """
        Exports certificate to JSON/dict format.

        :return: A dictionary of AccountPermissions's data
        :rtype: dict
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'enabled': self.enabled,
            'creation_timestamp': utc_iso_format(self.creation_timestamp)
        }


class PeopleCertificates(Base):

    __tablename__ = 'people_certificates'
    id = Column(Integer, primary_key=True)
    ca = Column(Integer, ForeignKey('certificates.id'))
    person_id = Column(Integer, ForeignKey('people.id'))
    serial = Column(Integer, default=1)
    certificate = Column(UnicodeText, nullable=True)

    cacert = relation(
        'Certificates',
        foreign_keys='Certificates.id',
        primaryjoin='and_(PeopleCertificates.ca==Certificates.id)',
        uselist=False
        )

    person = relation(
        'People',
        foreign_keys='People.id',
        primaryjoin='and_(PeopleCertificates.person_id==People.id)',
        uselist=False
        )

