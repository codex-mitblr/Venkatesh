import os
import pathlib
from typing import NamedTuple

ENVIRONMENT = os.getenv("ENVIRONMENT")
if ENVIRONMENT is None:
    from dotenv import load_dotenv

    load_dotenv(dotenv_path=f"{os.getcwd()}/.env")

# Environment Vars
PREFIX = os.getenv("PREFIX", ">")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Paths
EXTENSIONS = pathlib.Path("venkatesh/exts/")

if TEST_GUILDS := os.getenv("TEST_GUILDS"):
    TEST_GUILDS = [int(x) for x in TEST_GUILDS.split(",")]


class Channels(NamedTuple):
    log = int(os.getenv("CHANNEL_LOG", 1035618172402925659))


class Roles(NamedTuple):
    moderator = int(os.getenv("ROLE_MODERATOR", 1037793218756104292))
