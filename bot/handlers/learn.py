"""
This module is responsible for new words learning task.

Steps:
- User receives new word in callback query message with 3 answer options
  (word buttons).
- User presses one button.
- If answer is correct user receives next new word.
- If answer is incorrect user recieves same word.
- When all new words run out, user receives task feedback.
- Task result is saved on server.
"""
import logging
import random

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery, ContentType, Message

from handlers import callbacks
from keyboards.user_keyboards import inline_keyboard, test_keyboard
from lexicon.russian import LEARN_LEXICON
from misc.api import backend_api

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Learn(StatesGroup):
    """Intro FSM"""
    intro = State()
    in_progress = State()
    show_result = State()


async def learn_entry_point(message: Message, state: FSMContext,
                            task: dict) -> None:
    """Learn entry point from tasks handlers."""
    await state.update_data(user_tg_id=message.from_user.id,
                            task_id=task['id'],
                            questions=task['data'], correct=0, incorrect=0,
                            left=len(task['data']), mistakes='')
    await state.set_state(Learn.intro)
    await message.answer(
        text=(f'{LEARN_LEXICON["title"]}'
              f'{LEARN_LEXICON["topic"]}{task["topic"].lower()}\n'
              f'{LEARN_LEXICON["total_words"]}{len(task["data"])}\n\n'
              f'{LEARN_LEXICON["rules"]}'),
        reply_markup=inline_keyboard(
            buttons=[[LEARN_LEXICON['start_button'], callbacks.START],
                     [LEARN_LEXICON['exit_button'], callbacks.EXIT]],
            row_width=2
        )
    )


async def start_learn(callback: CallbackQuery, state: FSMContext) -> None:
    """Start learn handler."""
    await state.set_state(Learn.in_progress)
    await send_new_word(callback, state)


async def exit_learn(callback: CallbackQuery, state: FSMContext) -> None:
    """Exit learn handler."""
    await state.reset_state()
    await callback.message.delete()


async def send_new_word(callback: CallbackQuery, state: FSMContext) -> None:
    """Send new word handler."""
    data = await state.get_data()
    # Use negative index to get question from the list
    question = data['questions'][-data['left']]
    await callback.message.edit_text(
        text=(f'{LEARN_LEXICON["title"]}{question["origin"]} - '
              f'{question["word"]}'),
        reply_markup=inline_keyboard(
            buttons=[[LEARN_LEXICON["check_button"], callbacks.CHECK]],
            row_width=1
        )
    )


async def check_new_word(callback: CallbackQuery, state: FSMContext) -> None:
    """Check new word handler."""
    data = await state.get_data()
    question = data['questions'][-data['left']]
    await callback.message.edit_text(
        text=f'{LEARN_LEXICON["title"]}{question["word"]}',
        reply_markup=test_keyboard(question['buttons'])
    )


async def correct_answer(callback: CallbackQuery, state: FSMContext) -> None:
    """Correct answer handler."""
    data = await state.get_data()
    await state.update_data(correct=data['correct'] + 1)
    if data['left'] == 0:
        await state.set_state(Learn.show_result)
        keyboard = inline_keyboard(
            buttons=[[LEARN_LEXICON['result_button'], callbacks.SHOW_RESULT]],
            row_width=1
        )
    else:
        await state.update_data(left=data['left'] - 1)
        keyboard = inline_keyboard(
            buttons=[[LEARN_LEXICON['next_button'], callbacks.NEXT_QUESTION]],
            row_width=1
        )
    await callback.message.edit_text(
        text=(f'{LEARN_LEXICON["title"]}'
              f'{random.choice(LEARN_LEXICON["correct"])}'
              f'{LEARN_LEXICON["total_left"]}{data["left"]}'),
        reply_markup=keyboard
    )


async def incorrect_answer(callback: CallbackQuery, state: FSMContext) -> None:
    """Incorrect answer handler."""
    data = await state.get_data()
    await state.update_data(incorrect=data['incorrect'] + 1)
    if data['left'] == 0:
        await state.set_state(Learn.show_result)
        keyboard = inline_keyboard(
            buttons=[[LEARN_LEXICON['result_button'], callbacks.SHOW_RESULT]],
            row_width=1
        )
    else:
        keyboard = inline_keyboard(
            buttons=[[LEARN_LEXICON['next_button'], callbacks.NEXT_QUESTION]],
            row_width=1
        )
    await callback.message.edit_text(
        text=(f'{LEARN_LEXICON["title"]}'
              f'{random.choice(LEARN_LEXICON["incorrect"])}'
              f'{LEARN_LEXICON["total_left"]}{data["left"]}'),
        reply_markup=keyboard
    )


async def learn_result(callback: CallbackQuery, state: FSMContext) -> None:
    """Send learn result message."""
    data = await state.get_data()
    await state.reset_state()
    await callback.message.edit_text(
        text=(f'{LEARN_LEXICON["result_title"]}'
              f'{LEARN_LEXICON["total_correct"]}{data["correct"]}\n'
              f'{LEARN_LEXICON["total_incorrect"]}{data["incorrect"]}')
    )
    await backend_api.update_user_task_results(
        user_tg_id=data['user_tg_id'], task_id=data['task_id'],
        incorrect=data['incorrect'], correct=data['correct']
    )


async def learn_warning(message: Message):
    """Learn warning message."""
    await message.answer(text=LEARN_LEXICON['warning'])


def register_learn_handlers(dp: Dispatcher) -> None:
    dp.register_callback_query_handler(start_learn, text=callbacks.START,
                                       state=Learn.intro)
    dp.register_callback_query_handler(exit_learn, text=callbacks.EXIT,
                                       state=Learn.intro)
    dp.register_callback_query_handler(send_new_word,
                                       text=callbacks.NEXT_QUESTION,
                                       state=Learn.in_progress)
    dp.register_callback_query_handler(check_new_word, text=callbacks.CHECK,
                                       state=Learn.in_progress)
    dp.register_callback_query_handler(correct_answer, text=callbacks.CORRECT,
                                       state=Learn.in_progress)
    dp.register_callback_query_handler(incorrect_answer,
                                       text=callbacks.INCORRECT,
                                       state=Learn.in_progress)
    dp.register_callback_query_handler(learn_result,
                                       text=callbacks.SHOW_RESULT,
                                       state=Learn.show_result)
    dp.register_message_handler(
        learn_warning, content_types=ContentType.ANY,
        state=[Learn.in_progress, Learn.show_result]
    )
