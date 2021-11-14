#!/bin/python3

# Import system libraries
import sys
import os
import argparse

# Do not write pycache
sys.dont_write_bytecode=True

from lib.config import get_env
from lib.logger import log, logging

from func.start import start_parser
from func.resize import resize_parser
from func.flash import flash_parser
from func.backup import backup_parser

# Default environment variables from configuration file
CONFIG_PATH = os.path.dirname(sys.argv[0]) + '/config.env'
env = get_env(CONFIG_PATH)

# Help text
usage = "docker run [docker args] ptrsr/pi-ci"
get_usage = lambda command: f"{usage} {command} [optional args]"

main_usage = f"{usage} [command] [optional args]"
main_description = "PI-CI: the reproducible PI emulator."
main_epilog = "Refer to https://github.com/ptrsr/pi-ci for the full README on how to use this program."

# Parser arguments that are shared between subparsers
shared_parser = argparse.ArgumentParser(add_help=False)
shared_parser.add_argument('-v', dest='verbose', action='store_true', help="show verbose output", default=False)

# Main CLI parser
parser = argparse.ArgumentParser(description=main_description, epilog=main_epilog, usage=main_usage, parents=[shared_parser])

# Define CLI subcommand group
command_group = parser.add_subparsers(metavar="command", help="[start, resize, flash, backup]")

# Define CLI subcommands
for enable_parser in [start_parser, resize_parser, flash_parser, backup_parser]:
  enable_parser(command_group, shared_parser, get_usage, env)

# Get CLI arguments
args = parser.parse_args(sys.argv[1:])
print(args)

# Print help on missing command or help argument
if not 'func' in args:
  parser.print_help()
  exit(0)

# Combine arguments and variables into options
opts = argparse.Namespace(**vars(args), **vars(env))

# Set verbose logging
if args.verbose:
  log.setLevel(level=logging.DEBUG)
else:
  log.setLevel(level=logging.INFO)

# Run command function using options
try:
  args.func(opts)
except Exception as e:
  log.error(e)
  log.info("Exiting ...")
