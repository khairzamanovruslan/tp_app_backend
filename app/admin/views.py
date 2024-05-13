from sqladmin import ModelView
from app.substation.models import Substation
from app.users.models import Users
from app.users_tg.models import UsersTG


class UsersAdmin(ModelView, model=Users):
    name_plural = "Users App"
    name = 'User App'
    column_list = [c.name for c in Users.__table__.c if c.name !=
                   'hashed_password' and c.name != 'id']
    column_searchable_list = [Users.email]
    column_details_exclude_list = [Users.hashed_password]
    can_edit = False
    can_delete = False
    page_size = 50


class UsersTGAdmin(ModelView, model=UsersTG):
    name_plural = "Users Telegram Bot"
    name = 'User Telegram Bot'
    column_list = [c.name for c in UsersTG.__table__.c if c.name != 'id']
    column_searchable_list = [UsersTG.full_name]
    column_sortable_list = [UsersTG.full_name]
    save_as = False
    page_size = 50


class SubstationAdmin(ModelView, model=Substation):
    name_plural = "Substations"
    name = 'Substation'
    column_list = [c.name for c in Substation.__table__.c if c.name != 'id']
    column_searchable_list = [Substation.name]
    column_sortable_list = [Substation.name]
    page_size = 150
