import requests
import json
import os

import discord
from discord import app_commands
from discord.ext import commands

from pprint import pprint

# Settings
discord_token = os.getenv("DISCORD_BOT_TOKEN")

koito_base_url = os.getenv("KOITO_BASEURL")
koito_api_url = koito_base_url + "/apis/web/v1"
koito_api_key = os.getenv("KOITO_APIKEY")
KOITO_AUTH_HEADER = {
    "Authorization": f"Token {koito_api_key}"
}

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='?', intents=intents)
tree = bot.tree

@bot.event
async def on_ready():
    print(f'logged in as {bot.user}')

@bot.command()
@commands.is_owner()
async def sync(ctx: commands.Context) -> None:
    """Sync commands"""
    synced = await ctx.bot.tree.sync()
    await ctx.send(f"Synced {len(synced)} commands globally")

@discord.app_commands.allowed_installs(guilds=True, users=True)
@discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@bot.hybrid_command(name="meow", description="Speak as a cat")
@app_commands.describe(message="thing to say")
async def meow(ctx: commands.Context, message: str):
    await ctx.send(message)

@discord.app_commands.allowed_installs(guilds=True, users=True)
@discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@bot.hybrid_command(name="fm", description="/fm for cats")
async def fm(ctx: commands.Context):
    result = get_current_track()

    print(result)

    itsover = result.get("itsover", False)
    is_playing = result.get("is_playing", False)
    title = result.get("title", "Unknown title")
    artist = result.get("artist", "Unknown Artist")
    albumid = result.get("albumid", "")
    imageurl = result.get("imageurl", "")

    if itsover == True:
        await ctx.send(f"[It's over.](https://i.ibb.co/v6sw4cp4/its-over.jpg)")
        return

    if is_playing != True:
        await ctx.send(f"<@!{ctx.author.id}> is not listening to anything.")
        return

    if albumid:
        r = requests.get(f"{koito_api_url}/album/{albumid}", headers=KOITO_AUTH_HEADER)
        data = r.json()

        album = data["title"] # bit messy to have this here instead of get_current_track(), but whatever.

        print(f"\nalbum id data\n{data}")
        listendata = f"{artist} • {album}"
        if album == None:
            listendata = f"{artist}"
    else:
        listendata = f"{artist}"

    embed=discord.Embed(title=f"{title}")
    embed.set_thumbnail(url=imageurl)
    embed.add_field(name=listendata, value="", inline=False)
    await ctx.send(embed=embed)

@discord.app_commands.allowed_installs(guilds=True, users=True)
@discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@bot.hybrid_command(name="me", description="perform action")
@app_commands.describe(action="thing to do")
async def me(ctx: commands.Context, action: str):
    await ctx.send(f"\\* <@!{ctx.author.id}> {action}")

def get_current_track():
    r = requests.get(f"{koito_api_url}/now-playing", headers=KOITO_AUTH_HEADER)
    if r.status_code == 200:
        data = r.json()
        if data["currently_playing"] != True:
            is_playing = False
            return locals()
        else:
            is_playing = data["currently_playing"]
            title = data["track"]["title"]
            artist = data["track"]["artists"][0]["name"]
            albumid = data["track"]["album_id"]
            imageurl = koito_base_url + data["track"]["image"]["large"]

            return locals()

    else:
        print(f"{koito_api_url}/now-playing")
        print(r.status_code)
        print("It's over")
        itsover = True
        return locals()

bot.run(discord_token)
