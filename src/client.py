import asyncio
import os
import discord
import dotenv
import logging
import pendulum
import aiofiles
import asyncpg
import json

from . import context, misc

from discord.ext import commands

DATABASE_CONNECTION_TRIES = 5

class Bot(commands.Bot):
    def __init__(self, **options):
        dotenv.load_dotenv()
        
        self.logger = logging.getLogger(__name__)
        
        self.c_emojis = None
        
        super().__init__(command_prefix=os.getenv("PREFIX"), intents=discord.Intents.all(), **options)
        
    async def login(self, bot=True):
        self.load_extensions()
        await self.initialize_db()
        await self.load_emojis()
        await super().login(token=os.getenv("TOKEN"), bot=bot)  
        
    def load_extensions(self):
        extensions_path = "src/extensions"
        for file in os.listdir(extensions_path):
            if file.endswith(".py") and not file.startswith("__init__"):
                try:
                    self.load_extension(
                        f"{extensions_path.replace('/', '.')}.{file.rstrip('.py')}"
                    )
                except Exception as ex:
                    self.logger.warn("", exc_info=ex)
                    
        self.load_extension('jishaku')
                    
    async def load_emojis(self):
        async with aiofiles.open("emojis.json", "r") as file:
            file = json.loads(await file.read())
            self.c_emojis = misc.DotDict(file)
            
    async def initialize_db(self):
        for i in range(DATABASE_CONNECTION_TRIES):
            try:
                self.pool = await asyncpg.create_pool(os.getenv("DB_URL"))
                return
            except Exception as ex:
                self.logger.warn(f"Connection to database failed. [{i}/{DATABASE_CONNECTION_TRIES}]", exc_info=ex)
                await asyncio.sleep(2)
        else:
            self.logger.error(f"Connection to database failed after {DATABASE_CONNECTION_TRIES} tries.")
    
    async def get_context(self, message, *, cls=None):
        return await super().get_context(message, cls=cls or context.Context)

