from aiogram.fsm.state import StatesGroup, State


class AddLink(StatesGroup):
    waiting_for_site_name = State()
    waiting_for_url = State()