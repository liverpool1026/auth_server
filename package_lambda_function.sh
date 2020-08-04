#!/bin/sh

mkdir deps
python3 -m pip install --target deps/ --system pyotp passlib

cd deps/
zip -r9 ../auth_server.zip .
cd ..
zip -g -r auth_server.zip auth_server/ lambda_function.py


