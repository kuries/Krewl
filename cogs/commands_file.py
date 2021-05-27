import discord, sys, os
from discord.ext import commands
import random, requests, json
import typing

if 'env.py' in os.listdir(os.getcwd()):
    import env
else:
    sys.exit("env.py file not found!")

store = ["Hey", "Yo Wassup 😁", "gtg :wave:", "Hola Amigo!!!", ":astonished:", "Hi :slight_smile:"]

class General(commands.Cog, name="General"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='spam', help='Spams the user mentioned(5 times)')
    async def spam(self, ctx, mem: typing.Union[discord.Member, str]):
        if type(mem) == str:
            if mem[0] == '@':
                mem = mem[1:]
            await ctx.send(f"'{mem}' is not a user in this server.")
            return
        print(str(mem))
        if str(mem) == 'lodestar#6104':
            await ctx.send("Hehe. I won't allow it 😝")
            return
        for i in range(15):
            await ctx.send(f"{mem.mention}")

    @commands.command(name='hey', help="Greets the user back")
    async def hey(self, ctx):
        await ctx.send(f"{ctx.author.mention} {random.choice(store)}!")

    @commands.command(name='flag', help="Sends the flag emoji of the given country")
    async def flag(self, ctx, *, country=None):
        if country is not None:
            try:
                url = 'https://restcountries.eu/rest/v2/name/' + country + '?fullText=true'
                response_id = requests.get(url)
                cid = json.loads(response_id.text)[0]['alpha2Code'].lower()
            except KeyError:
                await ctx.send(f"{ctx.author.mention} Country Not found.")
                return
        else:
            cid = 'in'
        await ctx.send(":flag_" + f"{cid}" + ":")

    @commands.command(name="ping", help="For testing purposes.")
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
