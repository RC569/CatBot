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
koito_api_url = "/apis/web/v1"
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
    is_playing, title, artist, imageurl, = get_current_track() # add a check for if these actually show up

    if is_playing != True:
        await ctx.send(f"<@!{ctx.author.id}> is not listening to anything.")
        return

    embed=discord.Embed()
    embed.set_thumbnail(url=imageurl)
#    embed.add_field(name=f"{title}", value=f"{artist} • {album}", inline=False) # TODO - can be grabbed through /apis/web/v1/album/["track"]["album_id"]
    embed.add_field(name=f"{title}", value=f"{artist}", inline=False)
    await ctx.send(embed=embed)

@discord.app_commands.allowed_installs(guilds=True, users=True)
@discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@bot.hybrid_command(name="me", description="perform action")
@app_commands.describe(action="thing to do")
async def me(ctx: commands.Context, action: str):
    await ctx.send(f"\\* <@!{ctx.author.id}> {action}")

def get_current_track():
    r = requests.get(f"{koito_base_url}{koito_api_url}/now-playing", headers=KOITO_AUTH_HEADER)
    if r.status_code == 200:
        data = r.json()
        if data["currently_playing"] != True:
            is_playing = False
            title = None # annoying
            artist = None # annoying
            imageurl = None # annoying
            return is_playing, title, artist, imageurl
        else:
            is_playing = data["currently_playing"]
            title = data["track"]["title"]
            artist = data["track"]["artists"][0]["name"]
            imageurl = koito_base_url + data["track"]["image"]["large"]
    
            pprint(data)
            return is_playing, title, artist, imageurl

    else:
        print(f"{koito_base_url}{koito_api_url}/now-playing")
        print(r.status_code)
        print("It's over")

bot.run(discord_token)
