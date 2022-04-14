from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from config import token


bot = Bot(token=token,parse_mode="HTML")
storage=MemoryStorage()
dp = Dispatcher(bot,storage=storage)



