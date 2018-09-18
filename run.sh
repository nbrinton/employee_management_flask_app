#!/bin/bash

pip install --editable .
export FLASK_APP=employee_app
export FLASK_DEBUG=true
flask run

