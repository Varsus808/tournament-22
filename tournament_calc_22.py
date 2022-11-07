import functools
import typing
import requests
import urllib.parse
import time
import sys
# bot.py
import os

import discord
from dotenv import load_dotenv

banned_list= [
'Banned Cards',
'Ancient Tomb',
'Animate Dead',
'Ashnod´s Altar',
'Basalt Monolith',
'Bazaar of Bagdad',
'Channel',
'Cranial Plating',
'Dance of the Dead',
'Demonic Consultation',
'Demonic Tutor',
'Diamaond Valley',
'Enlightened Tutor',
'Force of Will',
'Goblin Lakey',
'Goblin Recruiter',
'Hermit Druid',	
'High Tide',
'Hymn to Tourach',
'Imperial Recruiter',
'Isochrom Scepter',
'Karakas',
'Krark-Clan Ironworks',
'Library of Alexandria',
'Loyal Retainers',
'Mana Drain',
'Maze of Ith',
'Mystical Tutor',
'Necomancy',
'Personal Tutor',
'Power Artifact',
'Rystic Study',
'Shadowborn Apostle',
'Sink hole',
'Skull Clamp',
'Sol Ring',
'Strip Mine',
'Sword oft the Meek',	
'Sylvan Library',
'Sylvan Tutor',
'Tinker',
'Transmute Artifact',
'Vampiric Tutor',
'Waste Land',
'Worldly Tutor',
]



load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
	print(f'{client.user} has connected to Discord!')

@client.event
async def on_member_join(member):
	await member.create_dm()
	await member.dm_channel.send(
		f'Hi {member.name}, welcome to the Un+Common Tournament 2022 server!\nIf you want your Deck checked, please respond with just post your Decklist unchanged the MTGO Format!!!'
	)

def simplify_line(string):
	out_str = string
	if '\n' in out_str:
		out_str = out_str[:-1]
	return ' '.join(out_str.split(' ')[1:])


def deckcheck(decklist):
	base_url = "https://api.scryfall.com/cards/search?q=" + urllib.parse.quote("(r:u or r:c) -(set:sunf OR set:unf OR set:und OR set:ust OR set:unh OR set:ugl)")
	out = "```diff\n"

	
	for line in decklist:
		
		simple = simplify_line(line)
		if simple in banned_list:
			out += f"-{simple}\n"
		else:
			api_url = base_url + urllib.parse.quote(simple)
			response = requests.get(api_url)
			#time.sleep(5)
			data =response.json()
			if data["object"] == "error" or data["total_cards"] == 0:
				print(data)
				print(api_url)
				out += f"-{simple}\n"
			else: 
				flaggy = False
				for elem in data["data"]:
					if elem["name"].lower() == simple.lower() and flaggy == False:
						out += f"+{simple}\n"
						flaggy = True
				if flaggy == False:
					out += f"-{simple}\n"
						
	out += "```\n"
	return out


async def run_blocking(blocking_func: typing.Callable, *args, **kwargs) -> typing.Any:
    """Runs a blocking function in a non-blocking way"""
    func = functools.partial(deckcheck, *args, **kwargs) # `run_in_executor` doesn't support kwargs, `functools.partial` does
    return await client.loop.run_in_executor(None, func)

@client.event
async def on_message(message):
	if not isinstance(message.channel, discord.channel.DMChannel):
		return 

	if message.author == client.user:
		return

	await message.channel.send("Please give me some Minutes<3```diff\n+Green cards are legal\n-Red cards are illegal```\n")
	usr_message = message.content.splitlines()
	
	text = await run_blocking(deckcheck, usr_message[:])
	await message.channel.send(text)


client.run(TOKEN)