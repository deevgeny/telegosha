from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def test_keyboard(buttons: list[dict[str, str]]) -> InlineKeyboardMarkup:
    """Test keyboard.

    Create test buttons based on api data response.
    Input data:
      buttons: [{'button_text': 'callback'}, ...]
    Input example:
      buttons: [{'blue': 'correct'}, {'green': 'incorrect'}, ...]
    """
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    for button in buttons:
        text, callback = next(iter(button.items()))
        keyboard.add(InlineKeyboardButton(text=text, callback_data=callback))
    return keyboard


def inline_keyboard(buttons: list[list[str]],
                    row_width: int) -> InlineKeyboardMarkup:
    """Create inline keyboard.

    Input:
      buttons: [['button_text', 'callback_text'],...]
      row_width: number of buttons in one row
    """
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=row_width)
    for button in buttons:
        keyboard.insert(
            InlineKeyboardButton(text=button[0], callback_data=button[1])
        )
    return keyboard
