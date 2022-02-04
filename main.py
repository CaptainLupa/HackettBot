from discord.ext import commands
import discord
import os
from dotenv import load_dotenv
import random
from youtube_dl import YoutubeDL
from requests import get
import asyncio

load_dotenv()
H_TOKEN = os.getenv('HACKETT_TOKEN')

intents = discord.Intents.all()

hackett = commands.Bot(command_prefix="!", intents=intents)


def search(query):
    with YoutubeDL({'format': 'bestaudio', 'noplaylist': 'True'}) as ydl:
        try:
            get(query)
        except:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
        else:
            info = ydl.extract_info(query, download=False)
    return info, info['formats'][0]['url']


@hackett.command(name="join", help="joins voice channel")
async def join(ctx):
    if ctx.author.voice is None:
        await ctx.send(f'{ctx.author.name} is not connected to a vc')
        return

    await ctx.author.voice.channel.connect()


@hackett.command(name='leave',  help="leaves")
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client is not None:
        await voice_client.disconnect()
    else:
        await ctx.send("Hackett is not connected to a voice channel.")


@hackett.command(name='play', help='plays a song')
async def play(ctx, *, query):
    FFMPEG_OPTS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    video, source = search(query)

    voice = discord.utils.get(hackett.voice_clients, guild=ctx.guild)

    if voice is None:
        await join(ctx)
    await ctx.send(f"Now playing {video['title']}")

    voice.play(discord.FFmpegPCMAudio(source, **FFMPEG_OPTS), after=lambda e: print("done", e))
    voice.is_playing()


@hackett.command(name='pause')
async def pause(ctx):
    vc = ctx.message.guild.voice_client
    if vc is not None and vc.is_playing():
        await vc.pause()
    else:
        await ctx.send("Hackett is not playing anything atm.")


@hackett.command(name='resume')
async def resume(ctx):
    vc = ctx.message.guild.voice_client
    if vc.is_paused():
        await vc.resume()
    else:
        await ctx.send("Hackett was not playing anything before this. Use play command")


@hackett.command(name="stop")
async def stop(ctx):
    vc = ctx.message.guild.voice_client
    if vc.is_playing():
        await vc.stop()
    else:
        await ctx.send("Hackett is not playing anything at the moment.")


async def is_jagraj(ctx):
    return ctx.author.id != 526162219197661216


@hackett.event
async def on_ready():
    print("Hackett is ready to ping some doors")


@hackett.command(name="quirkedup", help="You know what it does.")
async def quirkedup(ctx):
    await ctx.send(f"<@!{ctx.author.id}> is definitely a quirked up white boy, and he is most certainly busting it down"
                   f" sexual style, but is he goated with the sauce?")


@hackett.command(name="ping", help="Pings the closest door")
async def ping(ctx):
    d = [
        f'Hey <@!{ctx.author.id}>, door here.',
        'Door here!',
        'Door over here!',
        f'Door here, <@!{ctx.author.id}>!'
    ]
    await ctx.send(random.choice(d))


@hackett.command(name="kick", help="Kicks the mentioned user")
@commands.check(is_jagraj)
async def kick(ctx, user: str):
    guild = ctx.guild
    user = guild.get_member(user_id=int(user.strip('<@!>')))
    if user.voice is not None:
        await user.move_to(None)


@hackett.command(name="hackettpics", help="Sends you a saucy hackettpics")
async def porn(ctx):
    f = open('hackett_default.png', mode='rb')
    df = discord.File(fp=f)
    await ctx.send(file=df)


@hackett.command(name="rename", help="Changes someone's nickname")
@commands.check(is_jagraj)
async def rename(ctx, usr: str, *newNick):
    n = ""
    for c in newNick:
        n += c + " "
    n = n.strip()
    usr = ctx.guild.get_member(user_id=int(usr.strip('<@!>')))
    await usr.edit(nick=n)


@hackett.command(name="getid")
async def getid(ctx, usr):
    await ctx.send(ctx.guild.get_member(user_id=int(usr.strip('<@!>'))).id)


@hackett.command(name="move", help="Use '-' instead of space in channel name")
@commands.check(is_jagraj)
async def move(ctx, usr: str, *ch):
    chan = ""
    for c in ch:
        chan += c + " "

    chan = chan.strip()

    for channel in ctx.guild.channels:
        if channel.name == chan:
            break
    else:
        await ctx.send(f"No channel named {chan}")
        return

    usr = ctx.guild.get_member(user_id=int(usr.strip('<@!>')))
    await usr.move_to(channel=channel)


@hackett.command(name='chinfo', help="get info about specific channel")
async def chinfo(ctx, ch: str):
    for channel in ctx.guild.channels:
        if channel.name == ch:
            break
    else:
        await ctx.send(f"No channel named {ch}")
        return

    f = "\n - ".join(["Name: " + channel.name, str(channel.category), str(channel.id), "Members:\n    - " + "\n    - ".join([x.name for x in channel.members])])
    await ctx.send(f)


@hackett.command(name="niglet")
async def nig(ctx):
    await ctx.send(f"<@!{ctx.author.id}> is black")

hackett.run(H_TOKEN)
