from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong, PeerIdInvalid
from info import ADMINS, LOG_CHANNEL, SUPPORT_CHAT, MELCOW_NEW_USERS
from database.users_chats_db import db
from database.ia_filterdb import Media
from utils import get_size, temp, get_settings
from Script import script
from pyrogram.errors import ChatAdminRequired

"""-----------------------------------------https://t.me/GetTGLink/4179 --------------------------------------"""

@Client.on_message(filters.new_chat_members & filters.group)
async def save_group(bot, message):
    r_j_check = [u.id for u in message.new_chat_members]
    if temp.ME in r_j_check:
        if not await db.get_chat(message.chat.id):
            total=await bot.get_chat_members_count(message.chat.id)
            r_j = message.from_user.mention if message.from_user else "Anonymous" 
            await bot.send_message(LOG_CHANNEL, script.LOG_TEXT_G.format(message.chat.title, message.chat.id, total, r_j))       
            await db.add_chat(message.chat.id, message.chat.title)
        if message.chat.id in temp.BANNED_CHATS:
            # Inspired from a boat of a banana tree
            buttons = [[
                InlineKeyboardButton('🌐ஆதரவு', url=f'https://t.me/MR_OTT_REQUEST')
            ]]
            reply_markup=InlineKeyboardMarkup(buttons)
            k = await message.reply(
                text='<b>அரட்டை அனுமதிக்கப்படவில்லை 🐞\n\nஎனது நிர்வாகிகள் என்னை இங்கு பணிபுரிய விடாமல் தடுத்துள்ளனர்! நீங்கள் அதைப் பற்றி மேலும் அறிய விரும்பினால், உரிமையாளரைத் தொடர்பு கொள்ளவும்...</b>',
                reply_markup=reply_markup,
            )

            try:
                await k.pin()
            except:
                pass
            await bot.leave_chat(message.chat.id)
            return
        buttons = [[
            InlineKeyboardButton('என்னை எப்படி பயன்படுத்துவது', url=f"https://t.me/{temp.U_NAME}?start=help"),
            InlineKeyboardButton('📢 என்னை எப்படி பயன்படுத்துவது 📢', url='https://t.me/MROTTTamilOffl')
        ]]
        reply_markup=InlineKeyboardMarkup(buttons)
        await message.reply_text(
            text=f"<b>›› என்னை உங்கள் குழுவில் சேர்த்ததற்கு நன்றி. {message.chat.title} ❣️\n›› என்னை நிர்வாகியாக்க மறக்காதே.\n›› என்னைப் பயன்படுத்துவதில் ஏதேனும் சந்தேகம் இருந்தால் கீழே உள்ள பொத்தானைக் கிளிக் செய்க..⚡⚡.</b>",
            reply_markup=reply_markup)
    else:
        settings = await get_settings(message.chat.id)
        if settings["welcome"]:
            for u in message.new_chat_members:
                if (temp.MELCOW).get('welcome') is not None:
                    try:
                        await (temp.MELCOW['welcome']).delete()
                    except:
                        pass
                temp.MELCOW['welcome'] = await message.reply_video(
                video="https://telegra.ph/file/03691465baa774e46506d.mp4",                                               
                                                 caption=f'<b>வண்ணகம், {u.mention} 👋🏻\nஎங்கள் குழுவிற்கு வரவேற்கிறோம் {message.chat.title}\n\n இந்த பாட் அல்லது குழு உங்கள் கல்வி நோக்கத்திற்காக உருவாக்கப்பட்டது. எனவே உங்கள் நண்பர்களுடன் பகிர்ந்து கொள்ளுங்கள் மற்றும் அறிவை அறிந்து கொள்ளுங்கள் 👍</b>',

                                                 reply_markup=InlineKeyboardMarkup( [ [ InlineKeyboardButton('🔥  ↭ பகிரவும் ↭  🔥', url='https://t.me/+Y92lcOFkdkIzZjll') ]

                                                                                    ] )

                )

@Client.on_message(filters.command('leave') & filters.user(ADMINS))
async def leave_a_chat(bot, message):
    if len(message.command) == 1:
        return await message.reply('Give me a chat id')
    chat = message.command[1]
    try:
        chat = int(chat)
    except:
        chat = chat
    try:
        buttons = [[
            InlineKeyboardButton('🌐ஆதரவு', url=f'https://t.me/MR_OTT_REQUEST')
        ]]
        reply_markup=InlineKeyboardMarkup(buttons)
        await bot.send_message(
            chat_id=chat,
            text='<<b>வணக்கம் நண்பர்களே, \nஎனது நிர்வாகி என்னை குழுவிலிருந்து வெளியேறச் சொன்னார், அதனால் நான் செல்கிறேன்! நீங்கள் என்னை மீண்டும் சேர்க்க விரும்பினால் எனது ஆதரவு குழுவை தொடர்பு கொள்ளவும்.</b>',
            reply_markup=reply_markup,
        )

        await bot.leave_chat(chat)
        await message.reply(f"left the chat `{chat}`")
    except Exception as e:
        await message.reply(f'Error - {e}')

@Client.on_message(filters.command('disable') & filters.user(ADMINS))
async def disable_chat(bot, message):
    if len(message.command) == 1:
        return await message.reply('Give me a chat id')
    r = message.text.split(None)
    if len(r) > 2:
        reason = message.text.split(None, 2)[2]
        chat = message.text.split(None, 2)[1]
    else:
        chat = message.command[1]
        reason = "காரணம் எதுவும் வழங்கப்படவில்லை"
    try:
        chat_ = int(chat)
    except:
        return await message.reply('சரியான அரட்டை ஐடியைக் கொடுங்கள்')
    cha_t = await db.get_chat(int(chat_))
    if not cha_t:
        return await message.reply("DB இல் அரட்டை இல்லை")
    if cha_t['is_disabled']:
        return await message.reply(f"இந்த அரட்டை ஏற்கனவே முடக்கப்பட்டுள்ளது:\nகாரணம்-<code> {cha_t['reason']} </code>")
    await db.disable_chat(int(chat_), reason)
    temp.BANNED_CHATS.append(int(chat_))
    await message.reply('அரட்டை வெற்றிகரமாக முடக்கப்பட்டது')
    try:
        buttons = [[
            InlineKeyboardButton('🌐ஆதரவ', url=f'https://t.me/MR_OTT_REQUEST')
        ]]
        reply_markup=InlineKeyboardMarkup(buttons)
        await bot.send_message(
            chat_id=chat_, 
            text=f'<b>வணக்கம் நண்பர்களே, \nஎனது நிர்வாகி என்னை குழுவிலிருந்து வெளியேறச் சொன்னார், அதனால் நான் செல்கிறேன்! நீங்கள் என்னை மீண்டும் சேர்க்க விரும்பினால் எனது ஆதரவு குழுவை தொடர்பு கொள்ளவும்.</b> \nகாரணம் : <code>{reason}</code>',
            reply_markup=reply_markup)
        await bot.leave_chat(chat_)
    except Exception as e:
        await message.reply(f"Error - {e}")


@Client.on_message(filters.command('enable') & filters.user(ADMINS))
async def re_enable_chat(bot, message):
    if len(message.command) == 1:
        return await message.reply('Give me a chat id')
    chat = message.command[1]
    try:
        chat_ = int(chat)
    except:
        return await message.reply('சரியான அரட்டை ஐடியைக் கொடுங்கள்')
    sts = await db.get_chat(int(chat))
    if not sts:
        return await message.reply("DB இல் அரட்டை இல்லை!")
    if not sts.get('is_disabled'):
        return await message.reply('இந்த அரட்டை இன்னும் முடக்கப்படவில்லை.')
    await db.re_enable_chat(int(chat_))
    temp.BANNED_CHATS.remove(int(chat_))
    await message.reply("Cஅரட்டை வெற்றிகரமாக மீண்டும் இயக்கப்பட்டது")


@Client.on_message(filters.command('stats') & filters.incoming)
async def get_ststs(bot, message):
    rju = await message.reply('புள்ளிவிவரங்களைப் பெறுகிறது..')
    total_users = await db.total_users_count()
    totl_chats = await db.total_chat_count()
    files = await Media.count_documents()
    size = await db.get_db_size()
    free = 536870912 - size
    size = get_size(size)
    free = get_size(free)
    await rju.edit(script.STATUS_TXT.format(files, total_users, totl_chats, size, free))


# a function for trespassing into others groups, Inspired by a Vazha
# Not to be used , But Just to showcase his vazhatharam.
# @Client.on_message(filters.command('invite') & filters.user(ADMINS))
async def gen_invite(bot, message):
    if len(message.command) == 1:
        return await message.reply('Give me a chat id')
    chat = message.command[1]
    try:
        chat = int(chat)
    except:
        return await message.reply('Give Me A Valid Chat ID')
    try:
        link = await bot.create_chat_invite_link(chat)
    except ChatAdminRequired:
        return await message.reply("அழைப்பு இணைப்பு உருவாக்கம் தோல்வியடைந்தது, எனக்கு போதுமான உரிமைகள் இல்லை")
    except Exception as e:
        return await message.reply(f'Errஉங்கள் அழைப்பு இணைப்பு இதோor {e}')
    await message.reply(f'Here is your Invite Link {link.invite_link}')

@Client.on_message(filters.command('ban') & filters.user(ADMINS))
async def ban_a_user(bot, message):
    # https://t.me/GetTGLink/4185
    if len(message.command) == 1:
        return await message.reply('எனக்கு ஒரு பயனர் ஐடி / பயனர் பெயரைக் கொடுங்கள்')
    r = message.text.split(None)
    if len(r) > 2:
        reason = message.text.split(None, 2)[2]
        chat = message.text.split(None, 2)[1]
    else:
        chat = message.command[1]
        reason = "காரணம் எதுவும் வழங்கப்படவில்லை"
    try:
        chat = int(chat)
    except:
        pass
    try:
        k = await bot.get_users(chat)
    except PeerIdInvalid:
        return await message.reply("இது தவறான பயனர், நான் அவரை இதற்கு முன்பு சந்தித்திருக்கிறீர்களா என்பதை உறுதிப்படுத்திக் கொள்ளுங்கள்.")
    except IndexError:
        return await message.reply("இது ஒரு சேனலாக இருக்கலாம், இது ஒரு பயனர் என்பதை உறுதிப்படுத்தவும்.")
    except Exception as e:
        return await message.reply(f'Error - {e}')
    else:
        jar = await db.get_ban_status(k.id)
        if jar['is_banned']:
            return await message.reply(f"{k.mention} ஏற்கனவே தடை செய்யப்பட்டுள்ளது\nகாரணம்: {jar['ban_reason']}")
        await db.ban_user(k.id, reason)
        temp.BANNED_USERS.append(k.id)
        await message.reply(f"வெற்றிகரமாக தடை செய்யப்பட்டது {k.mention}")


    
@Client.on_message(filters.command('unban') & filters.user(ADMINS))
async def unban_a_user(bot, message):
    if len(message.command) == 1:
        return await message.reply('எனக்கு ஒரு பயனர் ஐடி / பயனர் பெயரைக் கொடுங்கள்')
    r = message.text.split(None)
    if len(r) > 2:
        reason = message.text.split(None, 2)[2]
        chat = message.text.split(None, 2)[1]
    else:
        chat = message.command[1]
        reason = "காரணம் எதுவும் வழங்கப்படவில்ல"
    try:
        chat = int(chat)
    except:
        pass
    try:
        k = await bot.get_users(chat)
    except PeerIdInvalid:
        return await message.reply("இது தவறான பயனர், நான் அவரை இதற்கு முன்பு சந்தித்திருக்கிறீர்களா என்பதை உறுதிப்படுத்திக் கொள்ளுங்கள்.")
    except IndexError:
        return await message.reply("இது ஒரு சேனலாக இருக்கலாம், இது ஒரு பயனர் என்பதை உறுதிப்படுத்தவும்.")
    except Exception as e:
        return await message.reply(f'Error - {e}')
    else:
        jar = await db.get_ban_status(k.id)
        if not jar['is_banned']:
            return await message.reply(f"{k.mention} is not yet banned.")
        await db.remove_ban(k.id)
        temp.BANNED_USERS.remove(k.id)
        await message.reply(f"தடை நீக்கப்பட்டது {k.mention}")


    
@Client.on_message(filters.command('users') & filters.user(ADMINS))
async def list_users(bot, message):
    # https://t.me/GetTGLink/4184
    raju = await message.reply('பயனர்களின் பட்டியலைப் பெறுதல்')
    users = await db.get_all_users()
    out = "DB இல் சேமிக்கப்பட்ட பயனர்கள்:\n\n"
    async for user in users:
        out += f"<a href=tg://user?id={user['id']}>{user['name']}</a>"
        if user['ban_status']['is_banned']:
            out += '( Banned User )'
        out += '\n'
    try:
        await raju.edit_text(out)
    except MessageTooLong:
        with open('users.txt', 'w+') as outfile:
            outfile.write(out)
        await message.reply_document('users.txt', caption="List Of Users")

@Client.on_message(filters.command('chats') & filters.user(ADMINS))
async def list_chats(bot, message):
    raju = await message.reply('Getting List Of chats')
    chats = await db.get_all_chats()
    out = "DB இல் சேமிக்கப்பட்ட பயனர்கள்:\n\n"
    async for chat in chats:
        out += f"**Title:** `{chat['title']}`\n**- ID:** `{chat['id']}`"
        if chat['chat_status']['is_disabled']:
            out += '( Disabled Chat )'
        out += '\n'
    try:
        await raju.edit_text(out)
    except MessageTooLong:
        with open('chats.txt', 'w+') as outfile:
            outfile.write(out)
        await message.reply_document('chats.txt', caption="List Of Chats")
