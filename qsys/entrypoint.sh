#!/bin/bash

export HOME=/home/django

exec /usr/sbin/gosu django "$@"
