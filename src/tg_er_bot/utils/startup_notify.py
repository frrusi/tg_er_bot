from aiogram import Dispatcher


def on_startup_notify(dp: Dispatcher):
    pass
    # USERS = []
    # for user in DataBase('../database/', 'users', '.db').get_users():
    #     USERS.append(*user)
    #
    # for user in USERS:
    #     try:
    #         await dp.bot.send_message(user, 'Привет! Я снова включился...', reply_markup=types.ReplyKeyboardRemove())
    #
    #     except Exception as err:
    #         logging.error(err)
