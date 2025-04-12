import asyncio
from loguru import logger

from domain.user.bl_models.db_bl import UserBL
from utils.data_state import DataSuccess, DataFailedMessage  # Импортируем необходимые классы

async def hourly_request_to_1c():
    while True:
        try:

            data_state = await UserBL.update_employee_data()

            if isinstance(data_state, DataSuccess):
                logger.info(f"Данные о сотрудниках успешно синхронизированы с базой 1С")

            elif isinstance(data_state, DataFailedMessage):
                logger.error(f"Ошибка при обновлении данных сотрудников: {data_state.error_message}")

            else:
                logger.warning("Неизвестный тип состояния данных при обновлении сотрудников")

        except Exception as e:
            logger.error(f"Ошибка при обновлении данных сотрудников: {e}")

        await asyncio.sleep(3600)
