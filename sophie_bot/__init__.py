# Copyright © 2018, 2019 MrYacha
# This file is part of SophieBot.
#
# SophieBot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SophieBot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License

import logging
import coloredlogs
import asyncio
import redis
import ujson
import sys

from quart import Quart

from aiogram.contrib.fsm_storage.redis import RedisStorage

from pymongo import MongoClient
from motor import motor_asyncio
from telethon import TelegramClient
from aiogram import Bot, Dispatcher, types

from sophie_bot.config import get_config_key

# enable logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s: %(message)s",
    level=logging.INFO)

logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO', logger=logger)

logger.info("----------------------")
logger.info("|      SophieBot     |")
logger.info("----------------------")
logger.info("Powered by Telethon and AIOGram and bleck megic")

if not (platform := sys.platform == 'linux' or 'linux2'):
    logger.error("SophieBot support only Linux systems, your OS is " + platform)
    exit(1)

DEBUG_MODE = get_config_key("debug_mode")
if DEBUG_MODE is True:
    logger.setLevel(logging.DEBUG)
    coloredlogs.set_level('DEBUG')
    logger.warn("! Enabled debug mode, please don't use it on production to repect data privacy.")


OWNER_ID = get_config_key("owner_id")

SUDO = list(get_config_key("sudo"))
SUDO.append(OWNER_ID)

WHITELISTED = SUDO + [OWNER_ID] + [483808054]

API_ID = get_config_key("app_id")
API_HASH = get_config_key("app_hash")
MONGO_CONN = get_config_key("mongo_conn")
MONGO_PORT = get_config_key("mongo_port")
REDIS_COMM = get_config_key("redis_conn")
REDIS_PORT = get_config_key("redis_port")
TOKEN = get_config_key("token")
NAME = TOKEN.split(':')[0] + get_config_key("bot_name_additional")

# Init MongoDB
mongodb = MongoClient(MONGO_CONN).sophie
motor = motor_asyncio.AsyncIOMotorClient(MONGO_CONN, MONGO_PORT)
smotor = motor.sophie

# Init Redis
redis = redis.StrictRedis(
    host=REDIS_COMM, port=REDIS_PORT, db='1', decode_responses=True)

tbot = TelegramClient(NAME, API_ID, API_HASH)

# Telethon
tbot.start(bot_token=TOKEN)

# AIOGram
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
storage = RedisStorage()
dp = Dispatcher(bot, storage=storage)

# Quart
quart = Quart(__name__)

bot_info = asyncio.get_event_loop().run_until_complete(bot.get_me())
BOT_USERNAME = bot_info.username  # bot_info.username
BOT_ID = bot_info.id
