from aiogram import *
from telegram import Update
from pytube import *
import os

token = '5809552126:AAHzOC_An6lO18fT8YeT__BZosXM34vJPRU'
bot = Bot(token)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_message(message):
    chat_id = message.chat.id
    await bot.send_message(chat_id, 'Привет. Хочешь скачать видео из YouTube. Отправь ссылку.')
    
@dp.message_handler()
async def text_message(message):
    chat_id = message.chat.id
    url = message.text
    youtube = YouTube(url)
    if 'https://www.youtube.com/' or 'https://www.youtu.be/' in message:
        await bot.send_message(chat_id, f'Идёт загрузка видео: {youtube.title} с канала: {youtube.author} {youtube.channel_url}.')
        await download_video(url, message, bot)

async def download_video(url, message, bot):
    chat_id = message.chat.id
    youtube = YouTube(url)
    stream = youtube.streams.filter(file_extension='mp4')
    stream.get_highest_resolution().download('Downloading video', f'{chat_id}')
    with open(f'Downloading video\{chat_id}', 'rb') as video:
        await bot.send_video(chat_id, video, caption='Получите и распишитесь')
        os.remove(f'Downloading video\{chat_id}')

if __name__ == '__main__':
    executor.start_polling(dp)