import discord, sys, os, re
from discord.ext import commands

if 'env.py' in os.listdir(os.getcwd()):
    import env
else:
    sys.exit("env.py file not found!")

class EmbedHelp(commands.HelpCommand):

    def get_ending_note(self):
        return f"Use {self.clean_prefix}{self.invoked_with} [command] for more info on a command"

    def get_command_signature(self, command):
        return "{0}{1} <{2}>".format(self.clean_prefix, command.qualified_name, re.findall('\w+', command.signature)[0])

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Bot Commands", color=env.COLOR)
        for cog, coms in mapping.items():
            name = "Not available" if cog is None else cog.qualified_name
            if cog is None:
                continue
            filtered_coms = await self.filter_commands(coms, sort=True)
            if filtered_coms:
                value = ', '.join(f"`{c.name}`" for c in coms)
                embed.add_field(name=name, value=value, inline=False)
        embed.set_footer(text=self.get_ending_note())
        await self.get_destination().send(embed=embed)

    async def send_command_help(self, command):
        embed = discord.Embed(title=f"Help: {command.name}", color=env.COLOR)
        syntax = f"{self.clean_prefix}{command.name}" if not command.signature else self.get_command_signature(command)
        embed.add_field(name=syntax, value=command.help)
        aliases = command.aliases
        if aliases:
            embed.add_field(name="Aliases", value=f"{', '.join(aliases)}", inline=False)
        await self.get_destination().send(embed=embed)


class Helper(commands.Cog, name="Help"):

    def __init__(self, bot):
        self.bot = bot
        self.bot.help_command = EmbedHelp()

    def cog_unload(self):
        self.bot.help_command = commands.DefaultHelpCommand()


def setup(bot):
    bot.add_cog(Helper(bot))