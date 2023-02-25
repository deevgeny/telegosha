"""
This module is responsible for new words introduction task.

Steps:
- User receives new word in callback query message text update.
- User reads new word and presses 'next' button to get next word.
- When all new words run out, user receives feedback.
- Task result is saved on server.
"""
import logging

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery, ContentType, Message

from handlers import callbacks
from keyboards.user_keyboards import inline_keyboard
from lexicon.russian import INTRO_LEXICON
from misc.api import backend_api

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Intro(StatesGroup):
    """Intro FSM"""
    intro = State()
    in_progress = State()
    show_result = State()


async def intro_entry_point(message: Message, state: FSMContext,
                            task: dict) -> None:
    """Intro entry point from tasks handlers."""
    await state.update_data(user_tg_id=message.from_user.id,
                            task_id=task['id'], questions=task['data'],
                            left=len(task['data']))
    await state.set_state(Intro.intro)
    await message.answer(
        text=(f'{INTRO_LEXICON["title"]}'
              f'{INTRO_LEXICON["topic"]}{task["topic"].lower()}\n'
              f'{INTRO_LEXICON["total_words"]}{len(task["data"])}\n\n'
              f'{INTRO_LEXICON["rules"]}'),
        reply_markup=inline_keyboard(
            buttons=[[INTRO_LEXICON['start_button'], callbacks.START],
                     [INTRO_LEXICON['exit_button'], callbacks.EXIT]],
            row_width=2
        )
    )


async def start_intro(callback: CallbackQuery, state: FSMContext) -> None:
    """Start intro handler."""
    await state.set_state(Intro.in_progress)
    await send_word(callback, state)


async def exit_intro(callback: CallbackQuery, state: FSMContext) -> None:
    """Exit intro handler."""
    await state.reset_state()
    await callback.message.delete()


async def send_word(callback: CallbackQuery, state: FSMContext) -> None:
    """Send next word handler."""
    data = await state.get_data()
    # Prepare keyboards
    if data['left'] == 1:
        await state.set_state(Intro.show_result)
        keyboard = inline_keyboard(
            buttons=[[INTRO_LEXICON['result_button'], callbacks.SHOW_RESULT]],
            row_width=1
        )
    else:
        keyboard = inline_keyboard(
            buttons=[[INTRO_LEXICON["next_button"], callbacks.NEXT_QUESTION]],
            row_width=1
        )
    # Use negative index to get question from the list
    question = data['questions'][-data['left']]
    await state.update_data(left=data['left'] - 1)
    await callback.message.delete()
    if question.get('sound'):
        await callback.message.answer_audio(
            caption=f'{question["origin"]} - {question["translation"]}',
            audio=question['sound'],
            reply_markup=keyboard
        )
    else:
        await callback.message.answer(
            text=f'{question["origin"]} - {question["translation"]}',
            reply_markup=keyboard
        )


async def intro_result(callback: CallbackQuery, state: FSMContext) -> None:
    """Send intro result message and save user results to backend."""
    data = await state.get_data()
    await state.reset_state()
    await callback.message.delete()
    await callback.message.answer(
        text=f'{INTRO_LEXICON["result_title"]}'
    )
    await backend_api.update_user_task_results(
        user_tg_id=data['user_tg_id'], task_id=data['task_id'],
        incorrect=data['left'], correct=len(data['questions'])
    )


async def test_warning(message: Message):
    """Intro warning message."""
    await message.answer(text=INTRO_LEXICON['warning'])


def register_intro_handlers(dp: Dispatcher) -> None:
    dp.register_callback_query_handler(start_intro, text=callbacks.START,
                                       state=Intro.intro)
    dp.register_callback_query_handler(exit_intro, text=callbacks.EXIT,
                                       state=Intro.intro)
    dp.register_callback_query_handler(send_word,
                                       text=callbacks.NEXT_QUESTION,
                                       state=Intro.in_progress)
    dp.register_callback_query_handler(intro_result,
                                       text=callbacks.SHOW_RESULT,
                                       state=Intro.show_result)
    dp.register_message_handler(
        test_warning, content_types=ContentType.ANY,
        state=[Intro.intro, Intro.in_progress]
    )
