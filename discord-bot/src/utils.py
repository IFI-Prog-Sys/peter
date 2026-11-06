import sys as _sys
import os as _os

import logging as _logging
import pathlib as _pathlib


# This is here as a temporary function to simulate a database that returns a list of usernames
def get_all_unregistered_members() -> list[str]:
	# open the database
	# get every intern without a discord registration
	pass


# get the logger to be used by the bot
def get_logger(name: str | None, path: str) -> _logging.Logger:
	# create the log files parents path if it doesn't exist
	_pathlib.Path(path).parent.mkdir(parents=True, exist_ok=True)

	# get the length of the longest level name so we can use it to align out log
	# I feel like there should be a better way of doing this
	_max_level_length: int = max(map(len, _logging.getLevelNamesMapping().keys()))
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
