import discord
import pendulum
import typing

from discord.ext import commands

class Context(commands.Context):   
    async def pretty_send(self, description: str, emoji: typing.Union[str, discord.Emoji, discord.PartialEmoji] = None, content: str = None, color: discord.Color = discord.Color.blurple()):
        """Sends a fancy standardized embed
        """
        if isinstance(emoji, str):
            emoji = self.bot.c_emojis.get(emoji, None)
            
        embed = discord.Embed(
            color=color,
            description=f"{emoji} {description}" if emoji else description,
            timestamp=pendulum.now(),
        )
        embed.set_footer(text=f"Requested by {self.author}", icon_url=self.author.avatar_url)
        return await self.reply(content=content, embed=embed)