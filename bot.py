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
koito_now_playing = "/apis/web/v1/now-playing"
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
    saythis = get_current_track(ctx.author.id)
    await ctx.send(saythis)

@discord.app_commands.allowed_installs(guilds=True, users=True)
@discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@bot.hybrid_command(name="me", description="perform action")
@app_commands.describe(action="thing to do")
async def me(ctx: commands.Context, action: str):
    await ctx.send(f"\\* <@!{ctx.author.id}> {action}")

@discord.app_commands.allowed_installs(guilds=True, users=True)
@discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@bot.hybrid_command(name="embedtest", description="perform action")
async def embedtest(ctx: commands.Context):
    title = "Song title"
    artist = "Artist name"
    album = "Album name"
    embed=discord.Embed()
    embed.set_thumbnail(url="https://placehold.co/500x500.png")
    embed.add_field(name=f"{title}", value=f"{artist} • {album}", inline=False)
    await ctx.send(embed=embed)

def get_current_track(author):
    r = requests.get(koito_base_url + koito_now_playing, headers=KOITO_AUTH_HEADER)
    if r.status_code == 200:
        data = r.json()
        if data["currently_playing"] != True:
            saythis = f"<@!{author}> is not listening to anything."
            print(saythis)
            return saythis
        
        title = data["track"]["title"]
        artist = data["track"]["artists"][0]["name"]

        pprint(data)
        saythis = f"<@!{author}> is listening to **{title}** by **{artist}**"
        print(saythis)
        return saythis
    else:
        print("It's over")

bot.run(discord_token)
