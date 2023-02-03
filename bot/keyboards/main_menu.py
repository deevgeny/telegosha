from aiogram import Dispatcher, types


async def set_main_menu(dp: Dispatcher):
    """Set main menu commands."""
    main_menu_commands = [
        types.BotCommand(command='/tasks',
                         description='задания'),
        types.BotCommand(command='/help',
                         description='подсказка'),
        types.BotCommand(command='/cancel',
                         description='отменить задание'),
    ]
    await dp.bot.set_my_commands(main_menu_commands)
