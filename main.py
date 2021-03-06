from resources import register as last_r
import format_msg as last_f
import collage as last_c

from io import BytesIO
from PIL import Image

import discord
from discord import NotFound
from discord.ext import commands

with open("resources/keys.txt", "r") as f:
    LASTFM_KEY = f.readline().split("=")[1].strip("\n")
    DISCORD_KEY = f.readline().split("=")[1].strip("\n")

PREFIX = "$"
INTENTS = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, intents=INTENTS)

@bot.event
async def on_ready():
    print(f"logged in as {bot.user}")

@bot.command()
async def register(ctx):
    message_text = last_f.strip_command(PREFIX, ctx.message.content, "register")
    message_text = last_f.strip_double_spaces(message_text)
    last_r.register(str(ctx.message.author.id), message_text)
    await ctx.message.channel.send(f"Registered <@{ctx.message.author.id}> as {message_text}.")

@bot.command()
async def collage(ctx):
    message_text = last_f.strip_command(PREFIX, ctx.message.content, "collage")
    message_text = last_f.strip_double_spaces(message_text)
    timeframe, message_text = last_f.strip_timeframe(message_text)
    size, username = last_f.get_size_username(message_text)

    print(username)
    username = username.replace("<@", "")
    username = username.replace("!", "")
    username = username.replace(">", "")
    print(username)
    if username.isdigit():
        check = last_r.id_to_username(username)
        if check:
            username = check
    print(username)

    username = last_f.validate_username(username, LASTFM_KEY)
    quality = 95

    if size is None:
        size = 7
    elif size > 25:
        size = 25
    elif size < 1:
        size = 1

    if timeframe is None:
        timeframe = "overall"
    if username is None:
        await ctx.message.channel.send("Invalid username.")
        return

    try:
        collage = last_c.collage(username, timeframe, LASTFM_KEY, size=size)
    except IndexError:
        await ctx.message.channel.send("Not enough user data; try a smaller collage size.")
        return

    image_binary = BytesIO()
    collage.save(image_binary, 'JPEG', quality=quality, optimize=True, progressive=True)
    while image_binary.tell() > 8000000:
        quality -= 5
        print(image_binary.tell())
        image_binary = BytesIO()
        collage.save(image_binary, 'JPEG', quality=quality, optimize=True, progressive=True)
    image_binary.seek(0)
    await ctx.message.channel.send(file=discord.File(fp=image_binary, filename='image.png'))

@bot.command()
async def colour_collage(ctx):
    message_text = last_f.strip_command(PREFIX, ctx.message.content, "collage")
    message_text = last_f.strip_double_spaces(message_text)
    timeframe, message_text = last_f.strip_timeframe(message_text)
    size, username = last_f.get_size_username(message_text)

    username = username.replace("<@", "")
    username = username.replace("!", "")
    username = username.replace(">", "")
    if username.isdigit():
        username = last_r.id_to_username(username)

    username = last_f.validate_username(username, LASTFM_KEY)
    quality = 95

    if size is None:
        size = 7
    elif size > 25:
        size = 25
    elif size < 1:
        size = 1

    if timeframe is None:
        timeframe = "overall"
    if username is None:
        await ctx.message.channel.send("Invalid username.")
        return

    try:
        collage = last_c.collage(username, timeframe, LASTFM_KEY, size=size, hue=True)
    except IndexError:
        await ctx.message.channel.send("Not enough user data; try a smaller collage size.")
        return

    image_binary = BytesIO()
    collage.save(image_binary, 'JPEG', quality=quality, optimize=True, progressive=True)
    while image_binary.tell() > 8000000:
        quality -= 5
        print(image_binary.tell())
        image_binary = BytesIO()
        collage.save(image_binary, 'JPEG', quality=quality, optimize=True, progressive=True)
    image_binary.seek(0)
    await ctx.message.channel.send(file=discord.File(fp=image_binary, filename='image.png'))

if __name__ == "__main__":
    bot.run(DISCORD_KEY)
