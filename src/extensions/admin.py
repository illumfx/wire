import discord
import os

from discord.ext import commands


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    def cog_check(self, ctx):
        return ctx.author.id == int(os.getenv("OWNER_ID"))

    @commands.command()
    async def emojis(self, ctx):
        await ctx.send("\n".join([f"`{emoji}` - {self.bot.c_emojis[emoji]}" for emoji in self.bot.c_emojis]))
    

def setup(bot):
    bot.add_cog(Admin(bot))
