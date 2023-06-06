import os
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
from pyppeteer import launch
from tiktok import TikTokAPI

# Replace <BOT_TOKEN> with your Telegram bot token
TOKEN = '6179143538:AAHL47_OiZ0hmLUd7yJWsUhMCdFvHtpKIv4'

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Replace <USERNAME> and <PASSWORD> with your TikTok account credentials
USERNAME = 'vimukthioada5@gmail.com'
PASSWORD = 'OShada2005@'
api = TikTokAPI(username=USERNAME, password=PASSWORD)


@dp.message_handler(Command("start"))
async def start_command(message: types.Message):
    await message.reply("Welcome to the TikTok Download Bot! Send me a TikTok video URL to get started.")


@dp.message_handler()
async def download_tiktok(message: types.Message, state: FSMContext):
    url = message.text.strip()

    await bot.send_chat_action(message.chat.id, "typing")
    try:
        await message.reply("Processing the video... Please wait.")

        video_path = await download_video(url)
        await bot.send_video(message.chat.id, video_path)

        await message.reply("Video download complete!")

        os.remove(video_path)
    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")


async def download_video(url: str) -> str:
    async with launch() as browser:
        page = await browser.newPage()
        await page.goto(url)
        video_url = await page.evaluate("() => window.__INIT_PROPS__?.pageProps?.itemInfo?.itemStruct?.video?.downloadAddr")
        video_path = f"videos/{url.split('/')[-1]}.mp4"

        async with api.session() as session:
            await session.get_video(video_url, output_path=video_path)

        return video_path


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
