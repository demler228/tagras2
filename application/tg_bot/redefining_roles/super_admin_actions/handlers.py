from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from loguru import logger
from application.tg_bot.redefining_roles.super_admin_actions.keyboards.super_admins_keyboards import \
    get_role_management_keyboard
from domain.redefining_users.db_bl import RedefinigDbBl
from utils.data_state import DataSuccess
from .keyboards.callback_factory import BackToAdminActions, BackToUsersList

router = Router()

class RedefineUserStates(StatesGroup):
    WAITING_FOR_USER_NUMBER = State()

@router.callback_query(BackToUsersList.filter())
@router.callback_query(F.data == "redefining_roles_super_admin")
async def redefining_roles_handler(callback_query: types.CallbackQuery, state: FSMContext):
    data_state = RedefinigDbBl.get_all_users()
    logger.info(f"redefining_roles_handler is handled")
    users_list = f"Список пользаветелей:\n\n"

    if isinstance(data_state, DataSuccess) and data_state.data:
        users = data_state.data
        for idx, user in enumerate(users, start=1):
            users_list += f"{idx}. {user.username} - [{user.role}]\n"

        await callback_query.message.edit_text(
            text=f"{users_list}\n\nВведите порядковый номер пользователя для детальной информации."
        )

        # Устанавливаем состояние ожидания ввода номера пользователя
        await state.set_state(RedefineUserStates.WAITING_FOR_USER_NUMBER)
        await state.update_data(users=users)
    else:
        await callback_query.message.answer("Пользователи не найдены")



@router.message(RedefineUserStates.WAITING_FOR_USER_NUMBER)
async def process_user_number(message: types.Message, state: FSMContext):
    try:
        user_number = int(message.text)
    except ValueError:
        await message.answer("Пожалуйста, введите корректный числовой порядковый номер.")
        return
    logger.info("process_user_number is handled")

    # Получаем список пользователей из состояния
    data = await state.get_data()
    users = data.get("users", [])
    logger.info(f"Users: {users}")

    if 1 <= user_number <= len(users):
        selected_user = users[user_number - 1]
        # Отправляем информацию о выбранном пользователе
        await message.answer(
            text=f"<b>Информация о пользователе:</b>\n"
                 f"<b>ID:</b> {selected_user.id}\n"
                 f"<b>Имя:</b> {selected_user.username}\n"
                 f"<b>Роль:</b> {selected_user.role}"
                 f"<b>Тг имя:</b> {selected_user.tg_username}",
            parse_mode="HTML",
            reply_markup=get_role_management_keyboard(selected_user.id, selected_user.role)

        )

        # Сбрасываем состояние после завершения обработки
        await state.clear()
    else:
        await message.answer("Пожалуйста, введите существующий порядковый номер из списка.")


@router.callback_query(F.data.startswith("make_admin:"))
async def make_admin_callback_handler(callback_query: types.CallbackQuery):
    try:
        user_id = int(callback_query.data.split(":")[-1])  # Извлекаем ID пользователя из callback_data
        result = RedefinigDbBl.change_user_role(user_id, "admin")

        if isinstance(result, DataSuccess):
            await callback_query.message.answer(f"{result.data}")
        else:
            await callback_query.message.answer(f"Ошибка: {result.message}")
    except Exception as e:
        logger.error(e)
        await callback_query.message.answer("Произошла ошибка при назначении администратора.")


@router.callback_query(F.data.startswith("remove_admin:"))
async def remove_admin_callback_handler(callback_query: types.CallbackQuery):
    try:
        user_id = int(callback_query.data.split(":")[-1])  # Извлекаем ID пользователя из callback_data
        result = RedefinigDbBl.change_user_role(user_id, "user")

        if isinstance(result, DataSuccess):
            await callback_query.message.answer(f"{result.data}")
        else:
            await callback_query.message.answer(f"Ошибка: {result.message}")
    except Exception as e:
        logger.error(e)
        await callback_query.message.answer("Произошла ошибка при снятии привилегий администратора.")


@router.callback_query(F.data == "cancel_action")
async def cancel_action_callback_handler(callback_query: types.CallbackQuery):
    await callback_query.message.answer("Действие отменено.")
