import sys as _sys
import os as _os

import logging as _logging
import pathlib as _pathlib

import yaml as _yaml


# A helper class to keep track of the config
class Config:
	# Takes every positional argument as a name for a required field in the config field and
	# takes every keyword argument as a name and a default value for fields in the config.
	def __init__(self, *required_configs: str, **optional_configs):
		self.logger = _logging.getLogger("__main__")

		self.config = {}
		self.required_configs = required_configs
		self.optional_configs = optional_configs

		# Add this if it is not defined already
		if "redundant_config_opts" not in self.optional_configs:
			self.optional_configs.update({"redundant_config_opts": "Ignore"})

	def create(self, f_name: str):
		self.logger.info(f"Creating config file {f_name}")

		data = []
		# Format string for each line to use while creating the config file
		required_line_str = "{}: ~\n"
		optional_line_str = "{}: {}\n"

		# Add every required field to the list of lines
		for required in self.required_configs:
			data.append(required_line_str.format(required))

		data.append("\n")

		# Add every optional field and its value to the list
		for key, value in self.optional_configs.items():
			data.append(optional_line_str.format(key, value))

		# Write the config to file
		with open(f_name, 'w') as f:
			f.writelines(data)

		self.logger.info(f"Config created successfully.")

	def load(self, stream):
		# Load the config or an empty dict if the file is empty
		self.config = _yaml.safe_load(stream) or {}

		self.logger.info(f"Loading config")

		# Check if every required field is filled
		for required in self.required_configs:
			if required not in self.config:
				self.logger.error(f"Required key {required} not found in config.")
				_sys.exit(1)

		# Check if optional fields are present in the config file, if not fallback to their defaults
		for optional in self.optional_configs:
			if optional not in self.config:
				self.logger.info(
					f"Optional key {optional} not found in config, defaulting to {self.optional_configs[optional]}")

		# Handle the fields in the file which we don't expect
		expected_configs = self.required_configs + tuple(self.optional_configs.keys())
		for key, value in self.config.items():
			if key not in expected_configs:
				if self.config["redundant_config_opts"] == "Error":
					self.logger.error(f"Config key {key} not found in config definition, exiting.")
					_sys.exit(1)
				else:
					self.logger.info(f"Config key {key} not found in config definition, ignoring.")

		self.logger.info(f"Config loaded successfully.")

	def safe_load(self, f_name: str, force_create=True):
		f_path = _pathlib.Path(f_name)
		# if file exists load it
		if _pathlib.Path.exists(f_path):
			with open(f_name, 'r') as stream:
				self.load(stream)
		elif force_create:
			self.logger.info(f"{f_name} does not exist, creating.")

			# create the path the config is supposed to be at
			f_path.parent.mkdir(parents=True, exist_ok=True)
			self.create(f_name)

			# since we just created the file we know for a fact required config fields are empty
			# so if we have more than 0 required fields, error
			if req_len := len(self.required_configs):
				self.logger.error(f"{req_len} required configs not found, please set them and rerun.")
				_sys.exit(1)

			# load otherwise
			with open(f_name, 'r') as f:
				self.config = _yaml.safe_load(f) or {}
		else:
			self.logger.error(f"Config file {f_name} not found. Set `force_create` to True to create one.")

	# define a getitem so we can just use config["name"] to get config values
	def __getitem__(self, key):
		return self.config[key]


# This is here as a temporary function to simulate a database that returns a list of usernames
def get_all_unregistered_members() -> list[str]:
	# open the database
	# get every intern without a discord registration
	return ["rex.0515"]


# get the logger to be used by the bot
def get_logger(name: str | None, path: str) -> _logging.Logger:
	# create the log files parents path if it doesn't exist
	_pathlib.Path(path).parent.mkdir(parents=True, exist_ok=True)

	# get the lenght of the longest level name so we can use it to align out log
	# I feel like there should be a better way of doing this
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


# a utility function to safely get stuff from the env
def get_env(env_name: str) -> str:
	if (token := _os.getenv(env_name)) is None:
		_logging.error(f"Environment_var {env_name} is not set")
		_sys.exit(1)
	return token
