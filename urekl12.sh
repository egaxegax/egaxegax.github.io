#!/bin/bash

pkill -f "rekl1.html\?r"
sleep 1s
xargs -P0 -I {} sh -c 'CHROMIUM_FLAGS="--disk-cache-size=0" $1' - {} <<EOF
chromium --app=https://egax.ru/rekl1.html?r=0_240,0_240,0_240,0_s
chromium --app=https://egax.ru/rekl1.html?r=0_32,0_36,0_240,0_s
chromium --app=https://egax.ru/rekl1.html?r=0_32,0_36,0_240,0_s
chromium --app=https://egax.ru/rekl1.html?r=0_32,0_32,0_32,0_s
chromium --app=https://egax.ru/rekl1.html?r=0_32,0_32,0_32,0_s
chromium --app=https://egax.ru/rekl1.html?r=0_32,0_32,0_32,0_s
chromium --app=https://egax.ru/rekl1.html?r=0_32,0_32,0_32,0_s
chromium --app=https://egax.ru/rekl1.html?r=0_32,0_32,0_32,0_s
chromium --app=https://egax.ru/rekl1.html?r=0_32,0_32,0_32,0_s
chromium --app=https://egax.ru/rekl1.html?r=0_32,0_32,0_32,0_s
chromium --app=https://egaxegax.github.io/rekl1.html?r=1_240,1_240,1_240,1_s
chromium --app=https://egaxegax.github.io/rekl1.html?r=1_32,1_36,1_240,1_s
chromium --app=https://egaxegax.github.io/rekl1.html?r=1_32,1_36,1_240,1_s
chromium --app=https://egaxegax.github.io/rekl1.html?r=1_32,1_32,1_36,1_s
chromium --app=https://egaxegax.github.io/rekl1.html?r=1_32,1_32,1_32,1_s
chromium --app=https://egaxegax.github.io/rekl1.html?r=1_32,1_32,1_32,1_s
chromium --app=https://egaxegax.github.io/rekl1.html?r=1_32,1_32,1_32,1_s
chromium --app=https://egaxegax.github.io/rekl1.html?r=1_32,1_32,1_32,1_s
chromium --app=https://egaxegax.github.io/rekl1.html?r=1_32,1_32,1_32,1_s
chromium --app=https://egaxegax.github.io/rekl1.html?r=1_32,1_32,1_32,1_s
EOF
sleep 3s
fly-wmfunc FLYWM_TILE_MATRIX
