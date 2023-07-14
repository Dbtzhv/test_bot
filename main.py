from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio

# указать токен бота и telegram id, куда будут присылаться выполнено/невыполнено/проигнорировано

bot = Bot(token='')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
MANAGER_CHAT_ID = ''


@dp.message_handler(commands=['set_reminder'])
async def set_reminder(message: types.Message):
    args = message.get_args().split(',')

    if len(args) != 5:
        await message.reply('Неверное количество аргументов.')
        return

    tel_id, text, date, time, answer_time = args

    # Создание инлайн-клавиатуры
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(
        types.InlineKeyboardButton(text='Выполнено', callback_data='done'),
        types.InlineKeyboardButton(text='Не сделано', callback_data='not_done')
    )

    await bot.send_message(chat_id=tel_id, text='Пожалуйста, выберите одну из опций:', reply_markup=keyboard)

    await asyncio.sleep(int(answer_time)*60)
    await bot.send_message(chat_id=MANAGER_CHAT_ID, text=f'Пользователь {tel_id} проигнорировал задачу')



@dp.callback_query_handler()
async def process_callback(callback_query: types.CallbackQuery):
    tel_id = callback_query.from_user.id
    button = callback_query.data

    if button == 'done' or button == 'not_done':
        await bot.send_message(chat_id=MANAGER_CHAT_ID, text=f'Пользователь {tel_id} нажал кнопку "{button}"')





if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
