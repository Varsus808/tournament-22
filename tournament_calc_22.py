
import requests
import urllib.parse
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
		f'Hi {member.name}, welcome to the Un+Common Tournament 2022 server!\nIf you want your Deck checked, please respond with /Deckcheck'
	)

def simplify_line(string):
	out_str = string
	if '\n' in out_str:
		out_str = out_str[:-1]
	return ' '.join(out_str.split(' ')[1:])


def deckcheck(decklist):
	base_url = "https://api.scryfall.com/cards/search?q=" + urllib.parse.quote("(r:u or r:c) (set:sunf OR set:unf OR set:und OR set:ust OR set:unh OR set:ugl)")
	out_errors = ""
	
	print(type(decklist))
	for line in decklist:
		print(decklist, line)
		simple = simplify_line(line)
		print(simple)
		if simple in banned_list:
			out_errors += f"{simple} is either too similar to an entry in the Banned List or actually illegal \n"
		else:
			api_url = base_url + urllib.parse.quote(simple)
			response = requests.get(api_url)
			data =response.json()
			if data["object"] == "error" or data["total_cards"] == 0:
				out_errors += f"{simple} Seems not to be common or uncommon, or you are using un-Set cards!\n"

	return out_errors

@client.event
async def on_message(message):
	if message.author == client.user:
		return
	usr_message = message.content.splitlines()
	usr_message_1 = usr_message[:len(usr_message)//2]
	usr_message_2 = usr_message[len(usr_message)//2:]
	response = deckcheck(usr_message_1)
	await message.channel.send(response)
	response = deckcheck(usr_message_2)
	await message.channel.send(response)


client.run(TOKEN)

