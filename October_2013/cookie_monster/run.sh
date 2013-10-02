#!/bin/sh
gunicorn -w 32 main:app
