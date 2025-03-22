from application.tg_bot.user.entities.user import User


class UserMember(User):
    is_member: bool
