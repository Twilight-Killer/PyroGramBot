import io
import sys
import traceback
from contextlib import redirect_stdout
from subprocess import getoutput as run
from pyrogram import filters
from pyrogram import Client 

from MyTgBot import bot, get_readable_time, StartTime

from datetime import datetime



async def aexec(code, client, message):
    exec(
        "async def __aexec(client, message): "
        + "".join(f"\n {l_}" for l_ in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)


@bot.on_message(filters.command(["run","eval"],["?","!",".","*","/","$",]))
async def eval(client, message):
    if message.from_user.id !=1666544436:
         return await message.reply_text("`You Don't Have Enough Rights To Run This!`")
    if len(message.text.split()) <2:
          return await message.reply_text("`Input Not Found!`")
    status_message = await message.reply_text("Processing ...")
    cmd = message.text.split(None, 1)[1]
    start = datetime.now()
    reply_to_ = message
    if message.reply_to_message:
        reply_to_ = message.reply_to_message

    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None

    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()

    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"
    end = datetime.now()
    ping = (end-start).microseconds / 1000
    final_output = "<b>📎 Input</b>: "
    final_output += f"<code>{cmd}</code>\n\n"
    final_output += "<b>📒 Output</b>:\n"
    final_output += f"<code>{evaluation.strip()}</code> \n\n"
    final_output += f"<b>✨ Taken Time</b>: {ping}<b>ms</b>"
    if len(final_output) > 4096:
        with io.BytesIO(str.encode(final_output)) as out_file:
            out_file.name = "eval.text"
            await reply_to_.reply_document(
                document=out_file, caption=cmd, disable_notification=True
            )
    else:
        await status_message.edit_text(final_output)


@bot.on_message(filters.command(["sh","shell"],["?","!",".","*","/","$",]))
async def sh(client, message):
    if message.from_user.id !=1666544436:
         return await message.reply_text("`You Don't Have Enough Rights To Run This!`")
         await message.reply_text("`No Input Found!`")
    else:
          code = message.text.replace(message.text.split(" ")[0], "")
          x = run(code)
          string = f"**📎 Input**: `{code}`\n\n**📒 Output **:\n`{x}`"
          try:
             await message.reply_text(string) 
          except Exception as e:
              with io.BytesIO(str.encode(string)) as out_file:
                 out_file.name = "shell.text"
                 await message.reply_document(document=out_file, caption=e)

async def aexec(code, client, message):
    exec(
        "async def __aexec(client, message): "
        + "".join(f"\n {l_}" for l_ in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)


@bot.on_message(filters.command("ping"))
async def ping(_, message):
     start_time = time.time()
     end_time = time.time()
     ping_time = round((end_time - start_time) * 1000, 5)
     uptime = get_readable_time((time.time() - StartTime))
     await message.edit(f"👾 **System Uptime & Ping**\n=> 🔔 **Ping**: {ping_time}\n=> ⬆️ **Uptime**: {uptime}")
