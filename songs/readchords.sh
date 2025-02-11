#!/bin/bash

D=~/Projects/chords-parser

npm run start --prefix $D
python3 readchords.py $D
