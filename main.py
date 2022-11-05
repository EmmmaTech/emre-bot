import pydris
import traceback

client = pydris.Client("emre-bot", prefix="emre!")

@client.listen(lambda m: m.content.startswith("emre-bot"))
async def help_cmd(msg: pydris.Message):
    await client.send(f"Hello {msg.author}! My name is emre-bot, and my prefix is `emre!`.")

@client.command("hello")
async def hello(msg: pydris.Message):
    await client.send(f"Hello {msg.author}! How are you today?")

@client.command("bye")
async def bye(msg: pydris.Message):
    await client.send(f"Goodbye {msg.author}! See you later!")

@pydris.param("reason", pydris.StringParser())
@pydris.param("target", pydris.StringParser())
@client.command("ban")
async def ban(msg: pydris.Message, target: str, reason: str):
    await client.send(f"{msg.author} banned {target} because of {reason}!")

async def error_handler(msg: pydris.Message, err: Exception):
    formatted_tb = "".join(traceback.format_exception(type(err), err, err.__traceback__))
    await client.send(f"{msg.author} caused this error: \n```\n{formatted_tb}\n```")

for cmd in client.commands.values():
    error_handler = cmd.error(error_handler)

client.run()
