import asyncio
import os
from random import randint
from aiogram import F, Bot, Router
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message, PreCheckoutQuery, CallbackQuery, FSInputFile, ChatJoinRequest
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from reely.classes import InstagramDownloader, fact_list
import reely.keyboards as kb
from config import USERNAME, PASSWORD, CHANNEL_ID, CHANNEL_LINK, TOKEN
bot = Bot(token=TOKEN)




router = Router()
downloader = InstagramDownloader(USERNAME, PASSWORD)
INSTAGRAM_URL_REGEX = r"(https?:\/\/)?(www\.)?instagram\.com\/(reel|p)\/[\w-]+\/?"
download_dir = "downloads"
if not os.path.exists(download_dir):
    os.mkdir(download_dir)
pending_requests = set()

async def is_subscribed(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in ("member", "administrator", "creator")
    except Exception:
        return False
    


async def subscription_check(user, msg: Message) -> bool:
    if await is_subscribed(user):
        return True
    elif user in pending_requests:
        return True
    else:
        await msg.answer(f"Subscribe first: {CHANNEL_LINK}", reply_markup=kb.subscribe_channel)
        return False
@router.chat_join_request()
async def handle_join_request(update: ChatJoinRequest):
    pending_requests.add(update.from_user.id)
    # Optionally notify admins or log the request

@router.message(CommandStart())
async def start(message:Message):
    if not await subscription_check(message.from_user.id, message):
        return
    await message.answer("Hello the bot is working")

@router.callback_query(F.data == "subchek")
async def subchek(callback: CallbackQuery, message: Message):
    if not await subscription_check(message.from_user.id, message):
        await callback.answer("Your not subscribed yet",)
        return
    await callback.answer("Your are okay to go")

@router.message(F.text.regexp(INSTAGRAM_URL_REGEX))
async def handle_instagram_reel(message: Message):
    if not await subscription_check(message.from_user.id, message):
        return
    x = await message.answer(f"✅ Instagram post detected! Did you know: {fact_list[randint(0, len(fact_list)-1)]}")
    
    downloader.download_single_post(url=message.text, id=message.from_user.id)
    # await message.answer(str(file_path)) // for debuging 
    for file in os.listdir(download_dir):
        if file.endswith(".mp4"):
            upload_dir = f"downloads\\{file}"
            # await message.answer(str(file)) // for debuging 
            reel = FSInputFile(upload_dir, filename=str(file))
            await message.answer_video(video=reel, caption="📥 Downloaded via @ReelyFastBot", reply_markup=kb.add_to_group)
            os.remove(upload_dir)
        if file.endswith(".txt"):
            txt_dir = f"downloads\\{file}"
            os.remove(txt_dir)
        if file.endswith(".jpg"):
            upload_dir = f"downloads\\{file}"
            img = FSInputFile(upload_dir, filename=str(file))
            await message.answer_photo(img, caption="📥 Downloaded via @ReelyFastBot")
            os.remove(upload_dir)

    await x.delete()

@router.message()
async def catch_all(message: Message):
    if not await subscription_check(message.from_user.id, message):
        return
    await message.answer("Pls send instagram url/link")