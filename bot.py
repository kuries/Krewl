import discord, sys, os
from discord.ext import commands

if 'env.py' in os.listdir(os.getcwd()):
    import env
else:
    sys.exit("env.py file not found!")

bot = commands.Bot(command_prefix='?')

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user.name} {bot.user.id}")
    print(f"Discord.py version: {discord.__version__}")

# @bot.event
# async def on_message(msg):
#     print(3)
#     if msg.author == bot.user:
#         print(4)
#         return



if __name__ == "__main__":
    for extension in env.STARTUP_COGS:
        try:
            temp = 'cogs.' + extension
            bot.load_extension(temp)
            print(f"Successfully loaded {extension}")
        except Exception as e:
            print(f"Failed to load {extension}")
            print(e)

bot.run(env.TOKEN)
