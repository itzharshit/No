### Copyright ©️ 2022 Amit Sharma <https://github.com/buddhhu>

import glob
import json
from importlib import import_module

from telethon.tl.types import InputMessagesFilterDocument

from bot import client, db, log

true, false, null = True, False, None


async def get_database():
    msg = await client.get_messages("me", search="#NoDM", limit=1)
    if msg.total == 0:
        mess = json.dumps(db.template, ensure_ascii=False, indent=1)
        msg = await client.send_message("me", f"#NoDM\n\n\n{mess}")
    else:
        msg = msg[0]
        db.cache.update(eval(msg.text.replace("#NoDM", "").strip()))
    return msg.id


async def get_approved_list():
    msg = await client.get_messages(
        "me",
        search="approved-list.txt",
        filter=InputMessagesFilterDocument(),
        limit=1,
    )
    if msg.total == 0:
        open("approved-list.txt", "w").write("{}")
        msg = await client.send_file(
            "me", "approved-list.txt", caption="List of approved users."
        )
    else:
        msg = msg[0]
        file = await msg.download_media()
        db.cache["approved"] = eval(open(file, "r").read())
    db.cache["approved-id"] = msg.id


db.cache["database-id"] = client.loop.run_until_complete(get_database())
client.loop.run_until_complete(get_approved_list())



for plugins in glob.glob("bot/plugins/*.py"):
    import_module(plugins[:-3].replace("/", "."))


log.info("Started")
client.run_until_disconnected()
