from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from lexicon.russian import QUIZ_LEXICON, SPELLING_LEXICON, TASKS_LEXICON


def quiz_start_keyboard() -> InlineKeyboardMarkup:
    """Quiz start keyboard."""
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton(text=QUIZ_LEXICON['start_button'],
                             callback_data='start'),
        InlineKeyboardButton(text=QUIZ_LEXICON['exit_button'],
                             callback_data='exit')
    )
    return keyboard


def spelling_start_keyboard() -> InlineKeyboardMarkup:
    """Spelling start keyboard."""
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton(text=SPELLING_LEXICON['start_button'],
                             callback_data='start'),
        InlineKeyboardButton(text=SPELLING_LEXICON['exit_button'],
                             callback_data='exit')
    )
    return keyboard


def quiz_keyboard(buttons: list[dict[str, str]]) -> InlineKeyboardMarkup:
    """Quiz keyboard."""
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    for button in buttons:
        text, callback = next(iter(button.items()))
        keyboard.add(InlineKeyboardButton(text=text, callback_data=callback))
    return keyboard


def next_question_keyboard() -> InlineKeyboardMarkup:
    """Next question keyboard."""
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton(text=QUIZ_LEXICON['next_button'],
                                      callback_data='next_question'))
    return keyboard


def show_result_keyboard() -> InlineKeyboardMarkup:
    """Show results keyboard."""
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton(text=QUIZ_LEXICON['result_button'],
                                      callback_data='show_result'))
    return keyboard


def tasks_keyboard() -> InlineKeyboardMarkup:
    """Tasks keyboard."""
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=3)
    keyboard.add(
        InlineKeyboardButton(text=TASKS_LEXICON['back_button'],
                             callback_data='previous_task'),
        InlineKeyboardButton(text=TASKS_LEXICON['select_button'],
                             callback_data='select_task'),
        InlineKeyboardButton(text=TASKS_LEXICON['forward_button'],
                             callback_data='next_task'),
    )
    return keyboard
