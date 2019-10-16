#!/bin/bash

source ~/.profile
workon cv
python yolo_email.py
deactivate