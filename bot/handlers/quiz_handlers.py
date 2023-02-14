import logging
import random

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from handlers import callbacks
from keyboards.user_keyboards import inline_keyboard, quiz_keyboard
from lexicon.russian import QUIZ_LEXICON
from misc.api import backend_api

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Quiz(StatesGroup):
    """Quiz FSM"""
    intro = State()
    in_progress = State()
    show_result = State()


async def quiz_intro(callback: CallbackQuery, state: FSMContext,
                     task: dict) -> None:
    """Quiz entry point from tasks handlers."""
    await state.update_data(user_tg_id=callback.from_user.id,
                            exercise_id=task['id'],
                            questions=task['data'], correct=0, incorrect=0,
                            left=len(task['data']), mistakes="")
    await state.set_state(Quiz.intro)
    await callback.message.edit_text(
        text=(f'{QUIZ_LEXICON["title"]}'
              f'{QUIZ_LEXICON["topic"]}{task["topic"].lower()}\n'
              f'{QUIZ_LEXICON["total_questions"]}{len(task["data"])}\n\n'
              f'{QUIZ_LEXICON["rules"]}'),
        reply_markup=inline_keyboard(
            buttons=[[QUIZ_LEXICON['start_button'], callbacks.START],
                     [QUIZ_LEXICON['exit_button'], callbacks.EXIT]],
            row_width=2
        )
    )


async def start_quiz(callback: CallbackQuery, state: FSMContext) -> None:
    """Start quiz handler."""
    await state.set_state(Quiz.in_progress)
    await send_question(callback, state)


async def exit_quiz(callback: CallbackQuery, state: FSMContext) -> None:
    """Exit quiz handler."""
    await state.reset_state()
    await callback.message.delete()


async def send_question(callback: CallbackQuery, state: FSMContext) -> None:
    """Helper function to send question."""
    data = await state.get_data()
    # Use negative index to get questions from the list
    question = data['questions'][- data['left']]
    await state.update_data(left=data['left'] - 1)
    await callback.message.edit_text(
        text=f'{QUIZ_LEXICON["title"]}{question["word"]}',
        reply_markup=quiz_keyboard(question['buttons'])
    )


async def correct_answer(callback: CallbackQuery, state: FSMContext) -> None:
    """Correct answer handler."""
    data = await state.get_data()
    await state.update_data(correct=data['correct'] + 1)
    if data['left'] == 0:
        await state.set_state(Quiz.show_result)
        keyboard = inline_keyboard(
            buttons=[[QUIZ_LEXICON['result_button'], callbacks.SHOW_RESULT]],
            row_width=1
        )
    else:
        keyboard = inline_keyboard(
            buttons=[[QUIZ_LEXICON['next_button'], callbacks.NEXT_QUESTION]],
            row_width=1
        )
    await callback.message.edit_text(
        text=(f'{QUIZ_LEXICON["title"]}'
              f'{random.choice(QUIZ_LEXICON["correct"])}'
              f'{QUIZ_LEXICON["total_left"]}{data["left"]}'),
        reply_markup=keyboard
    )


async def incorrect_answer(callback: CallbackQuery, state: FSMContext) -> None:
    """Incorrect answer handler."""
    data = await state.get_data()
    await state.update_data(incorrect=data['incorrect'] + 1)
    if data['left'] == 0:
        await state.set_state(Quiz.show_result)
        keyboard = inline_keyboard(
            buttons=[[QUIZ_LEXICON['result_button'], callbacks.SHOW_RESULT]],
            row_width=1
        )
    else:
        keyboard = inline_keyboard(
            buttons=[[QUIZ_LEXICON['next_button'], callbacks.NEXT_QUESTION]],
            row_width=1
        )
    await callback.message.edit_text(
        text=(f'{QUIZ_LEXICON["title"]}'
              f'{random.choice(QUIZ_LEXICON["incorrect"])}'
              f'{QUIZ_LEXICON["total_left"]}{data["left"]}'),
        reply_markup=keyboard
    )


async def quiz_result(callback: CallbackQuery, state: FSMContext) -> None:
    """Send quiz result message."""
    data = await state.get_data()
    await state.reset_state()
    # Refactor
    text = (f'{QUIZ_LEXICON["result_title"]}'
            f'{QUIZ_LEXICON["total_correct"]}{data["correct"]}\n'
            f'{QUIZ_LEXICON["total_incorrect"]}{data["incorrect"]}')
    await callback.message.edit_text(text=text)
    await backend_api.update_user_task_results(
        user_tg_id=data['user_tg_id'], exercise_id=data['exercise_id'],
        incorrect=data['incorrect'], correct=data['correct']
    )


async def quiz_warning(message: Message):
    """Quiz warning message."""
    await message.answer(text=QUIZ_LEXICON['quiz_warning'])


def register_quiz_handlers(dp: Dispatcher) -> None:
    dp.register_callback_query_handler(start_quiz, text=callbacks.START,
                                       state=Quiz.intro)
    dp.register_callback_query_handler(exit_quiz, text=callbacks.EXIT,
                                       state=Quiz.intro)
    dp.register_callback_query_handler(correct_answer, text=callbacks.CORRECT,
                                       state=Quiz.in_progress)
    dp.register_callback_query_handler(incorrect_answer,
                                       text=callbacks.INCORRECT,
                                       state=Quiz.in_progress)
    dp.register_callback_query_handler(send_question,
                                       text=callbacks.NEXT_QUESTION,
                                       state=Quiz.in_progress)
    dp.register_callback_query_handler(quiz_result, text=callbacks.SHOW_RESULT,
                                       state=Quiz.show_result)
    dp.register_message_handler(
        quiz_warning, content_types='any',
        state=[Quiz.in_progress, Quiz.show_result]
    )
