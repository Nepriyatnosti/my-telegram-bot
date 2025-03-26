from venv import logger
from datetime import datetime
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📝 Анализ текста", callback_data="analyze"),
                InlineKeyboardButton(text="📜 История", callback_data="history")
            ],
            [InlineKeyboardButton(text="ℹ️ Помощь", callback_data="help")]
        ]
    )




def history_pagination(entries, page: int, per_page: int = 5):
    try:
        # Получаем общее количество записей
        total = entries.count()
        total_pages = max(1, (total + per_page - 1) // per_page)
        current_page = min(max(page, 1), total_pages)

        # Создаем кнопки пагинации
        pagination_buttons = []
        if page > 1:
            pagination_buttons.append(
                InlineKeyboardButton(
                    text="◀️",
                    callback_data=f"history_page_{page - 1}"
                )
            )

        pagination_buttons.append(
            InlineKeyboardButton(
                text=f"{page}/{total_pages}",
                callback_data="current_page"
            )
        )

        if page < total_pages:
            pagination_buttons.append(
                InlineKeyboardButton(
                    text="▶️",
                    callback_data=f"history_page_{page + 1}"
                )
            )

        # Создаем кнопки записей
        entry_buttons = [
            [InlineKeyboardButton(
                text=f"{(entry.timestamp.strftime('%d.%m %H:%M') if isinstance(entry.timestamp, datetime) else entry.timestamp)} - {entry.command[:10]}...",
                callback_data=f"history_detail_{entry.id}"
            )]
            for entry in entries.paginate(page, per_page)
        ]

        return InlineKeyboardMarkup(
            inline_keyboard=entry_buttons + [pagination_buttons] + [
                [InlineKeyboardButton(
                    text="🔙 В меню",
                    callback_data="back_to_menu"
                )]
            ]
        )

    except Exception as e:
        logger.error(f"Keyboard error: {e}")
        return InlineKeyboardMarkup(inline_keyboard=[])