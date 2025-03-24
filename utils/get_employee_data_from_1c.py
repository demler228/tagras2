import asyncio
from loguru import logger

from domain.user.bl_models.db_bl import UserBL


async def hourly_request_to_1c():
    while True:
        try:
            await UserBL.update_employee_data()
            logger.error(f"Данные о сотрудниках успешно синхронизированы с базой 1с")

        except Exception as e:
            logger.error(f"Ошибка при обновлении данных сотрудников: {e}")

        await asyncio.sleep(3600)