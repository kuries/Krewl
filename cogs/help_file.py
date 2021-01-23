import discord, sys, os
from discord.ext import commands

if 'env.py' in os.listdir(os.getcwd()):
    import env
else:
    sys.exit("env.py file not found!")

class Help(commands.Cog, name = "Help"):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help", aliases=["h"])
    async def help(self, ctx, *, args):
        if args == 'covid' or args == 'CoronaStats':
            embed = discord.Embed(title="Aliases: covid", color=0xa83238)
            embed.set_author(name="Help command: CoronaStats")
            embed.add_field(name="?CoronaStats", value="Shows the real time statistics all over the world",
                            inline=False)

        elif args == 'h' or args == 'help':
            embed = discord.Embed(title="Aliases: h", color=0xa83238)
            embed.set_author(name="Help command: help")
            embed.add_field(name="?help", value="Shows the help menu.", inline=False)

        else:
            embed = discord.Embed(title="Help Commands", color=0xa83238)
            embed.add_field(name="General Commands", value="help, covid\n\u200b\n\u200b\n", inline=False)
            embed.set_footer(text="Type '?help <command-name>' for more details on a command")

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))