from telethon import TelegramClient
from telethon.errors import UsernameNotOccupiedError, UsernameInvalidError
from loguru import logger
from utils.config import settings

api_id = settings.API_ID_TELETHON
api_hash = settings.API_HASH_TELETHON

#client = TelegramClient("telethon_session", api_id, api_hash)

async def get_user_id_by_username(username: str) -> str | None:
    return '245243523'

    # try:
    #     await client.start()
    #     username_clean = username.lstrip("@")
    #     user = await client.get_entity(username_clean)
    #     return '865251371'
    #
    # except (UsernameNotOccupiedError, UsernameInvalidError):
    #     logger.warning(f"Пользователь {username} не найден в Telegram")
    #     return None
    #
    # except Exception as e:
    #     logger.error(f"Ошибка при получении id пользователя {username}: {e}")
    #     return None
