from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.orm import selectinload
from bot.mongo.mongo import *
from bot.keyboards import main_menu, show_exchange_card, get_exchangers_list_kb
from sqlalchemy import select
from bot.database.db import AsyncSessionLocal
from bot.models.models import Exchanger
from bot.states import AddLink


router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Привет! Какие данные хочешь получить?", reply_markup=await main_menu())


@router.message(F.text == 'Список обменников')
async def exchange_list(message: Message):
    # if not root_users(message.from_user.id):
    #     await message.answer(text='Доступно только Администрации')
    #     return

    async with AsyncSessionLocal() as session:
        stmt = select(Exchanger).options(selectinload(Exchanger.which_exchangers))
        result = await session.execute(stmt)
        exchangers = result.scalars().all()

        if not exchangers:
            await message.answer("Обменники не найдены")
            return

        text = "📊 <b>Список обменников:</b>\n\n"
        for exc in exchangers:
            text += f"<b>{exc.name}</b> 🟢\n"
            text += f"   Автоматизирован: {'✅' if exc.automated_bot else '❌'}\n"
            text += f"   Делаем заявки: {'✅' if exc.making_orders else '❌'}\n"
            text += f"   RU план: {exc.plan_best_ru} | ENG: {exc.plan_best_eng}\n"

            links = await get_sites(exc.name)
            if links:
                text += "🔗 <b>Ссылки:</b>\n"
                for site_name, url in links.items():
                    text += f"   • <b>{site_name}</b>: <code>{url}</code>\n"
            else:
                text += "🔗 <b>Ссылки:</b> нет\n"

            text += "\n"

        await message.answer(text, parse_mode="HTML")

@router.message(F.text == 'Список мониторингов')
async def monitoring_list(message: Message):
    # if not root_users(message.from_user.id):
    #     await message.answer(text='Доступно только Администрации')
    #     return

    async with AsyncSessionLocal() as session:
        stmt = select(Exchanger).options(selectinload(Exchanger.which_exchangers))
        result = await session.execute(stmt)
        exchangers = result.scalars().all()

        text = "💱 <b>Обменники и мониторинги</b>:\n\n"
        for exc in exchangers:
            text += f"<b>{exc.name}</b>\n"
            if exc.which_exchangers:
                for mon in exc.which_exchangers:
                    status = "✅" if mon.can_do else "❌"
                    text += f"  • <code>{mon.link}</code> {status}\n"
            else:
                text += "  Мониторинги: нет\n"
            text += "\n"

        await message.answer(text, parse_mode="HTML")


@router.message(F.text == 'Показать список обменников')
async def cmd_list_exc(message: Message):
    text, kb = await get_exchangers_list_kb()
    await message.answer(text, parse_mode="HTML", reply_markup=kb.as_markup())

@router.callback_query(F.data == "back_inline_exchange")
async def back_inline_exchange(callback: CallbackQuery):
    text, kb = await get_exchangers_list_kb()
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=kb.as_markup())
    await callback.answer()

@router.callback_query(F.data.startswith("exchanger:"))
async def exchanger_selected(callback: CallbackQuery):
    exc_id = int(callback.data.split(":")[1])
    await show_exchange_card(callback.message, exc_id)
    await callback.answer()


@router.callback_query(F.data.startswith("add_links_exchange:"))
async def add_links_exchange(callback: CallbackQuery, state: FSMContext):
    exchange_name = callback.data.split(":", 1)[1]
    await state.update_data(exchange_name=exchange_name)

    await callback.message.answer(
        f"Отправь <b>название сайта</b> для <b>{exchange_name}</b>\n"
        f"Пример: 'google-docs', 'vk.com', 'twitter'",
        parse_mode="HTML",
    )
    await state.set_state(AddLink.waiting_for_site_name)  # 1-й шаг
    await callback.answer()


@router.message(AddLink.waiting_for_site_name)
async def process_site_name(message: Message, state: FSMContext):
    await state.update_data(site_name=message.text.strip())  # сохраняем название

    await message.answer(
        "Теперь отправь <b>ссылку</b> на этот сайт",
        parse_mode="HTML",
    )
    await state.set_state(AddLink.waiting_for_url)

@router.callback_query(F.data == "back_inline_exchange")
async def back_inline_exchange(callback: CallbackQuery):
    async with AsyncSessionLocal() as session:
        stmt = select(Exchanger)
        result = await session.execute(stmt)
        exchangers = result.scalars().all()

    if not exchangers:
        await callback.message.edit_text("Обменники не найдены")
        await callback.answer()
        return

    kb = InlineKeyboardBuilder()
    for exc in exchangers:
        kb.add(
            InlineKeyboardButton(
                text=exc.name,
                callback_data=f"exchanger:{exc.id}",
            )
        )
    kb.adjust(2)

    await callback.message.edit_text("📊 <b>Список обменников:</b>",
                                     parse_mode="HTML",
                                     reply_markup=kb.as_markup())
    await callback.answer()



@router.message(AddLink.waiting_for_url)
async def process_url(message: Message, state: FSMContext):
    data = await state.get_data()
    exchange_name = data["exchange_name"]
    site_name = data["site_name"]
    url = message.text.strip()

    await add_site(exchange_name, site_name, url)

    await message.answer(
        f"✅ Ссылка <b>{site_name}</b> добавлена для <b>{exchange_name}</b>",
        parse_mode="HTML",
    )

    async with AsyncSessionLocal() as session:
        stmt = select(Exchanger).where(Exchanger.name == exchange_name)
        result = await session.execute(stmt)
        exc = result.scalar_one_or_none()
    if exc:
        await show_exchange_card(message, exc.id)
    await state.clear()
