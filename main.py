from discord.ext import commands
import discord
import os
from dotenv import load_dotenv

load_dotenv()
H_TOKEN = os.getenv('HACKETT_TOKEN')

intents = discord.Intents.default()
intents.members = True

hackett = commands.Bot(command_prefix="!", intents=intents)


@hackett.command(name="ping", help="Pings the closest door")
async def ping(ctx):
    await ctx.send("Door here.")


@hackett.command(name="kick", help="Kicks the mentioned user")
async def kick(ctx, user: str):
    guild = ctx.guild
    user = guild.get_member(user_id=int(user.strip('<@!>')))
    if user.voice is not None:
        await user.move_to(None)


@hackett.command(name="hackettpics", help="Sends you a saucy hackettpics")
async def porn(ctx):
    f = open('unknown.png', mode='rb')
    df = discord.File(fp=f)
    await ctx.send(file=df)

hackett.run(H_TOKEN)
