#!python3
#
# YouTube playlist CSV files (from https://jolantahuba.github.io/YT-Backup/) reader. 
#
# python3 ../../readcsv.py <dir_with_csv_playlist> ( run from dir where .md will be created )
#

import os, sys, time, re, csv

path = '.'
if len(sys.argv) > 1:
  path = sys.argv[1]

def tr_cut(t):
  t = re.sub(r'[/\.,\s]+',' ',t.lower())
  tr = []
  for ch in t:
    if ch in ' абвгдеёжзийклмнопрстуфхцчшщыъьэюяabcdefgjijklmnopqrstuvwxyz0123456789':
      tr.append( ch )
  t = ''.join(tr)
  t = re.sub('\s+','-',t)
  t = t.strip('-')
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
              href = 'https://www.youtube.com/watch?v='+row[0]
              imurl = row[5]
              rdate = row[3]
              authr = row[2]
              titl = row[1]
              ftime = os.path.getmtime(os.path.join(root, name))
              ctime = time.strftime('<!--%Y-%m-%d %H:%M:%S-->', time.localtime(ftime))

              text = """{ctime}
<div>
<a class="nodecor" href={href} target="_blank">
  <img src="{imurl}" class="yb" align="middle" alt="">
</a>
&nbsp;&nbsp;&nbsp;
<div class="inlbl">
  <a class="nodecor" href="{href}" target="_blank">{titl}</a><br>
  <i class="smaller2">{authr}</i>
</div>
</div>
""".format(ctime=ctime, href=href, imurl=imurl, titl=tr_chars(titl, 50), authr=authr)

              mtitl = tr_cut(titl)
              print(mtitl)

              open(mtitl + '.md', 'w', encoding='utf-8', newline='\n').write(text)
              fcount += 1

if fcount:
  import subprocess
  subprocess.Popen(['python', '../update.py'], cwd='../..')