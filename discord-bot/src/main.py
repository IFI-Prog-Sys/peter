#!/usr/bin/env python3

from utils import *
from peter import Peter

def main():
	# set up the logger
	log_path = r"./logs/latest.log"
	logger = get_logger(__name__, log_path)

	# set up the config
	config = Config(
		# general config
		"intern_role_id", "target_guild_id",
		# socket config
		socket_bind_addr="localhost", socket_bind_port=42069, socket_max_connections=5,
	)

	# load the config
	with open("config.yaml", 'r') as stream:
		config.load(stream)

	# set up & run the bot
	pete = Peter(config)
	discord_token = get_env('DISCORD_BOT_TOKEN')
	pete.run(discord_token)

if __name__ == '__main__':
	main()
