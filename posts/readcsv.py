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

def TR(t):
  ru = {
    'а':'a', 'б':'b', 'в':'v', 'г':'g', 'д':'d', 
    'е':'e', 'ё':'e', 'ж':'j', 'з':'z', 'и':'i', 'й':'j', 
    'к':'k', 'л':'l', 'м':'m', 'н':'n', 'о':'o', 
    'п':'p', 'р':'r', 'с':'s', 'т':'t', 'у':'u', 
    'ф':'f', 'х':'h', 'ц':'c', 'ч':'ch', 'ш':'sh', 
    'щ':'shch', 'ы':'y', 'э':'e', 'ю':'ju', 'я':'ya'
  }
  tr = []
  t = re.sub(r'[-\'"”“«»`%\*:/\|\{\}\(\)\[\]\!\?\&\$\#@]+','',t)
  t = re.sub(r'[\.,\s]+','-',t)  
  for s in t:
    ss = ru.get( s ) or ru.get( s.lower(), s )
    for ch in ss:
      if ord(ch) >= 0 and ord(ch) <= 126:
        tr.append( ch )
  return ''.join(tr).lower()

def truncate_chars(value, max_length):
    if len(value) > max_length:
        truncd_val = value[:max_length]
        if not len(value) == max_length+1 and value[max_length+1] != " ":
            truncd_val = truncd_val[:truncd_val.rfind(" ")]
        return  truncd_val + "..."
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
  <img src="{imurl}" width="300px" align="middle" alt="" style="border-radius:10%">
</a>
&nbsp;&nbsp;&nbsp;
<a class="nodecor" href="{href}" target="_blank">{titl}</a>
</div>
""".format(ctime=ctime, href=href, imurl=imurl, titl=truncate_chars(titl, 50), authr=authr)

              mtitl = TR(titl)
              print(mtitl)

              open(mtitl + '.md', 'w', encoding='utf-8', newline='\n').write(text)
              fcount += 1

if fcount:
  import subprocess
  subprocess.Popen(['python', '../update.py'], cwd='../..')