from discord.ext import commands
from dotenv import load_dotenv
import os
import random
import json
import discord
import requests
from bs4 import BeautifulSoup

load_dotenv()

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.messages = True
intents.members = True
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)
bot.help_command = commands.DefaultHelpCommand(no_category="Commands")

def scrape_urls(state=None):
    r = requests.get(f"https://battleforthehill.com/states/{state}/elections")
    print(r.status_code)
    soup = BeautifulSoup(r.content, "html.parser")
    vals = soup.find_all("div", class_="bg-gray-900 border border-gray-800 ring-4 ring-gray-500 ring-offset-2 ring-offset-gray-200 rounded shadow")
    sen1 = None
    sen2 = None
    gov = []
    hou1 = None
    hou2 = None

    if vals:
        trs = vals[0].table.tbody.find_all('tr')
        if trs:
            tds = trs[0].find_all('td')
            if tds[1].get_text(strip=True) == "Active":
                sen1 = tds[2].a["href"]

        trs = vals[1].table.tbody.find_all('tr')
        if trs:
            tds = trs[0].find_all('td')
            if tds[1].get_text(strip=True) == "Active":
                gov.append(tds[2].a["href"])

        trs = vals[2].table.tbody.find_all('tr')
        if trs:
            tds = trs[0].find_all('td')
            if tds[1].get_text(strip=True) == "Active":
                sen2 = tds[2].a["href"]

        trs = vals[3].table.tbody.find_all('tr')
        if trs:
            tds = trs[0].find_all('td')
            if tds[1].get_text(strip=True) == "Active":
                hou1 = tds[2].a["href"]

        trs = vals[4].table.tbody.find_all('tr')
        if trs:
            tds = trs[0].find_all('td')
            if tds[1].get_text(strip=True) == "Active":
                hou2 = tds[2].a["href"]

    return sen1, sen2, gov, hou1, hou2


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


@bot.command()
async def findurl(ctx, state: int = None):
    if state is None:
        await ctx.send("Please provide a state number.")
        return

    sen1, sen2, gov, hou1, hou2 = scrape_urls(state)
    urls = {
        "Senate 1": sen1,
        "Senate 2": sen2,
        "Governor": gov,
        "House 1": hou1,
        "House 2": hou2
    }

    response = f"**URLs for State {state}:**\n\n"
    for key, value in urls.items():
        if value:
            response += f"{key}: {value}\n"
        else:
            response += f"{key}: N/A\n"

    await ctx.send(response)

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
    response += f"Polls Left: {d2:.2f}%\n"
    response += f"Percentage Needed in Every Poll: {f2:.2f}%"

    await ctx.send(response)

bot.run(os.getenv('BOT_TOKEN'))
