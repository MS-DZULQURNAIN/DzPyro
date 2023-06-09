# Copas Teriak Copas MONYET
# Gay Teriak Gay Anjeng
# @Rizzvbss | @Kenapanan
# Kok Bacot
# © @KynanSupport
# FULL MONGO NIH JING FIX MULTI CLIENT



import os
import sys
from re import sub
import asyncio
from time import time
from pyrogram import Client, filters, enums
from pyrogram.errors import ChatAdminRequired
from pyrogram.types import ChatPermissions, ChatPrivileges, Message
from . import *
from ubotlibs.ubot.helper.basic import eor
from .profile import extract_user, extract_userid
from DzText.text import dz, no_adm, repp, pross, usernf, rea
from DzText.text import ban_1, ban_2, ban_3, ban_4, ban_5, unban_1, unban_2, unban_3
from DzText.text import pin_1, pin_2, unpin_1, mute_1, mute_2, mute_3, mute_4, mute_5, unmute_1
from DzText.text import kick_1, kick_2, kick_3, kick_4, kick_5, prmt, full_prmt, dmt_1, dmt_2

admins_in_chat = {}

unmute_permissions = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_polls=True,
    can_change_info=False,
    can_invite_users=True,
    can_pin_messages=False,
)

async def list_admins(client: Client, chat_id: int):
    global admins_in_chat
    if chat_id in admins_in_chat:
        interval = time() - admins_in_chat[chat_id]["last_updated_at"]
        if interval < 3600:
            return admins_in_chat[chat_id]["data"]

    admins_in_chat[chat_id] = {
        "last_updated_at": time(),
        "data": [
            member.user.id
            async for member in client.get_chat_members(
                chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS
            )
        ],
    }
    return admins_in_chat[chat_id]["data"]


async def extract_user_and_reason(message, sender_chat=False):
    args = message.text.strip().split()
    text = message.text
    user = None
    reason = None
    if message.reply_to_message:
        reply = message.reply_to_message
        if not reply.from_user:
            if (
                reply.sender_chat
                and reply.sender_chat != message.chat.id
                and sender_chat
            ):
                id_ = reply.sender_chat.id
            else:
                return None, None
        else:
            id_ = reply.from_user.id

        if len(args) < 2:
            reason = None
        else:
            reason = text.split(None, 1)[1]
        return id_, reason

    if len(args) == 2:
        user = text.split(None, 1)[1]
        return await extract_userid(message, user), None

    if len(args) > 2:
        user, reason = text.split(None, 2)[1:]
        return await extract_userid(message, user), reason

    return user, reason

@Client.on_message(filters.command(["setpg"], cmds) & filters.me)
async def set_chat_photo(client: Client, message: Message):
    zuzu = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    can_change_admin = zuzu.can_change_info
    can_change_member = message.chat.permissions.can_change_info
    if not (can_change_admin or can_change_member):
        await message.reply(f"{no_adm}")
    if message.reply_to_message:
        if message.reply_to_message.photo:
            await client.set_chat_photo(
                message.chat.id, photo=message.reply_to_message.photo.file_id
            )
            return
    else:
        await message.edit(f"{repp}")



@Client.on_message(filters.command(["ban", "dban"], cmds) & filters.me)
async def member_ban(client: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message, sender_chat=True)
    ky = await message.reply(f"`{pross}`")
    if not user_id:
        return await message.edit(f"{usernf}")
    if user_id == client.me.id:
        return await message.edit(f"{ban_1}")
    if user_id in DEVS:
        return await message.edit(f"{ban_2}")
    if user_id in (await list_admins(client, message.chat.id)):
        return await message.edit(f"{ban_3}")
    try:
        await ky.delete()
        mention = (await client.get_users(user_id)).mention
    except IndexError:
        mention = (
            message.reply_to_message.sender_chat.title
            if message.reply_to_message
            else "Anon"
        )
    if message.command[0][0] == "d":
        await message.reply_to_message.delete()
    msg = f"{dz}\n\n<b>{ban_4}</b> {mention}\n<b>{ban_5}</b> {message.from_user.mention}\n"
    if reason:
        msg += f"<b>{rea}</b> {reason}"
    try:
        await message.chat.ban_member(user_id)
        await message.edit(msg)
    except ChatAdminRequired:
        return await message.edit(f"**{no_adm}**")



@Client.on_message(filters.command(["unban"], cmds) & filters.me)
async def member_unban(client: Client, message: Message):
    reply = message.reply_to_message
    zz = await message.reply(f"`{pross}`")
    if reply and reply.sender_chat and reply.sender_chat != message.chat.id:
        return await message.edit(f"{unban_1}")

    if len(message.command) == 2:
        user = message.text.split(None, 1)[1]
    elif len(message.command) == 1 and reply:
        user = message.reply_to_message.from_user.id
    else:
        return await message.edit(
            f"{unban_2}"
        )
    try:
        await message.chat.unban_member(user)
        await asyncio.sleep(0.1)
        await zz.delete()
        umention = (await client.get_users(user)).mention
        await message.edit(f"{dz}\n\n{unban_3} {umention}")
    except ChatAdminRequired:
        return await message.edit(f"**{no_adm}**")



@Client.on_message(filters.command(["pin", "unpin"], cmds) & filters.me)
async def pin_message(client: Client, message):
    if not message.reply_to_message:
        return await message.reply(f"{pin_1}")
    await message.edit(f"`{pross}`")
    r = message.reply_to_message
    if message.command[0][0] == "u":
        await r.unpin()
        return await message.edit(
            f"{dz}\n\n**{unpin_1}({r.link})**",
            disable_web_page_preview=True,
        )
    try:
        await r.pin(disable_notification=True)
        await message.edit(
            f"{dz}\n\n**{pin_2}({r.link})**",
            disable_web_page_preview=True,
        )
    except ChatAdminRequired:
        return await message.edit(f"**{no_adm}**")


@Client.on_message(filters.command(["mute"], cmds) & filters.me)
async def mute(client: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message)
    nay = await message.reply(f"`{pross}`")
    if not user_id:
        return await message.edit(f"{usernf}")
    if user_id == client.me.id:
        return await message.edit(f"{mute_1}")
    if user_id in DEVS:
        return await message.edit(f"{mute_2}")
    if user_id in (await list_admins(client, message.chat.id)):
        return await message.edit(f"{mute_3}")
    await nay.delete()
    mention = (await client.get_users(user_id)).mention
    msg = (
        f"{dz}\n\n**{mute_4}** {mention}\n"
        f"**{mute_5}** {message.from_user.mention if message.from_user else 'Anon'}\n"
    )
    if reason:
        msg += f"**{rea}** {reason}"
    try:
        await message.chat.restrict_member(user_id, permissions=ChatPermissions())
        await message.edit(msg)
    except ChatAdminRequired:
        return await message.edit(f"**{no_adm}**")



@Client.on_message(filters.command(["unmute"], cmds) & filters.me)
async def unmute(client: Client, message: Message):
    user_id = await extract_user(message)
    kl = await message.reply(f"`{pross}`")
    if not user_id:
        return await message.edit(f"{usernf}")
    try:
        await message.chat.restrict_member(user_id, permissions=unmute_permissions)
        await kl.delete()
        umention = (await client.get_users(user_id)).mention
        await message.edit(f"{dz}\n\n{unmute_1} {umention}")
    except ChatAdminRequired:
        return await message.edit(f"**{no_adm}**")


@Client.on_message(filters.command(["kick", "dkick"], cmds) & filters.me)
async def kick_user(client: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message)
    ny = await message.reply(f"`{pross}`")
    if not user_id:
        return await message.edit(f"{usernf}")
    if user_id == client.me.id:
        return await message.edit(f"{kick_1}")
    if user_id == DEVS:
        return await message.edit(f"{kick_2}")
    if user_id in (await list_admins(client, message.chat.id)):
        return await message.edit(f"{kick_3}")
    await ny.delete()
    mention = (await client.get_users(user_id)).mention
    msg = f"""
{dz}

**{kick_4}** {mention}
**{kick_5}** {message.from_user.mention if message.from_user else 'Anon'}"""
    if message.command[0][0] == "d":
        await message.reply_to_message.delete()
    if reason:
        msg += f"\n**{rea}** `{reason}`"
    try:
        await message.chat.ban_member(user_id)
        await message.edit(msg)
        await asyncio.sleep(1)
        await message.chat.unban_member(user_id)
    except ChatAdminRequired:
        return await message.edit(f"**{no_adm}**")


@Client.on_message(
    filters.group & filters.command(["promote", "fullpromote"], cmds) & filters.me
)
async def promotte(client: Client, message: Message):
    user_id = await extract_user(message)
    biji = await message.reply(f"`{pross}`")
    if not user_id:
        return await message.edit(f"{usernf}")
    rd = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    try: 
        if message.command[0][0] == "f":
            await message.chat.promote_member(
                user_id,
                privileges=ChatPrivileges(
                    can_manage_chat=True,
                    can_delete_messages=True,
                    can_manage_video_chats=True,
                    can_restrict_members=True,
                    can_change_info=True,
                    can_invite_users=True,
                    can_pin_messages=True,
                    can_promote_members=True,
                ),
            )
            await asyncio.sleep(1)
            await biji.delete()
            umention = (await client.get_users(user_id)).mention
            return await message.edit(f"{dz}\n\n{full_prmt} {umention}")

        await message.chat.promote_member(
            user_id,
            privileges=ChatPrivileges(
                can_manage_chat=True,
                can_delete_messages=True,
                can_manage_video_chats=True,
                can_restrict_members=True,
                can_change_info=False,
                can_invite_users=True,
                can_pin_messages=True,
                can_promote_members=False,
            ),
        )
        await asyncio.sleep(1)
        await biji.delete()
        umention = (await client.get_users(user_id)).mention
        await message.edit(f"{dz}\n\n{prmt} {umention}")
    except ChatAdminRequired:
        return await message.edit(f"**{no_adm}**")


@Client.on_message(
    filters.group
    & filters.command(["cdemote"], ["."])
    & filters.user(DEVS)
    & ~filters.me
)
@Client.on_message(filters.group & filters.command(["demote"], cmds) & filters.me)
async def demote(client: Client, message: Message):
    user_id = await extract_user(message)
    sempak = await message.reply(f"`{pross}`")
    if not user_id:
        return await message.edit(f"{usernf}")
    if user_id == client.me.id:
        return await message.edit(f"{dmt_1}")
    await message.chat.promote_member(
        user_id,
        privileges=ChatPrivileges(
            can_manage_chat=False,
            can_delete_messages=False,
            can_manage_video_chats=False,
            can_restrict_members=False,
            can_change_info=False,
            can_invite_users=False,
            can_pin_messages=False,
            can_promote_members=False,
        ),
    )
    await asyncio.sleep(1)
    await sempak.delete()
    umention = (await client.get_users(user_id)).mention
    await message.edit(f"{dz}\n\n{dmt_2} {umention}")


add_command_help(
    "admin",
    [
        [f"ban [reply/username/userid]", "Ban pengguna dari group"],
        [f"unban [reply/username/userid]", "Unban pengguna dari group",],
        [f"kick [reply/username/userid]", "kick pengguna dari group"],
        [f"promote `atau` .fullpromote [reply/username/userid]","Promote pengguna sebagai admin",],
        [f"demote [reply/username/userid]", "Demote pengguna member"],
        [f"mute [reply/username/userid]","Mute pengguna dari group",],
        [f"unmute [reply/username/userid]","Unmute pengguna dari group",],
        [f"pin [reply pesan]","Pin sebuah pesan",],
        [f"unpin [reply pesan]","Unpin sebuah pesan",],
        [f"setpg [reply ke foto]","pasang poto profil group",],
    ],
)
