import asyncio
import logging
import base64
import sys
import os
import io
import json
import aiohttp
import requests
from typing import BinaryIO
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, File, ContentType
from aiogram.utils.markdown import hbold

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
API_URL = os.getenv('API_URL')

dp = Dispatcher()
bot = Bot(token=TELEGRAM_BOT_TOKEN, parse_mode=ParseMode.HTML)


async def file_handler(message: Message) -> BinaryIO:
    if message.voice is None:
        raise TypeError('Message is not a voice')
    file_id = message.voice.file_id
    file = await bot.get_file(file_id)
    file = await bot.download_file(file.file_path)

    return file


async def send_request_to_transcriber_voice(audio_file: BinaryIO) -> dict:
    base64_content = base64.b64encode(audio_file.read()).decode('utf-8')

    webhook = '/api/transcribe_voice'
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'X-API-KEY-Token': os.getenv('APP_SECRET'),
    }

    request_data = {
        'voice': base64_content
    }
    async with aiohttp.ClientSession() as session:
        response = await session.post(f'{API_URL}{webhook}', headers=headers, json=request_data)
        content = await response.json()
        return content


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    greeting_message = f'''
    Hello {hbold(message.from_user.full_name)}!\nBot can transcribe video note and voices into text
    '''
    await message.answer(greeting_message)


@dp.message()
async def handler(message: Message):
    try:
        audio_file = await file_handler(message)
        content = await send_request_to_transcriber_voice(audio_file)

        transcribed_voice = content.get('text')
        await message.answer(text=transcribed_voice)
    except Exception as e:
        await message.answer(text=f'{e}')


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
