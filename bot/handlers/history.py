from datetime import datetime
from venv import logger
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext  # Правильный импорт
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.models.user import History, User
from bot.keyboards.inline import history_pagination, main_menu
from aiogram.filters import Text

router = Router()


@router.callback_query(Text(startswith="history_page_"))
async def handle_history_pagination(callback: types.CallbackQuery):
    page = int(callback.data.split("_")[-1])
    user = User.get_or_none(user_id=str(callback.from_user.id))
    entries = user.history.order_by(History.timestamp.desc())

    await callback.message.edit_reply_markup(
        reply_markup=history_pagination(entries, page)
    )
    await callback.answer()


@router.callback_query(Text("history"))
async def show_history(callback: types.CallbackQuery):
    try:
        user, created = User.get_or_create(
            user_id=str(callback.from_user.id),
            defaults={'username': callback.from_user.username}
        )

        entries = (History
                   .select()
                   .where(History.user == user)
                   .order_by(History.timestamp.desc()))

        if not entries:
            await callback.answer("📭 История пуста!")
            return

        await callback.message.edit_text(
            "📜 История запросов:",
            reply_markup=history_pagination(entries, page=1)
        )
        await callback.answer()

    except Exception as e:
        logger.exception("History error:")  # Детальный лог
        await callback.answer("⚠️ Ошибка загрузки истории")


@router.callback_query(Text(startswith="history_detail_"))
async def show_history_detail(callback: types.CallbackQuery):
    try:
        entry_id = int(callback.data.split("_")[-1])
        entry = History.get_by_id(entry_id)

        # Преобразование timestamp
        timestamp_str = entry.timestamp.strftime("%d.%m.%Y %H:%M") if isinstance(entry.timestamp, datetime) else str(
            entry.timestamp)

        response = (
            f"📅 *Дата:* `{timestamp_str}`\n"
            f"🔍 *Команда:* `{entry.command}`\n"
            f"📝 *Результат:*\n```\n{entry.result}\n```"
        )

        await callback.message.answer(
            response,
            parse_mode="MarkdownV2",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text="🔙 Назад к истории",
                        callback_data=f"history_page_1"
                    )]
                ]
            )
        )
        await callback.answer()

    except History.DoesNotExist:
        await callback.answer("🚫 Запись не найдена")
    except Exception as e:
        logger.error(f"Ошибка деталей: {repr(e)}")
        await callback.answer("⚠️ Ошибка загрузки записи")


@router.callback_query(Text("back_to_menu"))
async def handle_back_to_menu(
    callback: types.CallbackQuery,
    state: FSMContext
):
    await state.clear()
    await callback.message.edit_text(
        "Главное меню:",
        reply_markup=main_menu()
    )
    await callback.answer()

@router.callback_query(Text("clear_history"))
async def clear_history(callback: types.CallbackQuery):
    user = User.get(user_id=str(callback.from_user.id))
    History.delete().where(History.user == user).execute()
    await callback.answer("🗑️ История очищена!")
    await show_history(callback)  # Показываем обновленный пустой список

