#!python3
#
# Read and parse to .md data from chords.json (by https://github.com/popstas/chords-parser)
#
# python3 readchords.py <dir_with_chords.json>
#

import os, sys, time, re, glob, json

sys.path.insert(0, '..')
from update import main as update_main
from updatelist import main as updatelist_main
from updaterssd import main as updaterss_main

path = '.'
if len(sys.argv) > 1:
  path = sys.argv[1]

cdir = os.path.dirname(__file__)

fcount = 0

for fn in glob.glob(path+'/chords*.json'):
  chlist = json.load(open(fn))
  for song in chlist:
    pdt = time.strptime(song['created'][:-1], '%Y-%m-%dT%H:%M:%S.%f')
    ctime = time.strftime('<!--%Y-%m-%d %H:%M:%S-->', pdt)
    for d in filter(os.path.isdir, os.listdir(cdir)):
      art = song['details']['artist']
      print(777, art.lower())
      if re.search('['+d+']', art.lower()[0]):
        artpath = os.path.join(cdir, d, art)
        if not os.path.exists(artpath):
          os.mkdir(artpath)
        songpath = os.path.join(artpath, song['details']['title'].replace('/', '')+'.txt')
        open(songpath, 'w').write(ctime + '\n' + song['text'].replace(']:', ']:\n'))
        print(songpath)
        fcount += 1

if fcount:
  update_main(cdir)
  updatelist_main(cdir)
  updaterss_main(cdir)
