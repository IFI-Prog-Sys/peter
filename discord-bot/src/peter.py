import asyncio
import threading

from logging import Logger
import socket

import discord
from discord import Intents

from utils import get_all_unregistered_members


class Peter(discord.Client):
	def __init__(self, logger: Logger, config, *, intents: Intents | None = None, **options) -> None:
		self.config = config
		self.server = None
		self.target_guild: discord.Guild | None = None
		self.logger = logger

		if intents is None:
			intents = Intents.all()
		super().__init__(intents=intents, **options)

	def listener(self) -> None:
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.bind((
			self.config["socket_bind_addr"],
			self.config["socket_bind_port"]
		))
		self.server.listen(self.config["socket_max_connections"])

		self.logger.info("Waiting for signals from the os")

		while True:
			client, addr = self.server.accept()
			response = "HTTP/1.0 200\r\nConnection: close\r\n\r\n{}\r\n"
			client.send(response.format("Checking the database").encode("utf-8"))

			self.logger.info(f"Updating roles on discord, requested by {addr}")

			users_to_add = get_all_unregistered_members()
			client.send(f"Found {len(users_to_add)} unregistered user(s).\r\n".encode("utf-8"))

			client.shutdown(socket.SHUT_RDWR)

			for user in users_to_add:
				asyncio.run_coroutine_threadsafe(self.add_role_to_member(user), self.loop)
				self.logger.info(f"Adding user {user} to discord")

	async def on_ready(self) -> None:
		self.logger.info(f'Logged in as {self.user}')

		self.target_guild = await self.fetch_guild(self.config["target_guild_id"])
		if self.target_guild is None:
			self.logger.error("Target guild does not exist")
			return

		threading.Thread(target=self.listener, daemon=True).start()

	async def add_role_to_member(self, username: str) -> None:
		if self.target_guild is None:
			self.logger.error("Target guild does not exist")
			return

		role_id = self.config["intern_role_id"]
		role = self.target_guild.get_role(role_id)

		members = await self.target_guild.query_members(username)
		if members is None or len(members) == 0:
			self.logger.error(f"User {username} does not exist")
			return

		if len(members) > 1:
			self.logger.error(f"{username} matches multiple members")
			return

		member = members[0]

		self.logger.info(f'Adding role of {role_id} to [{member.id}]({member.display_name})')
		await member.add_roles(role, reason=f"Automatically added role by {self.user}")
