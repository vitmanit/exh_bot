from bot.config import settings

def root_users(tg_id):
    admins = config.admins.get_secret_value()
    return str(tg_id) in admins