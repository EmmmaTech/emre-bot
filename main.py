import asyncio
import pydris

client = pydris.Client("emre-bot", prefix="emre!")

@client.listen(lambda m: m.content.startswith("emre-bot"))
async def help_cmd(msg: pydris.Message):
    await client.send(f"Hello {msg.author}! My name is emre-bot, and my prefix is `emre!`.")

client.run()
