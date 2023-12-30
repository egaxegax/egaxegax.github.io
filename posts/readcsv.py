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

def truncate_chars(value, max_length):
    if len(value) > max_length:
        truncd_val = value[:max_length]
        if not len(value) == max_length+1 and value[max_length+1] != " ":
            truncd_val = truncd_val[:truncd_val.rfind(" ")]
        return  truncd_val + "..."
    return value

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
<a class="nodecor" href={href}>
  <img src="{imurl}" width="300px" align="middle" alt="" style="border-radius:10%">
</a>
&nbsp;&nbsp;&nbsp;
<a class="nodecor" href="{href}">{titl}</a>
</div>
""".format(ctime=ctime, href=href, imurl=imurl, titl=truncate_chars(titl, 50), authr=authr)

              mtitl = ''
              for ch in titl:
                if ord(ch) >= 0 and ord(ch) <= 126:
                  mtitl += ch
              mtitl = mtitl.lower()
              mtitl = re.sub(r'[-\'"”“«»`%\*:/\|\{\}\(\)\[\]\!\?\&\$\#@]+','',mtitl)
              mtitl = re.sub(r'[\.,\s]+','-',mtitl)

              print(mtitl)

              open(mtitl + '.md', 'w', encoding='utf-8', newline='\n').write(text)

import subprocess
subprocess.Popen(['python', '../update.py'], cwd='../..')