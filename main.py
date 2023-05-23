from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv
import os 
import random
import json
import discord
import requests
from bs4 import BeautifulSoup

load_dotenv()

intents = Intents.default()
intents.typing = False
intents.presences = False
intents.messages = True
intents.members = True
intents = discord.Intents.default() 
intents.message_content = True 

bot = commands.Bot(command_prefix='$', intents=intents)

bot.help_command = commands.DefaultHelpCommand(no_category="Commands")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')

@bot.command()
async def bot_help(ctx):
    """Show what President Benjamin Franklin can do."""
    help_menu = """
    **Help Menu**
    - `$hello`:                Say hello to President Benjamin Franklin.
    - `$quote`:                Get a random quote from Benjamin Franklin.
    - `$roll [sides]`:   Roll a dice with the specified number of sides (2-10).
    - `$calculate1 [A2] [B2]`: Calculate results based on provided values of GOP Aggregate and Polls Left in the Last Hour.
    - `$calculate2 [A2] [B2]`: Calculate results based on provided values of GOP Aggregate and Polls Completed.
    """
    await ctx.send(help_menu)

@bot.command()
async def quote(ctx):
    with open('quotes.json', 'r') as file:
        quotes = json.load(file)
    random_quote = random.choice(quotes)['text']
    await ctx.send(random_quote)
    await ctx.message.delete()


@bot.command()
async def roll(ctx, sides: int):
    if sides < 2 or sides > 10:
        await ctx.send("Please provide a number between 2 and 10 for the sides of the die.")
        return
    
    result = random.randint(1, sides)
    await ctx.send(f"You rolled a {result} on a {sides}-sided die!")

@bot.command()
async def calculate1(ctx, a2: float, b2: float):
    c2 = a2 * (((b2 * 7.5) + 70) / 100)
    d2 = 50 - c2
    percentage_needed = round(d2 / (100 - ((b2 * 7.5) + 70)) * 100, 2)
    c2_percentage = round(c2, 2)
    d2_percentage = round(d2, 2)
    
    response = f"**Results**:\n\n"
    response += f"Current # of Votes Secured: {c2_percentage}%\n"
    response += f"Total # of Votes Needed: {d2_percentage}%\n"
    response += f"Percentage Needed in Every Poll: {percentage_needed}%"
    
    await ctx.send(response)


@bot.command()
async def calculate2(ctx, a2: float, b2: float):
    c2 = (b2 * 70) / 92
    d2 = a2 * (c2 / 100)
    e2 = 50 - d2
    f2 = e2 / (100 - c2) * 100
    
    response = "**Results:**\n"
    response += f"Percent of Vote In: {c2:.2f}%\n"
    response += f"Current Number of Vote Secured: {d2:.2f}%\n"
    response += f"Number of Vote Needed: {e2:.2f}%\n"
    response += f"Percent of Vote Needed in Every Remaining Polls: {f2:.2f}%"
    
    await ctx.send(response)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

bot.run(os.getenv('BOT_TOKEN'))