import discord
import aiohttp
import asyncio
import os
import re
import tweepy
from urllib.parse import urlparse
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

def is_twitter_link(url):
    parsed = urlparse(url)
    return parsed.netloc.endswith(('twitter.com', 'x.com', 't.co'))

DISCORD_TOKEN = os.getenv('Discord_Token')
TWITTER_BEARER_TOKEN = os.getenv('Twitter_Bearer_Token')
DISCORD_CHANNEL_ID = 1371264562132815875  
TWITTER_USERNAME = 'andrew20020'    
KEYWORDS = ['Details', 'Sunday'] 

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)
twitter_client = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN)
bot = commands.Bot(command_prefix='!', intents=intents)

last_tweet_id = None  

async def fetch_latest_tweets():
    global last_tweet_id
    headers = {
        'Authorization': f'Bearer {TWITTER_BEARER_TOKEN}'
    }

    params = {
        'tweet.fields': 'created_at,entities',
        'max_results': 5,
        'exclude': 'retweets,replies'
    }

    url = f'https://api.twitter.com/2/users/by/username/{TWITTER_USERNAME}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            user_data = await resp.json()
            # print("User lookup response:", user_data)
            user_id = user_data['data']['id']

        tweet_url = f'https://api.twitter.com/2/users/{user_id}/tweets'
        async with session.get(tweet_url, headers=headers, params=params) as resp:
            tweets = await resp.json()
            # print(tweets)
            # Gathering tweet info
            for tweet in tweets.get('data', []):
                tweet_id = tweet['id']
                text = tweet['text']
                entities = tweet.get('entities', {})
                # print(entities)

                # Get rid of tailing URL's at the end of text, then append the actual link found in entities to the end of tweet text
                urls = entities.get('urls', [])
                external_url = None
                for url_data in urls:
                    expanded_url = url_data.get('expanded_url', '') 
                    if not is_twitter_link(expanded_url):
                        external_url = expanded_url
                        break

                text = re.sub(r'https://t\.co/\S+', '', text).strip()

                if external_url:
                    text += f"\n{external_url}"
                
                # Output tweet text
                if last_tweet_id is None or int(tweet_id) > int(last_tweet_id):
                    if any(keyword.lower() in text.lower() for keyword in KEYWORDS):
                        channel = bot.get_channel(DISCORD_CHANNEL_ID)
                        await channel.send(f"{text}")
                    # If tweet has photo attachment also get it and output in discord
                    try:
                        response = twitter_client.get_tweet(
                                tweet_id,
                                expansions="attachments.media_keys",
                                media_fields="url,type"
                            )
                        media = response.includes.get("media", [])
                        if media:
                            for i, item in enumerate(media):
                                if item.type == "photo":
                                    image_url = item.url

                        embed = discord.Embed()
                        embed.set_image(url=image_url)
                        await channel.send(embed=embed)
                    except Exception as e:
                        print("No image")

                last_tweet_id = max(last_tweet_id or 0, int(tweet_id))

#Command to output overall Sunny Sunday Schedule
@bot.command()
async def sunnysunday(ctx):
    image_path = "./Discord Bot/SunnySunday.png"
    with open(image_path, "rb") as file:
        picture = discord.File(file)
        await ctx.send("Here is the Sunny Sunday schedule:", file=picture)

        
@bot.event
async def on_ready():
    print(f'Logged in as {client.user}')
    while True:
        try:
            await fetch_latest_tweets()
        except Exception as e:
            print(f"Error fetching tweets: {e}")
        await asyncio.sleep(600)  # Check every 10 mins

bot.run(DISCORD_TOKEN)