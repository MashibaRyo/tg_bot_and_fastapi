﻿from crud import BaseDAO
from users.models import Users


class UsersDAO(BaseDAO):
    model = Users

