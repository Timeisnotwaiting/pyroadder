from pyrogram import Client as Alpha, filters
from pyrogram.types import Message
from config import *
from sqldb import *
import time
import datetime 
from pyrogram.errors import FloodWait
import asyncio

LOG = -750989577

Alf = Alpha("yashu-alpha", api_id = API_ID, api_hash = API_HASH, session_string = STRING_SESSION)

@Alf.on_message(filters.command("send", "!"))
async def sned(_, m):
    if not str(m.from_user.id) in SUDO:
        return
    text = m.text.split(None, 1)[1]
    await _.send_message(m.chat.id, text)

@Alf.on_message(filters.command("get_common", "!"))
async def gs(_, m):
    if not str(m.from_user.id) in SUDO:
        return 
    id = int(m.text.split()[1])
    if id == m.chat.id:
        return await m.reply("😑😑")
    SCAM = []
    try:
        async for i in _.get_chat_members(id):
            SCAM.append(i.user.id)
    except Exception as e:
        await m.reply(e)
    UMM = []
    try:
        async for l in _.get_chat_members(m.chat.id):
            UMM.append(l.user.id)
    except Exception as e:
        await m.reply(e)
    SCAMMERS = []
    for scam in SCAM:
        for umm in UMM:
            if scam == umm:
                SCAMMERS.append(umm)
                break
    msg = ""
    for scammer in SCAMMERS:
        sn = (await _.get_users(scammer)).mention
        msg += f"\n{sn}"
    await m.reply(msg)

@Alf.on_message(filters.command("addall", "!"))
async def add(_, m):
    global SUDO
    l = m.chat.id
    try:
        me = (await _.get_me())
        myid = me["user_id"]
        SUDO.append(myid)
    except:
        pass
    if not str(m.from_user.id) in SUDO:
        return
    try:
        await m.delete()
    except:
        pass
    try:
        id = int(m.text.split(None, 1)[1])
    except:
        return await _.send_message(m.chat.id, "provide only group id !")
    if str(id)[0] != "-":
        return await m.reply("⚠️ provide valid group id !")
    ok = await m.reply("➕ adding users from given group id !")
    if m.chat.type == "private":
        return await ok.edit("try this command in groups !")
    MEM = []
    async for mem in _.get_chat_members(id):
        if (not mem.user.is_bot and not mem.user.is_deleted):
            MEM.append(mem.user.id)

    a = 0
    b = 0
    for lnk in MEM:
        try:
            await _.add_chat_members(l, lnk)
            a += 1
            await ok.edit(f"Scrap status :-\n\nList appended :- {len(MEM)}\n\nAdded :- {a}\nFailed :- {b}\n\nFor error, check logs")
            time.sleep(2)
        except Exception as ea:
            b += 1
            await ok.edit(f"Scrap status :-\n\nList appended :- {len(MEM)}\n\nAdded :- {a}\nFailed :- {b}\n\nFor error, check logs")
            pass
        if a == 30:
            break
    
    a = str(a)
    await ok.delete()
    await _.send_message(l, f"Scrap status :-\n\nList appended :- {len(MEM)}\n\nAdded :- {a}\nFailed :- {b}\n\nFor error, check logs")
    time.sleep(10)
    await ok.delete()

@Alf.on_message(filters.command("checkdb", "!"))
async def checker(_, m):
    if not str(m.from_user.id) in SUDO:
        return
    ok = await m.reply("Checking database... ♻️")
    time.sleep(2)
    list = getdb()
    try:
        await m.delete()
    except:
        pass
    await ok.edit(f"<code>Users on db: {len(list)}</code>")

@Alf.on_message(filters.command("addtodb", "!"))
async def add_to_db(_, m):
    if not str(m.from_user.id) in SUDO:
        return
    try:
        await m.delete()
    except:
        pass
    try:
        id = int(m.text.split(None, 1)[1])
    except:
        return await _.send_message(m.chat.id, "provide only group id !")
    if str(id)[0] != "-":
        return await m.reply("⚠️ provide valid group id !")
    ok = await m.reply("➕ adding users to database from given group id !")
    if m.chat.type == "private":
        await ok.edit("try this command in groups !")
    MEM = []
    async for mem in _.get_chat_members(id):
        if (not mem.user.is_bot and not mem.user.is_deleted):
            MEM.append(mem.user.id)
    a = 0
    b = 0
    for meme in MEM:
        try:
            add(meme)
            a += 1
        except Exception as e:
            b += 1
            await ok.edit(e)
            break
    await m.reply(f"{a} users added to db, {b} failed !")


@Alf.on_message(filters.command("scrapdb", "!"))
async def dbs(_, m):
    if not str(m.from_user.id) in SUDO:
        return
    if m.chat.type == "private":
        await m.delete()
        return await m.reply("try this command in groups !")
    try:
        await m.delete()
    except:
        pass
    ok = await m.reply("♻️ checking database... ⏳⌛️")
    time.sleep(2)
    try:
        list = getdb()
    except:
        await ok.edit("Can't connect to database !")
    if len(list) == 0:
        await ok.edit("Database is empty ! 🫙")
        time.sleep(5)
        return await ok.delete()
    await ok.edit(f"Found {len(list)} users on Database... !")
    time.sleep(2)
    a = 0
    b = 0
    for lk in list:
        try:
            await _.add_chat_members(m.chat.id, lk)
            a += 1
            pop(lk)
        except:
            b += 1
            pop(lk)
            pass
        time.sleep(2)
        if a == 20:
            break
    await ok.edit(f"Scrap status :- \n\nAdded : {a}\n\nFailed : {b}")
            
@Alf.on_message(filters.command("add", "!"))
async def test(_, m):
        if not str(m.from_user.id) in SUDO:
            return 
        try:
            add(int(m.text.split()[1]))
            await m.reply("working 🤧 !")
            await m.delete()
        except Exception as e:
            await m.reply(f"db problem 🤧\n\nError :- {e}")
            await m.delete()

@Alf.on_message(filters.command("join", "!"))
async def join(_, m):
    if not str(m.from_user.id) in SUDO:
        return
    get_text = m.text.split()
    id_u = get_text[1]
    try:
        await _.join_chat(id_u)
        await m.reply("Joined successfully... 😌✨💫")
    except Exception as e:
        await m.reply(e)

async def eor(_, m, t):
    try:
        await m.edit(t)
    except:
        await m.reply(t)

@Alf.on_message(filters.command("backup", "$"))
async def back(_, m):
    if not m.from_user.is_self:
        return
    if str(m.chat.id)[0] == "-":
        return await eor(_, m, "Only can backup private chats...")
    await eor(_, m, "Backing up chat.....")
    ch = _.get_chat_history(m.chat.id)
    MSG_ID = []
    await eor(_, m, f"{len(MSG_ID)} messages found...")
    ok = await m.reply("forwarding messages....")
    async for i in ch:
        MSG_ID.append(i.id)
    b = 0
    a = 0
    n = len(MSG_ID)//50
    for id in MSG_ID:
        try:
            await _.forward_messages(LOG, m.chat.id, id)
            a += 1
            b += 1
        except FloodWait as e:
            flood_time = 20
            if flood_time > 200:
                continue
            await ok.edit(f"sleeping for {flood_time}s..")
            await asyncio.sleep(flood_time)
        if n == a:
            try:
                await ok.edit(f"{b} messages backed up.....")
            except:
                pass
            a = 0
    return await eor(_, m, "all msges backed up successfully...")
        

if YA == "YashuAlpha":
    Alf.run()
    print("Pyro adder started successfully 🇮🇳🎊🎉")
else:
    print("password you entered is wrong")
