import os
import uuid
import shutil
import logging
from pyrogram import Client, filters
from creds import Credentials
from telegraph import upload_file

logging.basicConfig(level=logging.INFO)


TGraph = Client(
    "Image upload bot",
    bot_token=Credentials.BOT_TOKEN,
    api_id=Credentials.API_ID,
    api_hash=Credentials.API_HASH,
)


@TGraph.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        f"Hello!! <code>{message.from_user.first_name}</code>,\nI Am Telegraph Image Uploader Bot\n\n🎨 I can only upload photos\n🤖 This Bot Comes Under @ParaboyMirror ❤️",
        True,
    )

@TGraph.on_message(filters.command("help"))
async def start(client, message):
    await message.reply_text(
        f"You just need to send the photo here,\nand the bot will upload it to Telegraph",
        True,
    )

@TGraph.on_message(filters.photo)
async def getimage(client, message):
    tmp = os.path.join("downloads", str(message.chat.id))
    if not os.path.isdir(tmp):
        os.makedirs(tmp)
    img_path = os.path.join(tmp, str(uuid.uuid4()) + ".jpg")
    dwn = await message.reply_text("📥 Downloading...", True)
    img_path = await client.download_media(message=message, file_name=img_path)
    await dwn.edit_text("📤 Uploading...")
    try:
        response = upload_file(img_path)
    except Exception as error:
        await dwn.edit_text(f"Oops something went wrong\n{error}")
        return
    await dwn.edit_text(f"https://telegra.ph{response[0]}")
    shutil.rmtree(tmp, ignore_errors=True)


TGraph.run()
