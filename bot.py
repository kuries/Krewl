import discord, sys, os
from discord.ext import commands

if 'env.py' in os.listdir(os.getcwd()):
    import env
else:
    sys.exit("env.py file not found!")

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='?', intents=intents)


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user.name} {bot.user.id}")
    print(f"Discord.py version: {discord.__version__}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="?help"))


@bot.event
async def on_message(msg):
    if msg.author == bot.user:  # the command is skipped if it's from the bot
        return
    else:
        await bot.process_commands(msg)


bot.remove_command("help")

if __name__ == "__main__":
    for extension in env.STARTUP_COGS:
        try:  # the file is loaded if it's present in the list inside env.py
            temp = 'cogs.' + extension
            bot.load_extension(temp)
            print(f"Successfully loaded {extension}")
        except Exception as e:
            print(f"Failed to load {extension}")
            print(e)

bot.run(env.TOKEN)
