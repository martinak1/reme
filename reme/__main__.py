#!/usr/bin/env python3

# TODO
# add clap
# add argument for log level
# add arguement for log file
# add argument for starting a demo for performance metrics
# add argument for setting a database file path
# add a clean option to remove old entries from the database
# move most of the setup to functions in reme.py

from reme import Reme
import logging
import asyncio
import argparse

def set_log(lvl: str):
    """
    Sets the log level based off of what is provided from cli args
    :param str
    """
    logging.basicConfig()
    logging.getLogger("discord").setLevel(logging.INFO)
    logging.getLogger("discord.client").setLevel(logging.WARNING)
    logging.getLogger("discord.gateway").setLevel(logging.WARNING)
    logging.getLogger("websockets").setLevel(logging.WARNING)

    if lvl == "debug":
        level = logging.DEBUG
    elif lvl == "warning":
        level = logging.WARNING
    elif lvl == "error":
        level = logging.ERROR
    else:
        level = logging.INFO

    logging.getLogger().setLevel(level)
    logging.info(f"Reme: The log level has been set to: {lvl}")

# end set_log

async def main(database: str = None, token: str = None):
    # set log level
    bot = Reme()
    await bot.bootstrap(database=database, token=token)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--database",
        help="the path to the database",
        default="reme.db"
    )
    parser.add_argument(
        "-lv", "--level", 
        help="changes the level of detail in the log", 
        choices=["info", "debug", "warning", "error"],
        default="info"
    )
    parser.add_argument(
        "-t", "--token", 
        help="the path to the token file",
        default="token.id"
    )

    args = parser.parse_args()
    set_log(args.level)

    try:
        asyncio.run(main(database=args.database, token=args.token))
    except SystemExit:
        logging.info("Reme - A SystemExit signal has been received. Exiting!")
    except RuntimeError as e:
        logging.error(f"Reme - A RunTimeError occurred | {e}")
    except KeyboardInterrupt:
        logging.info("Reme - A KeyboardInterupt signal has been received. Exiting!")
    except Exception as e:
        logging.error(f"Reme - An unknown error occurred | {type(e)}: {e}")
        exit(1)