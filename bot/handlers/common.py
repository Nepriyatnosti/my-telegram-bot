from aiogram import Router, types
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.keyboards.inline import main_menu

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "📊 Аналитический бот приветствует вас!",
        reply_markup=main_menu()
    )


@router.callback_query(Text("help"))
async def show_help(callback: types.CallbackQuery):
    help_text = (
        "ℹ️ *Помощь*\n\n"
        "📝 Анализ текста: определяет эмоции и бизнес-характеристики\n"
        "📜 История: показывает ваши последние запросы\n"
        "🔄 Нажмите /start для перезагрузки бота"
    )

    await callback.message.edit_text(
        help_text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    text="🔙 В меню",
                    callback_data="menu"
                )]
            ]
        )
    )
    await callback.answer()

@router.callback_query(Text("menu"))
async def back_to_menu(
    callback: types.CallbackQuery,
    state: FSMContext  # Добавляем автоматическое получение состояния
):
    await state.clear()
    await callback.message.edit_text(
        "Главное меню:",
        reply_markup=main_menu()
    )
    await callback.answer()
