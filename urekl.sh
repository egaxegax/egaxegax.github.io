#!/bin/bash

xargs -P0 -I {} sh -c '$1' - {} <<EOF
chromium --app=https://egax.ru/rekl.html?r=6
chromium --app=https://egax.ru/rekl.html?r=6
chromium --app=https://egax.ru/rekl.html?r=1
chromium --app=https://egax.ru/rekl.html?r=2
chromium --app=https://egaxegax.github.io/rekl.html?r=1
chromium --app=https://egaxegax.github.io/rekl.html?r=2
chromium --app=https://egaxegax.github.io/rekl.html?r=3
chromium --app=https://egaxegax.github.io/rekl.html?r=4
EOF
