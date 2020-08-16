#!python
#
# list files and folders
#
# list_files.py <path_to_files>

import sys, os, time, json

def E_OS(text):
  if os.name == 'nt':
    return text.decode('cp1251').encode('utf-8')
  return text

path = '.'
mcount = 0
mfiles = []
gitskip = 1

if len(sys.argv) > 1:
  gitskip = (sys.argv[1] != "1")

for root, dirs, files in os.walk(path, topdown=False):
  for name in files:

    fname, ext = os.path.splitext(name)
    
    if ext == '.txt':

      mcount += 1

      subj = E_OS(os.path.basename(root))
      title = E_OS(fname)
      if os.path.basename(os.getcwd()) == 'news':
        ftime = time.mktime(time.strptime(name[:-4], '%Y_%m_%d_%H_%M_%S'))
      else:
        ftime = os.path.getmtime(os.path.join(root, name))

      mfiles.append([ subj, title, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ftime)) ]) 

mfiles.sort(key=lambda x: x[2], reverse=True)
msubj = {}
mtitles = []

for i, f in enumerate(mfiles):
  skey = '0' + str(hash(f[0])).replace('-','0')
  if not msubj.has_key(skey):
     msubj[skey] = f[0]
  if f[1] != 'about':
    tkey = '1' + str(hash(f[1])).replace('-','0')
    mtitles += [[skey, tkey, f[1], f[2]]]
  print( i )

open('index.js', 'wb').write('SUBJ=' + json.dumps(msubj, indent=1, ensure_ascii=0) + ';\n')
open('index.js', 'ab').write('TITLES=' + json.dumps(mtitles, indent=1, ensure_ascii=0) + ';')
time.sleep(1)

try:
  import subprocess
  if os.name == 'nt':
    os.putenv('PATH', '"c:/program files/git/bin"')
  if gitskip == 0: gitskip = subprocess.call('git add *.txt', shell=True)
  comment = '++' + os.path.basename(os.getcwd())
  if gitskip == 0: raw_input(comment + ' Continue commit and push to github.com?')
  if gitskip == 0: gitskip = subprocess.call('git config --global user.email egax@ya.ru', shell=True)
  if gitskip == 0: gitskip = subprocess.call('git config --global user.name  egax', shell=True)
  if gitskip == 0: gitskip = subprocess.call('git config core.fileMode false', shell=True)
  if gitskip == 0: gitskip = subprocess.call('git commit -m "' + comment + '"', shell=True)
  if gitskip == 0: gitskip = subprocess.call('git push origin master', shell=True)
except:
  raise

raw_input('enter...')
