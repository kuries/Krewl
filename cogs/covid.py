import discord, sys, os
import requests, json
import asyncio
import locale
from discord.ext import commands, tasks
from edit_distance import word_check

if 'env.py' in os.listdir(os.getcwd()):
	import env
else:
	sys.exit("env.py file not found!")


def create_embed_world(country_id=None):
	# for converting the values to indian numbering system
	locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

	# country_id consists of the alpha2 code
	# if ?covid world is called
	if country_id is not None:

		# the api sends data of a particular country based on their alpha 2 code
		url = 'http://corona-api.com/countries/' + country_id
		response = requests.get(url)
		store = json.loads(response.text)['data']
		embed = discord.Embed(title=f"{':flag_'+country_id.lower()+':'} {store['name']}", description="\n\u200b\n", color=env.COLOR)
		store = store['timeline'][0]
		active = store['confirmed'] - store['recovered'] - store['deaths']

	# if ?covid <country> command is called
	else:

		# if ?covid world command is called
		response = requests.get("https://corona-api.com/timeline")

		store = json.loads(response.text)['data'][0]
		embed = discord.Embed(title=":globe_with_meridians: World Statistics", description="Today \n\u200b\n", color=env.COLOR)
		active = store['active']

	#the store variable is modified based on the above two condtions
	embed.add_field(name="Active", value=f"{active:n}", inline=False)
	embed.add_field(name="Confirmed", value=f"{store['confirmed']:n}\u200b \u200b \u200b \u200b :arrow_up: {store['new_confirmed']:n}", inline=False)
	embed.add_field(name="Recovered", value=f"{store['recovered']:n}\u200b \u200b \u200b \u200b:arrow_up: {store['new_recovered']:n}", inline=False)
	embed.add_field(name="Deaths", value=f"{store['deaths']:n}\u200b \u200b \u200b \u200b:arrow_up: "
										 f"{store['new_deaths']:n}", inline=False)
	if country_id == 'in':
		embed.set_footer(text="Press <'s state_name'> to get a detailed statistics of that state")
	return embed


async def create_embed_states(msg):
	# for converting the values to indian numbering system
	locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

	fe = open("./storage/covid_data.json", mode='r')
	data_json = json.load(fe)
	fe.close()

	try:
		index = data_json['states'][msg.content[2:].lower()]
	except KeyError:
		state_name, err_val = word_check(msg.content[2:].lower())
		print(msg.content[2:].lower())
		if err_val < 3:
			if len(state_name) == 1:
				index = data_json['states'][state_name[0]]
			elif len(state_name) <= 6:
				embed = discord.Embed(title=f"Are you searching for any of these states?\n",description='\u200b', color=env.COLOR)
				embed.add_field(name=f"{', '.join(state_name)}", value='\u200b', inline=False)
				await msg.channel.send(embed=embed)
				return
			else:
				await msg.channel.send(f"{msg.author.mention} State not found.")
				return
		else:
			await msg.channel.send(f"{msg.author.mention} State not found.")
			return
	
	data_json = data_json['regional'][index]
	active = data_json["confirmedCasesIndian"] - data_json["discharged"] - data_json["deaths"]
	embed = discord.Embed(title=f"{data_json['loc']}", description="\n\u200b\n", color=env.COLOR)
	embed.add_field(name="Active", value=f"{active:n}", inline=False)
	embed.add_field(name="Confirmed", value=f"{data_json['confirmedCasesIndian']:n}", inline=False)
	embed.add_field(name="Recovered", value=f"{data_json['discharged']:n}", inline=False)
	embed.add_field(name="Deaths", value=f"{data_json['deaths']:n}", inline=False)
	embed.set_footer(text="Type <'s state_name'> to get a detailed statistics of that state")
	await msg.channel.send(embed=embed)


class Covid(commands.Cog, name="Covid-19 stats"):

	def __init__(self, bot):
		self.bot = bot
		self.bot.loop.create_task(self.file_update())


	async def file_update(self):
		await self.bot.wait_until_ready()
		while not self.bot.is_closed():
			print("Updating the file")
			response = requests.get("https://api.rootnet.in/covid19-in/stats/latest")
			store = json.loads(response.text)['data']
			summary = store['summary']

			with open("./storage/covid_data.json", mode='w') as f:
				json_data = {}
				state_names = {}
				store = store['regional']
				for i in range(len(store)):
					state_names[store[i]['loc'].lower()] = i
				json_data['states'] = state_names
				json_data['regional'] = store
				json_data['summary'] = summary
				json.dump(json_data, f, indent=4)
			await asyncio.sleep(10000)

	# ?covid <text> triggers the command
	@commands.command(
						name="covid",
						help="Shows the real time statistics all over the world\nDefault is `world`",
						aliases=["c", "covid-19"])
	async def world(self, context, *, country='world'):

		country = country.lower()

		# ?covid world (case insensitive)
		if country == 'world':
			await context.send(embed=create_embed_world())

		# ?covid india (case insensitive)
		elif country == 'india':
			await context.send(embed=create_embed_world('in'))

			def check(m):
				return m.author == context.author and m.content[0:2].lower() == "s "

			# terminates when the user dosen't enter anything for 30 seconds
			while True:
				# waits for the user to enter the command s <state-name>
				try:
					msg = await self.bot.wait_for("message", check=check, timeout=45)
				except asyncio.TimeoutError:
					await context.send(f"{context.author.mention} loop terminated. To get info on the indian states "
									   f"try calling the command `?covid india` again.")
					break
				else:
					await create_embed_states(msg)

		# ?covid <country-name>
		else:
			# REST API for countries
			url = 'https://restcountries.com/v3/name/' + country
			response_id = requests.get(url)
			country_id = json.loads(response_id.text)

			# gets the alpha 2 code for a particular country
			try:
				country_id = country_id[0]['cca2'].lower()
			except KeyError:
				if country[0] == 'e':
					await context.send(f"{context.author.mention} Are you searching for england? Then search for 'uk' instead.")
				elif country[0] == 's':
					await context.send(f"{context.message.author.mention} Are you searching for scotland? Then search for 'uk' instead.")
				else:
					await context.send(f"{context.author.mention} Country not found. ¯\_(ツ)_/¯")
			else:
				await context.send(embed=create_embed_world(country_id))


def setup(bot):
	bot.add_cog(Covid(bot))
