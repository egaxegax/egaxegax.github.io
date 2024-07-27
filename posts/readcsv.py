#!python3
#
# Parse YouTube playlist CSV files (from https://jolantahuba.github.io/YT-Backup/) to .md. 
#
# python3 ../../readcsv.py <dir_with_csv_playlist> ( run from dir where .md will be create )
#

import os, sys, time, re, csv

sys.path.insert(0, '../../..')

from update import TR
from update import main as update_main
from updatelist import main as updatelist_main

path = '.'
if len(sys.argv) > 1:
  path = sys.argv[1]

def tr_cut(t):
  t = re.sub(r'[/\.,\s]+',' ',t)
  tr = []
  for ch in t:
    if ch.lower() in ' -абвгдеёжзийклмнопрстуфхцчшщыъьэюяabcdefghjijklmnopqrstuvwxyz0123456789':
      tr.append( ch )
  t = ''.join(tr)
  t = re.sub('\s+',' ',t)
  t = t.strip()
  return t

def tr_chars(value, max_length):
    if len(value) > max_length:
        truncd_val = value[:max_length]
        if not len(value) == max_length+1 and value[max_length+1] != ' ':
            truncd_val = truncd_val[:truncd_val.rfind(' ')]
        return  truncd_val + '...'
    return value

fcount = 0

for root, dirs, files in os.walk(path, topdown=False):
  for name in files:

    fname, ext = os.path.splitext(name)

    if ext in ('.csv',):
      with open(os.path.join(root, name), newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        skipheader = 0
        for row in reader:
          if len(row) > 2:
            if not skipheader:
              skipheader = 1
            elif skipheader:
              videoid = row[0]
              href = 'https://www.youtube.com/watch?v='+videoid
              imurl = row[5]
              rdate = row[4]
              authr = row[2]
              titl = row[1]
              ftime = os.path.getmtime(os.path.join(root, name))
              ctime = time.strftime('<!--%Y-%m-%d %H:%M:%S-->', time.localtime(ftime))
              mtitl = tr_cut(titl)
              phref = '/posts.html?'+ TR(os.path.basename(os.getcwd())) +'/'+ TR(mtitl)
              text = """{ctime}
<div class="yb">
  <a class="nodecor" href="{phref}">
    <img class="preview" data-videoid="{videoid}" src="{imurl}" align="middle" alt="">
  </a>
  <div class="inlbl">
    <a class="nodecor" href="{phref}">{titl}</a><br>
    <i class="smaller2">{authr}</i><br>
    <i class="smaller3">{rdate}</i>
  </div>
</div>
""".format(ctime=ctime, phref=phref, href=href, imurl=imurl, rdate=rdate, videoid=videoid, titl=tr_chars(titl, 60), authr=authr)

              print(mtitl)
              open(mtitl + '.md', 'w', encoding='utf-8', newline='\n').write(text)
              fcount += 1

if fcount:
  update_main(os.path.dirname(__file__))
  updatelist_main(os.path.dirname(__file__))
  