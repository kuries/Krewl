import discord, sys, os
from discord.ext import commands

if 'env.py' in os.listdir(os.getcwd()):
    import env
else:
    sys.exit("env.py file not found!")


class General(commands.Cog, name="general"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='hey')
    async def hey(self, ctx):
        await ctx.send(f"Hey {ctx.message.author}!")

    @commands.command(name="ping")
    async def ping(self, context):
        embed = discord.Embed(
            color=0x00FF00
        )
        embed.add_field(
            name="Pong!",
            value=":ping_pong:",
            inline=True
        )
        embed.set_footer(
            text=f"Pong request by {context.message.author}"
        )
        await context.send(embed=embed)


def setup(bot):
    bot.add_cog(General(bot))
