import sys as _sys

import time as _time
import logging as _logging
import typing as _typing

import requests as _requests
import json as _json


# A helper class for the Nettskjema token
class NettskjemaToken:
	def __init__(self, access_token: str, token_type: str, expires_in: int):
		self.access_token = access_token
		self.token_type = token_type
		self.expires_in = expires_in
		# calculate the expiry date
		self.expires_at = self.expires_in + int(_time.time())


# A helper class to keep the token fresh
class NettskjemaSession:
	def __init__(self, client_id: str, client_secret: str):
		self.logger = _logging.getLogger("__main__")

		self.client_id = client_id
		self.client_secret = client_secret

		# we initialize the token as none and get a token before a request
		# this potentially reduces the amount of times we ask for tokens
		# if there is a significant amount of time between the initialization
		# and the actual requests
		self.token: NettskjemaToken | None = None

	def update_token(self) -> None:
		# request a new token with bare minimum requirements
		r = _requests.request(
			method="POST",
			url="https://authorization.nettskjema.no/oauth2/token",
			data={
				"grant_type": "client_credentials"
			},
			auth=(self.client_id, self.client_secret)
		)
		# if it is not a success exit
		if r.status_code != 200:
			self.logger.error("Error getting a token.")
			_sys.exit(1)

		# technically we should always get a json response
		# but Nettskjema sometimes redirects to their login
		# page and serves html so we try catch here to account
		# for that
		try:
			self.token = NettskjemaToken(**_json.loads(r.text))
		except _json.JSONDecodeError:
			self.logger.error("Cannot parse the token.")
			_sys.exit(1)

	# this function is essentially a direct wrapper to requests.request
	# so it can be used the same way as requests.request, but it adds
	# the required data to the request (which can be overwritten)
	def request(self, *args, **kwargs: dict[str, _typing.Any]) -> _requests.Response:
		# by default don't create a token
		create_token = False
		# if token is not found i.e. right after initialization
		if self.token is None:
			self.logger.info("No token was found.")
			create_token = True

		# or it expired
		if self.token and self.token.expires_at < int(_time.time()):
			self.logger.info("Token has expired.")
			create_token = True

		# then create a token
		if create_token:
			self.logger.info("Creating a new token.")
			self.update_token()

		# if nettskjema returns an empty token or if something goes really wrong
		if self.token is None:
			self.logger.error("Token creation failed.")
			_sys.exit(1)

		# if there are user specified headers pop that from kwargs so we don't
		# supply it twice
		headers = kwargs.pop("headers", {})

		# if the user specified headers use theirs, else use default
		if "Accept" not in headers:
			headers["Accept"] = "application/x-ndjson"

		if "Authorization" not in headers:
			headers["Authorization"] = f"{self.token.token_type} {self.token.access_token}"

		# execute the request and return the results
		return _requests.request(
			*args,
			headers=headers,
			**kwargs
		)