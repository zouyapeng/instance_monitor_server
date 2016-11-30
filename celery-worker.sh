#!/bin/bash

python manage.py celery worker --beat
