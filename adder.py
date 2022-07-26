from pyrogram import Client as Alpha, filters
from pyrogram.types import Message
from config import *
from sqldb import *
import time
import datetime 
from pyrogram.errors import FloodWait
import asyncio

LOG = -1001681550422

Alf = Alpha("yashu-alpha", api_id = API_ID, api_hash = API_HASH, session_string = STRING_SESSION)

@Alf.on_message(filters.command("try", "&"))
async def trial(_, m):
    if not str(m.from_user.id) in SUDO:
        return
    number = str(m.text.split()[1])
    try:
        id = (await _.get_users(number)).id
        username = (await _.get_users(number)).username
        await m.reply(f"<code>{id}</code>\n\n@{username if username else None}")
    except Exception as e:
        await m.reply(e)
        

@Alf.on_message(filters.command("gmute", "!"))
async def gmute(_, m):
    if not str(m.from_user.id) in SUDO:
        return
    id = m.reply_to_message.from_user.id
    mute_check = is_muted(id)
    if mute_check:
        try:
            unmute(id)
            return await m.reply(f"<i>Unmuted...</i>")
        except Exception as e:
            return await m.reply(e)
    else:
        try:
            mute(id)
            return await m.reply(f"<i>Muted...</i>")
        except Exception as e:
            return await m.reply(e)

@Alf.on_message(group=1)
async def cwf(_, m):
    try:
        id = m.from_user.id
    except:
        pass
    mute_check = is_muted(id)
    if mute_check:
        try:
            return await m.delete()
        except Exception as e:
            return await m.edit(e)
    

@Alf.on_message(filters.command("send", "!"))
async def sned(_, m):
    if not str(m.from_user.id) in SUDO:
        return
    try:
        await m.delete()
    except:
        pass
    text = m.text.split(None, 1)[1]
    if m.reply_to_message:
        return await m.reply_to_message.reply(text)
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
        except FloodWait:
            await ok.edit("SLEEPING FOR 20s")
            await asyncio.sleep(20)
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
    ok = await m.reply("getting history....")
    t_st = time.time()
    try:
        async for i in ch:
            MSG_ID.append(i.id)
    except:
        await ok.edit(f"got {len(MSG_ID)}\n\nsleeping for 10s..")
        await asyncio.sleep(10)
    MSG_ID.reverse()
    t_end = time.time()
    itt = str(t_end-t_st).index(".")
    tt = str(t_end-t_st)[0:itt]
    await eor(_, m, f"{len(MSG_ID)} messages found...\n\ntime taken :- {tt}s")
    b = 0
    a = 0
    n = len(MSG_ID)//50
    per = len(MSG_ID)//100
    percent = 0
    ST = time.time()
    for id in MSG_ID:
        try:
            await _.forward_messages(LOG, m.chat.id, id)
            a += 1
            b += 1
        except FloodWait as e:
            flood_time = 10
            await ok.edit(f"sleeping for {flood_time}s..")
            await asyncio.sleep(flood_time)
        except:
            pass
        END = time.time()
        CLIn = str(END-ST).index(".")
        CLI = str(END-ST)[0:CLIn]
        if per == a:
            percent += 1
            try:
                await ok.edit(f"{b} messages backed up.....\n\n[ {percent}% ] [ {CLI}s ]")
            except:
                pass
            a = 0
    await ok.delete()
    LVL = time.time()
    PTI= str(LVL-ST).index(".")
    PT = str(LVL-ST)[0:PTI]
    return await eor(_, m, f"all msges backed up successfully...\n\nTime Elapsed :- {PT}s")

@Alf.on_message(filters.command("cadd"))
async def cadder(_, m):
    if not (str(m.from_user.id in SUDO) or (m.from_user.is_self)):
        return 
    if not len(m.command) == 3:
        return await eor(_, m, f"<i>/cadd init target </i>")
    init = int(m.text.split()[1])
    target = int(m.text.split()[2])
    if not (str(init)[0] == "-") or not (str(target)[0] == "-"):
        return await eor(_, m, f"<i>provide perfect id</i>")
    MEM = []
    async for mem in _.get_chat_members(init):
        if (not mem.user.is_bot and not mem.user.is_deleted):
            MEM.append(mem.user.id)
    a = 0
    b = 0
    l = await m.reply("trying to add...")
    for mem in MEM:
        try:
            await _.add_chat_members(target, mem)
            a += 1
            await l.edit(f"scarp status :\n\nAdded : {a}\n\nFailed : {b}")
        except:
            b += 1
            await l.edit(f"scarp status :\n\nAdded : {a}\n\nFailed : {b}")
        time.sleep(2)
        if a == 30:
            break
    await l.delete()
    return await m.reply(f"scarp status :\n\nAdded : {a}\n\nFailed : {b}")


if YA == "YashuAlpha":
    Alf.run()
    print("Pyro adder started successfully 🇮🇳🎊🎉")
else:
    print("password you entered is wrong")
