import sys as _sys

import time as _time
import logging as _logging

import requests as _requests
import json as _json


class NettskjemaToken:
	def __init__(self, access_token, token_type, expires_in):
		self.access_token = access_token
		self.token_type = token_type
		self.expires_in = expires_in
		self.expires_at = self.expires_in + int(_time.time())


class NettskjemaSession:
	def __init__(self, client_id: str, client_secret: str):
		self.logger = _logging.getLogger("__main__")

		self.client_id = client_id
		self.client_secret = client_secret

		self.token: NettskjemaToken | None = None

	def get_token(self):
		r = _requests.request(
			method="POST",
			url="https://authorization.nettskjema.no/oauth2/token",
			data={
				"grant_type": "client_credentials"
			},
			auth=(self.client_id, self.client_secret)
		)
		if r.status_code != 200:
			self.logger.error("Error getting a token.")
			_sys.exit(1)

		try:
			self.token = NettskjemaToken(**_json.loads(r.text))
		except _json.JSONDecodeError:
			self.logger.error("Cannot parse the token.")
			_sys.exit(1)

	def request(self, *args, **kwargs):
		create_token = False
		if self.token is None:
			self.logger.info("No token was found.")
			create_token = True

		if self.token and self.token.expires_at < int(_time.time()):
			self.logger.info("Token has expired.")
			create_token = True

		if create_token:
			self.logger.info("Creating a new token.")
			self.get_token()

		headers = kwargs.pop("headers", {})

		if "Accept" not in headers:
			headers["Accept"] = "application/x-ndjson"

		if "Authorization" not in headers:
			headers["Authorization"] = f"{self.token.token_type} {self.token.access_token}"

		return _requests.request(
			*args,
			headers=headers,
			**kwargs
		)