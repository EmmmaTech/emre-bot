import pydris
import traceback

client = pydris.Client("emre-bot", prefix="emre!")

def command_signature(cmd: pydris.Command) -> str:
    base = f"{cmd.name}"

    if cmd.aliases:
        base += f"({', '.join(cmd.aliases)})"

    for arg in cmd.args:
        flag = "--" if arg.flag else ""
        default = f"={arg.default}" if arg.default is not None else ""
        short = f"|{flag}{arg.short}" if arg.short and arg.short != arg.name else ""

        if not arg.required:
            base += f" [{flag}{arg.name}{short}{default}]"
        else:
            base += f" {flag}{arg.name}{short}"

    return base

@pydris.param("cmd", pydris.StringParser(), required=False)
@client.command("help", description="Sends all of the commands or details on a specific command.")
async def help(_: pydris.Message, cmd: str | None):
    if cmd is not None:
        command = client.commands.get(cmd)

        if command is None:
            return await client.send(f"There is no command with the name {cmd}.")

        helpmsg = f"```\n**{', '.join([command.name] + command.aliases)}**\n"

        if command.description:
            helpmsg += f"\n{command.description}\n"

        helpmsg += f"Usage: {client.prefix}{command_signature(command)}\n```"
        return await client.send(helpmsg)

    helpmsg = "```\nCommands:\n"
    helpmsg += "\n".join([f"{name:<10} {cmd.description or ''}" for (name, cmd) in client.commands.items()])
    helpmsg += "\n```"
    return await client.send(helpmsg)

@client.command("hello", description="Says hello")
async def hello(msg: pydris.Message):
    await client.send(f"Hello {msg.author}! How are you today?")

@client.command("bye", description="Says bye")
async def bye(msg: pydris.Message):
    await client.send(f"Goodbye {msg.author}! See you later!")

@client.command("die_kys", description="Please do not kill me :(")
async def die_kys(_: pydris.Message):
    await client.send(f"Fu-")

@pydris.param("reason", pydris.StringParser(), required=False)
@pydris.param("target", pydris.StringParser())
@client.command("ban", description="Bans a person.")
async def ban(msg: pydris.Message, target: str, reason: str | None):
    if msg.author.lstrip("Bridge-").lower() in ("sham", "same"):
        return await client.send(f"You cannot use this command. Reason: you're unbased.")

    resp = f"{msg.author} banned {target}!"
    if reason is not None:
        resp = resp.rstrip("!") + f" because of {reason}!"

    await client.send(resp)

async def error_handler(msg: pydris.Message, err: Exception):
    formatted_tb = "".join(traceback.format_exception(type(err), err, err.__traceback__))
    await client.send(f"{msg.author} caused this error: \n```\n{formatted_tb}\n```")

for cmd in client.commands.values():
    error_handler = cmd.error(error_handler)

client.run()
