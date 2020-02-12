#!/usr/bin/env python3

# TODO
# add clap
# add argument for log level
# add arguement for log file
# add argument for starting a demo for performance metrics
# add argument for setting a database file path
# add a clean option to remove old entries from the database
# move most of the setup to functions in reme.py

from reme.reme import Reme
import logging
import asyncio
import argparse

async def main():
    # set log level
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)
    logging.getLogger("discord").setLevel(logging.INFO)
    logging.getLogger("discord.client").setLevel(logging.WARNING)
    logging.getLogger("discord.gateway").setLevel(logging.WARNING)
    logging.getLogger("websockets").setLevel(logging.WARNING)

    bot = Reme()
    await bot.bootstrap()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-l", "--log", 
        help="the path where the log file should be saved",
        default=None
    )
    parser.add_argument(
        "-lv", "--log-level", 
        help="changes the level of detail in the log", 
        choices=["info", "debug", "warning", "error"],
        default="info"
    )
    parser.add_argument(
        "-t", "--token", 
        help="the path to the token file",
        default=None
    )

    args = parser.parse_args()

    try:
        asyncio.run(main())
    except SystemExit:
        logging.info("Reme - A SystemExit signal has been received. Exiting!")
    except RuntimeError as e:
        logging.error(f"Reme - A RunTimeError occurred | {e}")
    except KeyboardInterrupt:
        logging.info("Reme - A KeyboardInterupt signal has been received. Exiting!")
    except Exception as e:
        logging.error(f"Reme - An unknown error occurred | {type(e)}: {e}")
        exit(1)