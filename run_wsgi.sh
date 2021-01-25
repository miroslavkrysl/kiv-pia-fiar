#!/bin/sh
gunicorn --worker-class eventlet -w 1 'fiar:app'