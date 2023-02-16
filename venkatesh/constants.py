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
    memberlog = int(os.getenv("CHANNEL_MEMBERLOG", 1035619429658132532))


class Departments(NamedTuple):
    cxsd = 1035615903762612334
    cxos = 1035615907503943711
    cxcp = 1035615911664697480
    cxad = 1035615915506683974
    cxit = 1035615919768080404
    cxds = 1035615923605880942
    cxnat = 1035615930627129345
    cxgd = 1035615934074847232


class Roles(NamedTuple):
    moderator = int(os.getenv("ROLE_MODERATOR", 1037793218756104292))
