from aiogram import Dispatcher, types

from lexicon.russian import COMMANDS_LEXICON


async def set_main_menu(dp: Dispatcher):
    """Set main menu commands."""
    main_menu_commands = [
        types.BotCommand(command='/tasks',
                         description=COMMANDS_LEXICON['tasks_description']),
        types.BotCommand(command='/cancel',
                         description=COMMANDS_LEXICON['cancel_description']),
        types.BotCommand(command='/help',
                         description=COMMANDS_LEXICON['help_description']),
    ]
    await dp.bot.set_my_commands(main_menu_commands)
