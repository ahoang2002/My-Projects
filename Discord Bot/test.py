import discord
from discord.ext import commands
import tweepy
import os
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv('Discord_Token')
TWITTER_BEARER_TOKEN = os.getenv('Twitter_Bearer_Token')

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

