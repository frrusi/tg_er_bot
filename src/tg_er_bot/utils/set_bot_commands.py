from aiogram import types


def set_default_commands(dp):
    dp.bot.set_my_commands(
        [
            types.BotCommand('start', 'Запустить бота'),
            types.BotCommand('help', 'Помощь')
        ]
    )
