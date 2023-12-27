#▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒✯ ʑᴇʟᴢᴀʟ_ᴍᴜsɪᴄ ✯▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
#▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒✯  T.me/ZThon   ✯▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
#▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒✯ T.me/Zelzal_Music ✯▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
import os
import requests
import urllib.request
from bs4 import BeautifulSoup
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery
from pyrogram.types import InlineKeyboardMarkup as Markup, InlineKeyboardButton as Button

from ZelzalMusic import app
from ZelzalMusic.plugins.play.filters import command

headers = {
    'Accept-language': 'en',
    'User-Agent': 'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) '
                  'Version/4.0.4 Mobile/7B334b Safari/531.21.102011-10-16 20:23:10'
}

def download_video(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    link = soup.find('link', {'rel': 'canonical'}).attrs['href']
    video_id = link.split('/')[-1:][0]
    request_url = f'https://api.tiktokv.com/aweme/v1/feed/?aweme_id={video_id}'
    response = requests.get(request_url, headers=headers)
    try:
        video_link = response.json()['aweme_list'][0]['video']['play_addr']['url_list'][2]
        urllib.request.urlretrieve(video_link, 'out.mp4')
        return 'out.mp4'
    except IndexError:
        return False


@app.on_message(command(["/tt", "تيك", "/tiktok"]))
async def reciveURL(client, message: Message):
    query = " ".join(message.command[1:])
    m = await message.reply_text("<b>⇜ جـارِ التحميل ▬▭ . . .</b>")
    if query and ("tiktok.com" in query):
        if download_video(query):
            await message.reply_video(
                video='out.mp4',
                caption=f"𖡃 ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ ʙʏ @{app.username} ",
            )
            await m.delete()
