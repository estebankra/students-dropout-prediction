#!/bin/sh
# Linter
ruff check app --fix
# Formatter
ruff format app