from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
# from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from lexicon.russian import COMMANDS_LEXICON


async def start_command(message: Message) -> None:
    """Handler for /start menu command."""
    await message.answer(text=COMMANDS_LEXICON['/start'])


async def help_command(message: Message) -> None:
    """Handler for /help menu command."""
    await message.answer(text=COMMANDS_LEXICON['/help'])


async def cancel_command(message: Message, state: FSMContext) -> None:
    """Handler for /cancel menu command."""
    await state.reset_state()


def register_menu_handlers(dp: Dispatcher) -> None:
    """Register menu handlers."""
    dp.register_message_handler(start_command, commands='start')
    dp.register_message_handler(help_command, commands='help')
    dp.register_message_handler(cancel_command, commands='cancel', state='*')
