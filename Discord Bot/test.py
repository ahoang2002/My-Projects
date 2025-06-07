import discord
from discord.ext import commands
import tweepy
import os

# # --- Twitter API Setup ---
# # Replace these with your actual keys
DISCORD_TOKEN = 'MTM3MDU2MTI3ODUxMDIzNTY5OQ.GuQM6G.INJNekLmeG0ggX6q8xQv1LoaZ38S9jt3OmZVws'
TWITTER_BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAF9J1wEAAAAAe1Nur1Pp7EL8bPseQItvzUd7vQQ%3DZwb2rSZoXLKJicXhGmgJjC9I4wbOszz3xUfKafz1AABvp2N7M0'

twitter_client = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN)

# --- Discord Bot Setup ---
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

# # --- Run the Bot ---
@bot.command()
async def tweet(ctx):
    response = twitter_client.get_tweet(1928659204350382139, expansions=["author_id"])
    tweet_text = response.data.get('text', 'No text found.')
    await ctx.send(f"{tweet_text}")

@bot.command()
async def image(ctx):
    response = twitter_client.get_tweet(
    1928659204350382139,
    expansions="attachments.media_keys",
    media_fields="url")

    media = response.includes.get("media", [])
    if media:
        for i, item in enumerate(media):
            if item.type == "photo":
                image_url = item.url

    embed = discord.Embed()
    embed.set_image(url=image_url)
    await ctx.send(embed=embed)

@bot.command()
async def sunnysunday(ctx):
    image_path = "./Discord Bot/SunnySunday.png"
    with open(image_path, "rb") as file:
        picture = discord.File(file)
        await ctx.send("Here is the Sunny Sunday schedule:", file=picture)

@bot.event
async def on_ready():
    print("Bot started")
bot.run(DISCORD_TOKEN)

