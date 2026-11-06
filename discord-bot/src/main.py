#!/usr/bin/env python3

from utils import *
from peter import Peter

def main() -> None:
	# set up the logger
	log_path = r"./logs/latest.log"
	logger = get_logger(__name__, log_path)

	# set up & run the bot
	pete = Peter()
	discord_token = get_env('DISCORD_BOT_TOKEN')
	pete.run(discord_token)

if __name__ == '__main__':
	main()
