from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import select

from bot.database import AsyncSessionLocal
from bot.models import Exchanger
from bot.mongo.mongo import get_sites


async def main_menu():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Список обменников"),
                KeyboardButton(text="Список мониторингов"),
            ],
            [
                KeyboardButton(text="Показать список обменников"),  # третья кнопка
            ],
        ],
        resize_keyboard=True,
    )
    return kb


async def show_exchange_card(msg: Message, exc_id: int) -> None:
    async with AsyncSessionLocal() as session:
        stmt = select(Exchanger).where(Exchanger.id == exc_id)
        result = await session.execute(stmt)
        exc = result.scalar_one_or_none()

        if exc is None:
            return

        text = f"📊 <b>{exc.name}</b>\n"
        text += f"   Автоматизирован: {'✅' if exc.automated_bot else '❌'}\n"
        text += f"   Делаем заявки: {'✅' if exc.making_orders else '❌'}\n"
        text += f"   RU план: {exc.plan_best_ru} | ENG: {exc.plan_best_eng}\n"
        text += f"   Описание: {exc.description}\n\n"
        links = await get_sites(exc.name)
        if links:
            text += "🔗 <b>Ссылки:</b>\n"
            for site_name, url in links.items():
                text += f"   • <b>{site_name}</b>: <code>{url}</code>\n"
        else:
            text += "🔗 <b>Ссылки:</b> нет\n"

        text += "\n"

        kb = InlineKeyboardBuilder().add(
            InlineKeyboardButton(text="🔗 Добавить ссылку", callback_data=f"add_links_exchange:{exc.name}"),
            InlineKeyboardButton(text="⬅️ Назад", callback_data="back_inline_exchange"),
        ).adjust(1)

        await msg.answer(text, parse_mode="HTML", reply_markup=kb.as_markup())


async def get_exchangers_list_kb() -> tuple[str, InlineKeyboardBuilder]:
    async with AsyncSessionLocal() as session:
        stmt = select(Exchanger)
        result = await session.execute(stmt)
        exchangers = result.scalars().all()

    text = "📊 <b>Список обменников:</b>"
    kb = InlineKeyboardBuilder()

    if not exchangers:
        return text + "\nОбменники не найдены", kb

    for exc in exchangers:
        kb.add(InlineKeyboardButton(text=exc.name, callback_data=f"exchanger:{exc.id}"))
    kb.adjust(2)

    return text, kb


