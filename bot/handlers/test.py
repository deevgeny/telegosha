"""
This module is responsible for new words test task.

Steps:
- User receives new word in callback query message with 3 answer options
  (word buttons).
- User presses one button.
- If answer is correct, correct counter increased by 1 and user receives
  next new word.
- If answer is incorrect, incorrect counter increased by 1 and user recieves
  next word.
- When all new words run out, user receives task feedback.
- Correct and incorrect answers saved on server.
"""
import logging
import random

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery, ContentType, Message

from handlers import callbacks
from keyboards.user_keyboards import inline_keyboard, test_keyboard
from lexicon.russian import TEST_LEXICON
from misc.api import backend_api

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Test(StatesGroup):
    """Test FSM"""
    intro = State()
    in_progress = State()
    show_result = State()


async def test_entry_point(message: Message, state: FSMContext,
                           task: dict) -> None:
    """Test entry point from tasks handlers."""
    await state.update_data(user_tg_id=message.from_user.id,
                            task_id=task['id'],
                            questions=task['data'], correct=0, incorrect=0,
                            left=len(task['data']), mistakes='')
    await state.set_state(Test.intro)
    await message.answer(
        text=(f'{TEST_LEXICON["title"]}'
              f'{TEST_LEXICON["topic"]}{task["topic"].lower()}\n'
              f'{TEST_LEXICON["total_words"]}{len(task["data"])}\n\n'
              f'{TEST_LEXICON["rules"]}'),
        reply_markup=inline_keyboard(
            buttons=[[TEST_LEXICON['start_button'], callbacks.START],
                     [TEST_LEXICON['exit_button'], callbacks.EXIT]],
            row_width=2
        )
    )


async def start_test(callback: CallbackQuery, state: FSMContext) -> None:
    """Start test handler."""
    await state.set_state(Test.in_progress)
    await send_question(callback, state)


async def exit_test(callback: CallbackQuery, state: FSMContext) -> None:
    """Exit test handler."""
    await state.reset_state()
    await callback.message.delete()


async def send_question(callback: CallbackQuery, state: FSMContext) -> None:
    """Helper function to send question."""
    data = await state.get_data()
    # Use negative index to get question from the list
    question = data['questions'][-data['left']]
    await state.update_data(left=data['left'] - 1)
    await callback.message.edit_text(
        text=f'{TEST_LEXICON["title"]}{question["word"]}',
        reply_markup=test_keyboard(question['buttons'])
    )


async def correct_answer(callback: CallbackQuery, state: FSMContext) -> None:
    """Correct answer handler."""
    data = await state.get_data()
    await state.update_data(correct=data['correct'] + 1)
    if data['left'] == 0:
        await state.set_state(Test.show_result)
        keyboard = inline_keyboard(
            buttons=[[TEST_LEXICON['result_button'], callbacks.SHOW_RESULT]],
            row_width=1
        )
    else:
        keyboard = inline_keyboard(
            buttons=[[TEST_LEXICON['next_button'], callbacks.NEXT_QUESTION]],
            row_width=1
        )
    await callback.message.edit_text(
        text=(f'{TEST_LEXICON["title"]}'
              f'{random.choice(TEST_LEXICON["correct"])}'
              f'{TEST_LEXICON["total_left"]}{data["left"]}'),
        reply_markup=keyboard
    )


async def incorrect_answer(callback: CallbackQuery, state: FSMContext) -> None:
    """Incorrect answer handler."""
    data = await state.get_data()
    await state.update_data(incorrect=data['incorrect'] + 1)
    if data['left'] == 0:
        await state.set_state(Test.show_result)
        keyboard = inline_keyboard(
            buttons=[[TEST_LEXICON['result_button'], callbacks.SHOW_RESULT]],
            row_width=1
        )
    else:
        keyboard = inline_keyboard(
            buttons=[[TEST_LEXICON['next_button'], callbacks.NEXT_QUESTION]],
            row_width=1
        )
    await callback.message.edit_text(
        text=(f'{TEST_LEXICON["title"]}'
              f'{random.choice(TEST_LEXICON["incorrect"])}'
              f'{TEST_LEXICON["total_left"]}{data["left"]}'),
        reply_markup=keyboard
    )


async def test_result(callback: CallbackQuery, state: FSMContext) -> None:
    """Send test result message."""
    data = await state.get_data()
    await state.reset_state()
    await callback.message.edit_text(
        text=(f'{TEST_LEXICON["result_title"]}'
              f'{TEST_LEXICON["total_correct"]}{data["correct"]}\n'
              f'{TEST_LEXICON["total_incorrect"]}{data["incorrect"]}')
    )
    await backend_api.update_user_task_results(
        user_tg_id=data['user_tg_id'], task_id=data['task_id'],
        incorrect=data['incorrect'], correct=data['correct']
    )


async def test_warning(message: Message):
    """Test warning message."""
    await message.answer(text=TEST_LEXICON['warning'])


def register_test_handlers(dp: Dispatcher) -> None:
    dp.register_callback_query_handler(start_test, text=callbacks.START,
                                       state=Test.intro)
    dp.register_callback_query_handler(exit_test, text=callbacks.EXIT,
                                       state=Test.intro)
    dp.register_callback_query_handler(correct_answer, text=callbacks.CORRECT,
                                       state=Test.in_progress)
    dp.register_callback_query_handler(incorrect_answer,
                                       text=callbacks.INCORRECT,
                                       state=Test.in_progress)
    dp.register_callback_query_handler(send_question,
                                       text=callbacks.NEXT_QUESTION,
                                       state=Test.in_progress)
    dp.register_callback_query_handler(test_result, text=callbacks.SHOW_RESULT,
                                       state=Test.show_result)
    dp.register_message_handler(
        test_warning, content_types=ContentType.ANY,
        state=[Test.in_progress, Test.show_result]
    )
