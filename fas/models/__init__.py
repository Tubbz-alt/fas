# -*- coding: utf-8 -*-
#
# Copyright © 2014 Xavier Lamien.
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
__author__ = 'Xavier Lamien <laxathom@fedoraproject.org>'

from flufl.enum import IntEnum
from sqlalchemy.ext.declarative import declarative_base

# import sqlalchemy as sa
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class BaseStatus(IntEnum):
    INACTIVE = 0x00
    ACTIVE = 0x01
    PENDING = 0x03
    LOCKED = 0x05
    DISABLED = 0x08


class AccountStatus(BaseStatus):
    ON_VACATION = 0x04
    LOCKED_BY_ADMIN = 0x06

# Disable dynamic status as of right we don't handle workflow
# mechanism to manage new status adding by end-user.
#
# class AccountStatus(Base):
#    __tablename__ = 'account_status'
#    id = sa.Column(sa.Integer, primary_key=True)
#    status = sa.Column(sa.Unicode(50), unique=True, nullable=False)


class GroupStatus(BaseStatus):
    ARCHIVED = 0x0A


class MembershipStatus(IntEnum):
    UNAPPROVED = 0x00
    APPROVED = 0x01
    PENDING = 0x02


class LicenseAgreementStatus(IntEnum):
    DISABLED = 0x00
    ENABLED = 0x01


class MembershipRole(IntEnum):
    UNKNOWN = 0x00
    USER = 0x01
    EDITOR = 0x02
    SPONSOR = 0x03
    ADMINISTRATOR = 0x04

# Disable dynamic status as of right we don't handle workflow
# mechanism to manage new status adding by end-user.
#
# class RoleLevel(Base):
#    __tablename__ = 'role_level'
#    id = sa.Column(sa.Integer, primary_key=True)
#    name = sa.Column(sa.Unicode(50), unique=True, nullable=False)


class AccountPermissionType(IntEnum):
    """
    Describes the type of permissions a person can request
    or have over its account.
    """
    UNDEFINED = 0x00
    CAN_READ_PUBLIC_INFO = 0x01
    CAN_READ_PEOPLE_PUBLIC_INFO = 0x02
    CAN_READ_PEOPLE_FULL_INFO = 0x03
    CAN_READ_AND_EDIT_PEOPLE_INFO = 0x05
    CAN_EDIT_GROUP_INFO = 0x07
    CAN_EDIT_GROUP_MEMBERSHIP = 0x08
    CAN_READ_SETTINGS = 0x0A
    CAN_READ_AND_EDIT_SETTINGS = 0xAF


class AccountLogType(IntEnum):
    LOGGED_IN = 0x01
    ACCOUNT_UPDATE = 0x03
    REQUESTED_API_KEY = 0x04
    UPDATE_PASSWORD = 0x05
    ASKED_RESET_PASSWORD = 0x06
    RESET_PASSWORD = 0x07
    SIGNED_LICENSE = 0x0A
    REVOKED_GROUP_MEMBERSHIP = 0x0B
    REVOKED_LICENSE = 0x0C
    ASKED_GROUP_MEMBERSHIP = 0x0D
    NEW_GROUP_MEMBERSHIP = 0x0E
    PROMOTED_GROUP_MEMBERSHIP = 0x0F
    DOWNGRADED_GROUP_MEMBERSHIP = 0x10
    REMOVED_GROUP_MEMBERSHIP = 0x11
    REVOKED_GROUP_MEMBERSHIP_BY_ADMIN = 0x12
    CHANGED_GROUP_MAIN_ADMIN = 0x13
