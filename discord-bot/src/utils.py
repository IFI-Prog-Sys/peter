import sys as _sys
import os as _os

import logging as _logging
import pathlib as _pathlib

import yaml as _yaml


class Config:
	def __init__(self, logger, *required_configs, **optional_configs):
		self.logger = logger

		self.config = {}
		self.required_configs = required_configs
		self.optional_configs = optional_configs

	def create(self, f_name: str):
		self.logger.info(f"Creating config file {f_name}")

		data = []
		required_line_str = "{}: ~\n"
		optional_line_str = "{}: {}\n"
		for required in self.required_configs:
			data.append(required_line_str.format(required))

		data.append("\n")

		for key, value in self.optional_configs.items():
			data.append(optional_line_str.format(key, value))

		with open(f_name, 'w') as f:
			f.writelines(data)

		self.logger.info(f"Config created successfully.")

	def load(self, stream):
		self.config = _yaml.safe_load(stream) or {}

		self.logger.info(f"Loading config")

		for required in self.required_configs:
			if required not in self.config:
				self.logger.error(f"Required key {required} not found in config.")
				_sys.exit(1)

		for optional in self.optional_configs:
			if optional not in self.config:
				self.logger.info(
					f"Optional key {optional} not found in config, defaulting to {self.optional_configs[optional]}")

		expected_configs = self.required_configs + tuple(self.optional_configs.keys())
		for key, value in self.config.items():
			if key not in expected_configs:
				if self.config["redundant_config_opts"] == "Error":
					self.logger.error(f"Config key {key} not found in config, exiting.")
					_sys.exit(1)
				else:
					self.logger.info(f"Config key {key} not found in config, ignoring.")

		self.logger.info(f"Config loaded successfully.")

	def safe_load(self, f_name: str, force_create=True):
		f_path = _pathlib.Path(f_name)
		if _pathlib.Path.exists(f_path):
			with open(f_name, 'r') as f:
				self.config = _yaml.safe_load(f) or {}
		elif force_create:
			self.logger.info(f"{f_name} does not exist, creating.")
			f_path.parent.mkdir(parents=True, exist_ok=True)
			self.create(f_name)

			if req_len := len(self.required_configs):
				self.logger.error(f"{req_len} required configs not found, please set them and rerun.")

			with open(f_name, 'r') as f:
				self.config = _yaml.safe_load(f) or {}
		else:
			self.logger.error(f"Config file {f_name} not found. Set `force_create` to True to create one.")

	def __getitem__(self, key):
		return self.config[key]


def get_all_unregistered_members() -> list[str]:
	# open the database
	# get every intern without a discord registration
	return ["rex.0515"]


def get_logger(name: str | None, path: str) -> _logging.Logger:
	_pathlib.Path(path).parent.mkdir(parents=True, exist_ok=True)

	_max_level_length = max(map(len, _logging.getLevelNamesMapping().keys()))
	_logging.basicConfig(
		filename=path,
		level=_logging.INFO,
		format=f"[%(asctime)s] %(levelname){-_max_level_length}s %(filename)s:%(lineno)d: %(message)s",
		datefmt="%H:%M:%S",
		filemode="w",
	)

	logger = _logging.getLogger(name)
	logger.addHandler(_logging.StreamHandler())
	logger.setLevel(_logging.INFO)

	return logger


def get_env(env_name: str) -> str:
	if (token := _os.getenv("DISCORD_BOT_TOKEN")) is None:
		_logging.error(f"Environment_var {env_name} is not set")
		_sys.exit(1)
	return token
