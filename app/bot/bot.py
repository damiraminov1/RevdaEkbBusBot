import logging
from aiogram import Bot, Dispatcher, executor, types

from config import Config
from app.parser.parser import Parser

bot = Bot(token=Config.TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)
buttons = {'from_revda': 'Из Ревды', 'from_ekb': 'Из Екатеринбурга', 'full_schedule': 'Полное расписание'}


def get_start_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bus_from_revda = types.KeyboardButton(buttons['from_revda'])
    bus_from_ekb = types.KeyboardButton(buttons['from_ekb'])
    full_schedule = types.KeyboardButton(buttons['full_schedule'])
    markup.add(bus_from_revda, bus_from_ekb, full_schedule)
    return markup


@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.reply('Привет! Это бот расписания автобусов Ревда-Екб', reply_markup=get_start_markup())


@dp.message_handler(content_types='text')
async def main(message: types.Message):
    if message.text in buttons.values():
        data = Parser.get_content(url=Config.HOST)
        if data['status'] != 'failed':
            if message.text == buttons['from_revda']:
                answer = data['price'] + '\n' + data['from_revda'] + '\n' + data['additional_information']
                await message.answer(answer)
            elif message.text == buttons['from_ekb']:
                answer = data['price'] + '\n' + data['from_ekb'] + '\n' + data['additional_information']
                await message.answer(answer)
            elif message.text == buttons['full_schedule']:
                answer = data['price'] + '\n' + data['full_schedule'] + '\n' + data['additional_information']
                await message.answer(answer)
