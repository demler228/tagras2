from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from loguru import logger
from application.tg_bot.redefining_roles.super_admin_actions.keyboards.super_admins_keyboards import \
    get_role_management_keyboard, back_to_admin_actions
from domain.redefining_users.db_bl import RedefinigDbBl
from utils.data_state import DataSuccess
from utils.logs import admin_logger
from .keyboards.callback_factory import BackToAdminActions, BackToUsersList, MakeRemoveAdminAction

router = Router()


class RedefineUserStates(StatesGroup):
    WAITING_FOR_USER_NUMBER = State()


class SelectedUser(StatesGroup):
    selected_user = State()


def selected_user_info_text(selected_user):
    user_info_text = (f"<b>Информация о пользователе:</b>\n\n"
                      f'<b>ID:</b> {selected_user.id}\n\n'
                      f'<b>Имя:</b> {selected_user.username}\n\n'
                      f'<b>Номер:</b> {selected_user.phone}\n\n'
                      f'<b>Телеграм ID:</b> {selected_user.telegram_id}\n\n'
                      f'<b>Роль:</b> {selected_user.role}\n\n'
                      f'<b>Ссылка на тг:</b> https://t.me/{selected_user.tg_username}')
    return user_info_text


@router.callback_query(BackToUsersList.filter())
@router.callback_query(F.data == "redefining_roles_super_admin")
async def redefining_roles_handler(callback_query: types.CallbackQuery, state: FSMContext):
    data_state = RedefinigDbBl.get_all_users()
    logger.info(f"redefining_roles_handler is handled")
    users_list = f"Список пользаветелей:\n\n"

    if isinstance(data_state, DataSuccess) and data_state.data:
        users = data_state.data
        previous_role = None
        for idx, user in enumerate(users, start=1):

            if previous_role == "user" and user.role == "admin":
                users_list += "-" * 30 + "\n"

            users_list += f"{idx}. {user.username} - [{user.role}]\n"

            previous_role = user.role

        await callback_query.message.edit_text(
            text=f"{users_list}\nВведите порядковый номер пользователя для детальной информации.",
            reply_markup=back_to_admin_actions()
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

    if 1 <= user_number <= len(users):
        selected_user = users[user_number - 1]
        # Отправляем информацию о выбранном пользователе
        await state.update_data(selected_user=selected_user)
        await message.answer(
            text=selected_user_info_text(selected_user),
            parse_mode="HTML",
            reply_markup=get_role_management_keyboard(selected_user.id, selected_user.role)

        )

        # Сбрасываем состояние после завершения обработки
        await state.clear()
    else:
        await message.answer("Пожалуйста, введите существующий порядковый номер из списка.")


@router.callback_query(MakeRemoveAdminAction.filter())
async def make_admin_callback_handler(callback_query: types.CallbackQuery, callback_data: MakeRemoveAdminAction):
    try:
        action = callback_data.action
        user_id = callback_data.user_id
        
        if action == "make_admin":
            result = RedefinigDbBl.change_user_role(user_id, "admin")
        else:
            result = RedefinigDbBl.change_user_role(user_id, "user")

        if isinstance(result, DataSuccess):
            role_change_description = (
                "сделал админом пользователя" if action == "make_admin" else "забрал роль админа у пользователя"
            )
            admin_logger.info(
                f"Супер-админ {callback_query.message.chat.full_name} ({callback_query.message.chat.id}) {role_change_description} - {user_id}"
            )
            await callback_query.answer(text="Смена роли произошла успешно", show_alert=True)
            await callback_query.message.edit_text(
                text=selected_user_info_text(result.data),
                parse_mode="HTML",
                reply_markup=get_role_management_keyboard(result.data.id, result.data.role)
            )
        else:
            await callback_query.answer(f"Ошибка: {result.message}", show_alert=True)
    except Exception as e:
        logger.error(e)
        await callback_query.answer("Произошла ошибка при назначении администратора.", show_alert=True)
