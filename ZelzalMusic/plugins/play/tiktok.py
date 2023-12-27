#▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒✯ ʑᴇʟᴢᴀʟ_ᴍᴜsɪᴄ ✯▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
#▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒✯  T.me/ZThon   ✯▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
#▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒✯ T.me/Zelzal_Music ✯▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
from os import remove
from requests import Session
import urllib.request as request
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery
from pyrogram.types import InlineKeyboardMarkup as Markup, InlineKeyboardButton as Button
from pyrolistener import Listener
from pyrolistener.exceptions import TimeOut
from ZelzalMusic import app
from ZelzalMusic.plugins.play.filters import command
from config import OWNER_ID

listener = Listener(app)
session = Session()
api = 'https://api.saidazim.uz/tiktok/'
turl = 'https://vm.tiktok.com/{id}'

caption = '''
- الاسـم : {nickname}
- اليـوزر : {username}
- العنـوان : {title}
- المشاهـدات : {views}
- اللايكـات : {likes}
- التعليقـات : {comments}
- المشاركـات : {shares}
'''

def downloadTiktok(url):
    params = {
        'url': url
    }
    res = session.get(api, params= params).json()
    if res.get('id') is None : return {'error' : '- - اووبـس .. رابـط غيـر صالـح ؟!'}
    _caption = caption.format(
        nickname = res['nickname'],
        username = res['username'],
        title = res['title'],
        views = res['view_count'],
        likes = res['like_count'],
        comments = res['comment_count'],
        shares = res['share_count']
    )
    return {
        'caption': _caption,
        'id': url.split('/')[3],
        'video': res['video']
    }

def downloadAudio(_id):
    url = turl.format(id=_id)
    params = {
        'url': url
    }
    res = session.get(api, params= params).json()
    audio = res['music']
    request.urlretrieve(audio, f'{_id}.mp3')


@app.on_message(command(['تيك', 'تيك توك'], ''))
async def reciveURL(_: Client, message: Message):
    try: ask = await listener.listen(
        chat_id = message.chat.id,
        from_id = message.from_user.id,
        text = '- ارسـل رابـط الفيـد مـن تيـك تـوك لـ تحميلـه ...',
        timeout = 30
    )
    except TimeOut: return await message.reply('- عـذراً .. انتهـى الوقت حـاول مجـدداً', reply_to_message_id = message.id)
    response = downloadTiktok(ask.text)
    if response.get('error'): return await ask.reply(response['error'])
    request.urlretrieve(response['video'], f'{response["id"]}.mp4')
    markup = Markup([
        [Button('تحميـل صـوت 🎙',f'adownload {response["id"]}')],
        [Button('مطـور البـوت ⛹🏻‍♂', user_id = OWNER_ID)]
    ])
    await ask.reply_video(video = f'{response["id"]}.mp4', caption = response['caption'], reply_markup = markup, reply_to_message_id = message.id)  
    remove(f'{response["id"]}.mp4')
    

@app.on_callback_query(filters.regex(r'^(adownload)'))
async def aDownload(_: Client, callback: CallbackQuery):
    _id = callback.data.split()[1]
    downloadAudio(_id)
    await callback.message.reply_audio(
        audio = f'{_id}.mp3',
        reply_to_message_id = callback.message.id
    )
    remove(f'{_id}.mp4')
