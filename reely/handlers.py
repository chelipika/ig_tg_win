import asyncio
import os
import shutil
from random import randint
from aiogram import F, Bot, Router
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message, PreCheckoutQuery, CallbackQuery, FSInputFile, ChatJoinRequest
from aiogram.types import ChatMemberUpdated
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import reely.keyboards as kb
import database.requests as rq
import instaloader
import re
import uuid
from datetime import datetime
from config import CHANNEL_ID, CHANNEL_LINK, TOKEN
bot = Bot(token=TOKEN)
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=5)  # Adjust based on server capacity
fact_list = [
    "🔥 Instagram boasts over 2 billion monthly active users.",
    "📸 High-quality visuals drive engagement.",
    "🗓️ Consistent posting keeps you visible.",
    "⚙️ Engagement fuels the algorithm.",
    "📖 Stories offer direct audience connection.",
    "🎥 Video content often outperforms images.",
    "🎬 Reels can dramatically increase reach.",
    "🙌 User-generated content builds credibility.",
    "🔍 Smart hashtag use boosts discoverability.",
    "🎯 Instagram ads allow precise targeting.",
    "👤 A clear bio converts visitors into followers.",
    "📚 Carousel posts capture more attention.",
    "📊 Analytics reveal what truly works.",
    "🛒 Instagram Shopping simplifies product sales.",
    "🤝 Influencer collaborations extend your audience.",
    "📝 Captions matter—be clear and compelling.",
    "⏰ Posting at peak times maximizes views.",
    "💡 Leverage various formats to keep content fresh.",
    "📍 Location tags attract local audiences.",
    "🔄 Regular testing refines your strategy.",
    "Instagram has over 2 billion monthly active users! 🌍",
    "The first Instagram post was a photo of a dog and a taco stand! 🐶🌮",
    "The most-liked post on Instagram is the photo of an egg! 🥚",
    "Instagram Stories are used by 500 million people daily! 📸",
    "The most popular hashtag on Instagram is #Love! ❤️",
    "Instagram was launched on October 6, 2010! 🎉",
    "The average user spends 30 minutes per day on Instagram! ⏳",
    "70% of Instagram users are under the age of 35! 👶",
    "Instagram is the second most downloaded free app on the App Store! 📱",
    "The most-followed account on Instagram is Instagram itself! 📈",
    "Over 95 million photos and videos are shared on Instagram daily! 🖼️",
    "Instagram Reels are watched by 45% of users weekly! 🎥",
    "The most-used filter on Instagram is Clarendon! 🌟",
    "Instagram's algorithm prioritizes content based on user engagement! 💬",
    "Businesses share 80% of their Instagram posts as photos! 📷",
    "The most popular emoji on Instagram is the heart emoji! ❤️",
    "Instagram influencers can earn up to $1 million per post! 💰",
    "The average Instagram post gets 10.7 hashtags! #️⃣",
    "Instagram ads reach over 1.2 billion people monthly! 📣",
    "The most popular time to post on Instagram is Wednesday at 11 AM! ⏰",
]
greeting_message = '''
Need to save an Instagram post? Just send the link, and I'll get it for you in seconds!

📌 What can I download?
✔️ Reels
✔️ Videos
✔️ Photos
✔️ Carousels

🚀 How to use:
1️⃣ Copy the Instagram post link 📋
2️⃣ Paste it here and send it 📩
3️⃣ Get your media instantly! 🎉

Let’s go—send me a link! 🎬🔥'''

router = Router()

class AdvMsg(StatesGroup):
    img = State()
    audio = State()
    txt = State()
    inline_link_name = State()
    inline_link_link = State()
    
class GroupMsg(StatesGroup):
    img = State()
    audio = State()
    txt = State()
    inline_link_name = State()
    inline_link_link = State()


INSTAGRAM_URL_REGEX = r"(https?:\/\/)?(www\.)?instagram\.com\/(reel|p)\/[\w-]+\/?"
pending_requests = set()

async def extract_shortcode(url):
        """
        Extract shortcode from various Instagram URL formats
        """
        # Regular expressions for different Instagram URL patterns
        patterns = [
            r'/(?:p|reel)/([A-Za-z0-9_-]+)',  # Matches both /p/ and /reel/
            r'shortcode=([A-Za-z0-9_-]+)',     # Matches shortcode parameter
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        # If no match found, raise error
        raise ValueError("Could not extract shortcode from URL")

def sync_download_single_post(url, id):
    """Synchronously download an Instagram post."""
    try:
        # Create a new Instaloader instance for each download
        L = instaloader.Instaloader(
            download_comments=False,
            save_metadata=False,
            download_video_thumbnails=False,
            filename_pattern="{shortcode}"
        )
        # Note: Not logging in here; assumes public posts
        shortcode = re.search(r'/(?:p|reel)/([A-Za-z0-9_-]+)', url).group(1)
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        download_dir = f"downloads{id}_{shortcode}_{uuid.uuid4()}"  # Unique directory
        os.makedirs(download_dir, exist_ok=True)
        L.download_post(post, target=download_dir)
        return download_dir
    except Exception as e:
        print(f"Error downloading single post: {e}")
        return None

async def download_single_post(url, id):
    """Async wrapper to run synchronous download in a thread."""
    loop = asyncio.get_running_loop()
    download_dir = await loop.run_in_executor(executor, sync_download_single_post, url, id)
    return download_dir
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
        await msg.answer(f"Send request first, Киньте запрос на подписку: {CHANNEL_LINK}", reply_markup=kb.subscribe_channel)
        return False

async def process_download(message: Message, x: Message):
    try:
        download_dir = await download_single_post(message.text, message.from_user.id)
        if download_dir is None:
            await message.answer("Error occurred: Could not download the post.")
            return

        # Send downloaded files
        for file in os.listdir(download_dir):
            file_path = os.path.join(download_dir, file)
            if file.endswith(".mp4"):
                reel = FSInputFile(file_path, filename=file)
                await message.answer_video(video=reel, caption="📥 Downloaded via @ReelyFastBot", reply_markup=kb.add_to_group)
                os.remove(file_path)
            elif file.endswith(".txt"):
                os.remove(file_path)
            elif file.endswith(".jpg"):
                img = FSInputFile(file_path, filename=file)
                await message.answer_photo(img, caption="📥 Downloaded via @ReelyFastBot")
                os.remove(file_path)

        # Clean up
        await x.delete()
        if os.path.isdir(download_dir):
            shutil.rmtree(download_dir)
    except Exception as e:
        await message.answer(f"An error occurred: {e}")
@router.chat_join_request()
async def handle_join_request(update: ChatJoinRequest):
    pending_requests.add(update.from_user.id)
    # Optionally notify admins or log the request

@router.my_chat_member()
async def handle_new_chat(update: ChatMemberUpdated):
    chat_id = update.chat.id
    await rq.set_group(chat_id)
    # Save chat_id to your database or list

@router.channel_post()
async def forward_channel_post(message: Message):
    """Forwards messages from the channel to a all users in bot, the channel you created to accept the requests 
    will be the target channel(posts from this channel will be listened and forwarded to all users)."""
    for user in await rq.get_all_user_ids():
        try:
            await bot.forward_message(from_chat_id=CHANNEL_ID,chat_id=user, message_id=message.message_id)
        except Exception as e:
            await message.answer(f"Unexpected error: {e}")

@router.message(CommandStart())
async def start(message:Message):
    await rq.set_user(tg_id=message.from_user.id)
    if not await subscription_check(message.from_user.id, message):
        return
    await message.answer(f"⚡ Welcome to {(await message.bot.get_me()).username}! ⚡" + greeting_message, reply_markup=kb.add_to_group)

@router.callback_query(F.data == "subchek")
async def subchek(callback: CallbackQuery, message: Message):
    if not await subscription_check(message.from_user.id, message):
        await callback.answer("Your not subscribed yet",)
        return
    await callback.answer("Your are okay to go")
@router.message(Command("narrator")) #// /narrator 123456, all users will recieve 123456
async def narrator(message: Message, command: CommandObject):
    for user in await rq.get_all_user_ids():
        await bot.send_message(chat_id=user, text=command.args)
@router.message(F.text.regexp(INSTAGRAM_URL_REGEX))
async def handle_instagram_reel(message: Message):
    if not await subscription_check(message.from_user.id, message):
        return
    x = await message.answer(f"✅ Instagram post detected! Did you know: {fact_list[randint(0, len(fact_list)-1)]}")
    # Start download as a background task
    asyncio.create_task(process_download(message, x))
    

@router.message(Command("send_to_all_users"))
async def start_send_to_all(message: Message, state: FSMContext):
    await state.set_state(AdvMsg.img)
    await message.answer("send your img🖼️\nIf no image then type none")


@router.message(AdvMsg.img)
async def ads_img(message: Message, state: FSMContext):
    if message.text:
        if message.text == "none":
            await state.set_state(GroupMsg.txt)
            await message.answer("send your text🗄️")
    photo_data = { "photo": message.photo }  # Ensure it's in dictionary format
    await state.update_data(img=message.photo[-1].file_id)
    await state.set_state(AdvMsg.txt)
    await message.answer("send your text🗄️")

@router.message(AdvMsg.txt)
async def ads_txt(message: Message, state: FSMContext):
    await state.update_data(txt=message.text)
    await state.set_state(AdvMsg.inline_link_name)
    await message.answer("send your inline_link name📛\n if no type none")

@router.message(AdvMsg.inline_link_name)
async def ads_lk_name(message: Message, state: FSMContext):
    await state.update_data(inline_link_name=message.text)
    await state.set_state(AdvMsg.inline_link_link)
    await message.answer("send your inline_link LINK🔗\n if no type none")

@router.message(AdvMsg.inline_link_link)
async def ads_final(message: Message, state: FSMContext):
    try:
        await state.update_data(inline_link_link=message.text)
        data = await state.get_data()
        new_inline_kb = kb.create_markap_kb(name=data['inline_link_name'], url=data['inline_link_link'])
        if new_inline_kb == None:
            for user in await rq.get_all_user_ids():
                if data['img']:
                    await bot.send_photo(chat_id=user, photo=data['img'],caption=data['txt'])
                elif data['audio']:
                    await bot.send_voice(chat_id=user, voice=data['audio'], caption=data["txt"])
                else:
                    await bot.send_message(chat_id=user, text=data['txt'])

        else:
            for user in await rq.get_all_user_ids():
                if data['img']:
                    await bot.send_photo(chat_id=user, photo=data['img'],caption=data['txt'], reply_markup=new_inline_kb)
                elif data['audio']:
                    await bot.send_voice(chat_id=user, voice=data['audio'], caption=data["txt"], reply_markup=new_inline_kb)
                else:
                    await bot.send_message(chat_id=user, text=data['txt'])

        await state.clear()
    except Exception as e:
        await message.answer(f"Got unexpected error, report to admin or just wait till update, the error:\n {e}")



@router.message(Command("send_to_all_groups"))
async def start_send_to_all_GroupMsg(message: Message, state: FSMContext):
    await state.set_state(GroupMsg.img)
    await message.answer("send your img🖼️\nIf no image then type none")


@router.message(GroupMsg.img)
async def ads_img_GroupMsg(message: Message, state: FSMContext):
    if message.text:
        if message.text == "none":
            await state.set_state(GroupMsg.txt)
            await message.answer("send your text🗄️")
    photo_data = { "photo": message.photo }  # Ensure it's in dictionary format
    await state.update_data(img=message.photo[-1].file_id)
    await state.set_state(GroupMsg.txt)
    await message.answer("send your text🗄️")

@router.message(GroupMsg.txt)
async def ads_txtGroupMsg(message: Message, state: FSMContext):
    await state.update_data(txt=message.text)
    await state.set_state(GroupMsg.inline_link_name)
    await message.answer("send your inline_link name📛\n if no type none")

@router.message(GroupMsg.inline_link_name)
async def ads_lk_nameGroupMsg(message: Message, state: FSMContext):
    await state.update_data(inline_link_name=message.text)
    await state.set_state(GroupMsg.inline_link_link)
    await message.answer("send your inline_link LINK🔗\n if no type none")

@router.message(GroupMsg.inline_link_link)
async def ads_finalGroupMsg(message: Message, state: FSMContext):
    try:
        await state.update_data(inline_link_link=message.text)
        data = await state.get_data()
        new_inline_kb = kb.create_markap_kb(name=data['inline_link_name'], url=data['inline_link_link'])
        if new_inline_kb == None:
            for user in await rq.get_all_groups_ids():
                if data['img']:
                    await bot.send_photo(chat_id=user, photo=data['img'],caption=data['txt'])
                elif data['audio']:
                    await bot.send_voice(chat_id=user, voice=data['audio'], caption=data["txt"])

        else:
            for user in await rq.get_all_groups_ids():
                if data['img']:
                    await bot.send_photo(chat_id=user, photo=data['img'],caption=data['txt'], reply_markup=new_inline_kb)
                elif data['audio']:
                    await bot.send_voice(chat_id=user, voice=data['audio'], caption=data["txt"], reply_markup=new_inline_kb)
                else:
                    await bot.send_message(chat_id=user, text=data['txt'])

        await state.clear()
    except Exception as e:
        await message.answer(f"Got unexpected error, report to admin or just wait till update, the error:\n {e}")

@router.message()
async def catch_all(message: Message):
    if not await subscription_check(message.from_user.id, message):
        return
    await message.answer("Pls send instagram url/link")
