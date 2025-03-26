from aiogram import Router, types
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from bot.services.text_analysis import analyze_text
from bot.models.user import History, User
from datetime import datetime

# Создаем роутер
router = Router()


class AnalysisStates(StatesGroup):
    waiting_for_text = State()


# Обработчик кнопки "Анализ текста"
@router.callback_query(Text("analyze"))
async def start_analysis(callback: types.CallbackQuery, state: FSMContext):  # Добавляем state
    await callback.message.edit_text("✍️ Введите текст для анализа:")
    await state.set_state(AnalysisStates.waiting_for_text)  # Правильный метод
    await callback.answer()


# Обработчик текста
@router.message(AnalysisStates.waiting_for_text)
async def process_text(message: types.Message, state: FSMContext):
    text = message.text

    user, created = User.get_or_create(
        user_id=str(message.from_user.id),
        defaults={'username': message.from_user.username}
    )

    analysis_result = await analyze_text(text)

    History.create(
        user=user,
        command="text_analysis",
        result=analysis_result,
        timestamp=datetime.now()  # Явное использование текущего времени
    )



    await message.answer(f"📊 Результат анализа:\n{analysis_result}")
    await state.clear()

    # Возвращаем главное меню
    from bot.keyboards.inline import main_menu  # Импортируем здесь, чтобы избежать циклических зависимостей
    await message.answer(
        "Выберите действие:",
        reply_markup=main_menu()
    )