import logging
import random

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from keyboards.user_keyboards import spelling_start_keyboard
from lexicon.russian import SPELLING_LEXICON
from services.api import backend_api

# from typing import Any, Dict


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Spelling(StatesGroup):
    intro = State()
    in_progress = State()
    show_result = State()


async def spelling_intro(callback: CallbackQuery, state: FSMContext,
                         task: dict) -> None:
    """Spelling entry point from tasks handlers."""
    await state.update_data(user_tg_id=callback.from_user.id,
                            exercise_id=task['id'],
                            questions=task['data'], correct=0, incorrect=0,
                            left=len(task['data']), mistakes="")
    await state.set_state(Spelling.intro)
    await callback.message.edit_text(
        text=(f'{SPELLING_LEXICON["title"]}'
              f'{SPELLING_LEXICON["topic"]}{task["topic"].lower()}\n'
              f'{SPELLING_LEXICON["total_questions"]}{len(task["data"])}\n\n'
              f'{SPELLING_LEXICON["rules"]}'),
        reply_markup=spelling_start_keyboard()
    )


async def start_spelling(callback: CallbackQuery, state: FSMContext) -> None:
    """Start spelling handler."""
    await state.set_state(Spelling.in_progress)
    await callback.message.delete_reply_markup()
    await send_question(callback.message, state)


async def exit_spelling(callback: CallbackQuery, state: FSMContext) -> None:
    """Start spelling handler."""
    await state.reset_state()
    await callback.message.delete()


async def send_question(message: Message, state: FSMContext) -> None:
    """Helper function to send question."""
    data = await state.get_data()
    if data['left'] == 0:
        await state.reset_state()
        await show_result(message, data)
        return
    # Use negative index to get questions from the list
    question = data['questions'][- data['left']]
    await state.update_data(left=data['left'] - 1,
                            spelling=question['spelling'],
                            word=question['word'])
    await message.answer(
        text=f'{question["word"]}')


async def check_spelling(message: Message, state: FSMContext) -> None:
    """Check spelling handler."""
    data = await state.get_data()
    if message.text.lower() == data['spelling'].lower():
        await state.update_data(correct=data['correct'] + 1)
        await message.answer(
            text=f'{random.choice(SPELLING_LEXICON["correct"])}'
        )
        await send_question(message, state)
    else:
        mistake = (f'<s>{message.text.lower()}</s> - '
                   f'{data["spelling"].lower()}\n')
        await state.update_data(
            incorrect=data['incorrect'] + 1,
            mistakes=data['mistakes'] + mistake
        )
        await message.answer(
            text=(f'{random.choice(SPELLING_LEXICON["incorrect"])}'
                  f'{SPELLING_LEXICON["feedback"]}{data["spelling"].lower()}')
        )
        await send_question(message, state)


async def show_result(message: Message, data: dict) -> None:
    """Show result handler."""
    await message.answer(
        text=(f'{SPELLING_LEXICON["result_title"]}'
              f'{SPELLING_LEXICON["total_correct"]}{data["correct"]}\n'
              f'{SPELLING_LEXICON["total_incorrect"]}{data["incorrect"]}\n'
              f'{SPELLING_LEXICON["mistakes"] if data["mistakes"] else ""}'
              f'{data["mistakes"]}')
    )
    await backend_api.update_user_task_results(
        data['user_tg_id'], data['exercise_id'], data['correct'],
        data['incorrect']
    )


def register_spelling_handlers(dp: Dispatcher) -> None:
    """Helper function to register spelling handlers."""
    dp.register_callback_query_handler(start_spelling, text='start',
                                       state=Spelling.intro)
    dp.register_callback_query_handler(exit_spelling, text='exit',
                                       state=Spelling.intro)
    dp.register_message_handler(check_spelling, state=Spelling.in_progress)
