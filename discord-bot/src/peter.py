import asyncio
import threading

import logging
import socket

import discord
from discord import Intents

from utils import get_all_unregistered_members


class Peter(discord.Client):
	def __init__(self, config, *, intents: Intents | None = None, **options) -> None:
		self.config = config
		self.server = None
		self.target_guild: discord.Guild | None = None
		self.logger = logging.getLogger("__main__")

		# if intents are none just include them all
		# TODO: limit intents depending on the acual use case
		if intents is None:
			intents = Intents.all()
		super().__init__(intents=intents, **options)

	# the listener function which listens for network requests
	# this allows us to either call it periodically usin cron, manually using curl or automatically
	def listener(self) -> None:
		# set up the socket
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.bind((
			self.config["socket_bind_addr"],
			self.config["socket_bind_port"]
		))
		self.server.listen(self.config["socket_max_connections"])

		self.logger.info("Waiting for signals from the os")

		# listen any activity
		while True:
			# block the code if there is no activity
			client, addr = self.server.accept()
			response = "HTTP/1.0 200\r\nConnection: close\r\n\r\n{}\r\n"
			client.send(response.format("Checking the database").encode("utf-8"))

			self.logger.info(f"Updating roles on discord, requested by {addr}")

			# get unregistered users from the database
			users_to_add = get_all_unregistered_members()
			client.send(f"Found {len(users_to_add)} unregistered user(s).\r\n".encode("utf-8"))

			# shutdown the connection
			client.shutdown(socket.SHUT_RDWR)

			# add the role to the users
			for user in users_to_add:
				asyncio.run_coroutine_threadsafe(self.add_role_to_member(user), self.loop)
				self.logger.info(f"Adding user {user} to discord")

	async def on_ready(self) -> None:
		self.logger.info(f'Logged in as {self.user}')

		# set the target discord server on ready so we don't make calls to the api multiple times
		self.target_guild = await self.fetch_guild(self.config["target_guild_id"])
		if self.target_guild is None:
			self.logger.error("Target guild does not exist")
			return

		# start the listener thread
		threading.Thread(target=self.listener, daemon=True).start()

	async def add_role_to_member(self, username: str) -> None:
		# this check is here in case something goes wrong
		if self.target_guild is None:
			self.logger.error("Target guild does not exist")
			return

		# this can be on ready but if the role gets deleted after initialization it might cause problems
		role_id = self.config["intern_role_id"]
		role = self.target_guild.get_role(role_id)
		if role is None:
			self.logger.error("Role does not exist")
			return

		# get every member whose name starts with the given username
		members = await self.target_guild.query_members(username)
		if members is None or len(members) == 0:
			self.logger.error(f"User {username} does not exist")
			return

		# in rare occasions a username might match something partially but not exactly
		# this might happen if;
		# a user registers with the discord username: foo
		# this user is not in the server yet
		# but there is another user called foobar
		# so foobar gets the role even tho he shouldn't

		# or in other rare occasions where a username might match multiple users, look for an exact match
		# this might happen if;
		# a user registeres with the username: foo
		# but there is another user called foobar
		# so both foo and foobar matches

		# filter the list to see if there is an exact match
		filtered_members = list(filter(lambda member: member.name == username, members))
		if len(filtered_members) == 0:
			# return if there are no exact matches
			self.logger.error(
				f"{username} has {len(members)} partial match(es) in members, but doesn't have an exact match."
			)
			return

		member = filtered_members[0]

		self.logger.info(f'Adding role of {role_id} to [{member.id}]({member.display_name})')
		# add the role
		# this doesn't check if the user already has the role, instead it silently continues
		await member.add_roles(role, reason=f"Automatically added role by {self.user}")
