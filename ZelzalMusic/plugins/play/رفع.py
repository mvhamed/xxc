import asyncio
import os
import time
import requests
import aiohttp
import json
from pyrogram import Client, filters
from pyrogram.enums import ChatMembersFilter
from pyrogram import enums
from pyrogram import filters
from pyrogram import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from strings.filters import command
from ZelzalMusic import (Apple, Resso, SoundCloud, Spotify, Telegram, YouTube, app)
from ZelzalMusic import app
from asyncio import gather
from pyrogram.errors import FloodWait



@app.on_message(filters.command("تفعيل", ""))
def update_owners(client, message):
    chat_id = str(message.chat.id)
    Toom = message.from_user
    tom_owners = load_tom_owners()
    tom_admin = load_tom_admin()
    chat_i = message.chat.id
    owner_id = None
    admins = app.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS)
    admins_id = [str(admin.user.id) for admin in admins if not admin.user.is_bot]
    if chat_id not in tom_admin['admin']:
        tom_admin['admin'][chat_id] = {'admin_id': admins_id}
    else:
        existing_admins = tom_admin['admin'][chat_id]['admin_id']
        new_admins = [admin_id for admin_id in admins_id if admin_id not in existing_admins]
        tom_admin['admin'][chat_id]['admin_id'].extend(new_admins)

    dump_tom_admin(tom_admin)
    count = len(new_admins)
    message.reply_text(f"""◍ تم تفعيل الجروب بواسطة [{Toom.first_name}](tg://user?id={Toom.id})\n\n◍ وتمت اضافة {count} مستخدمين الى الادمن
√""")
    
    for member in client.get_chat_members(chat_i, filter=enums.ChatMembersFilter.ADMINISTRATORS):
        if member.status == enums.ChatMemberStatus.OWNER:
            owner_id = str(member.user.id)
            tooom = member.user
            break
    
    if owner_id is not None:
        if chat_id not in tom_owners['owners']:
            tom_owners['owners'][chat_id] = {'owner_id': [owner_id]}
        else:
            existing_owners = tom_owners['owners'][chat_id]['owner_id']
            if owner_id not in existing_owners:
                tom_owners['owners'][chat_id]['owner_id'].append(owner_id)

        dump_tom_owners(tom_owners)
        message.reply_text(f"""◍ تم تفعيل الجروب بواسطة [{Toom.first_name}](tg://user?id={Toom.id})\n\n◍ وتم رفع [{tooom.first_name}](tg://user?id={tooom.id}) مالك للمجموعة 
√""")
    else:
        message.reply_text("لا يوجد مالك في الدردشة.")



@app.on_message(filters.new_chat_photo)
async def caesarphoto(client, message):
    chat_id = message.chat.id
    photo = await client.download_media(message.chat.photo.big_file_id)
    await client.send_photo(chat_id=chat_id, photo=photo, caption=f"حلوه صوره الجروب الجديده \n الشخص الي غيرها ده{message.from_user.mention}")

@app.on_message(filters.command(["الحسابات المحذوفه"], "") & filters.group, group=5)
async def list_bots(client: Client, message: Message):
    chat_member = await client.get_chat_member(message.chat.id, message.from_user.id)
    if chat_member.status not in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
        return
    count = 0 
    async for member in client.get_chat_members(message.chat.id):
        if member.user.is_deleted:
            count += 1

    if count > 0:
        await message.reply_text(f"عدد الأعضاء الذين لديهم حسابات محذوفة في المجموعة: {count}")
    else:
        await message.reply_text("لا يوجد أعضاء لديهم حسابات محذوفة في المجموعة.")
