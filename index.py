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
      cwd = os.path.basename(os.getcwd())

      if cwd == 'news':
        ftime = time.mktime(time.strptime(name[:-4], '%Y_%m_%d_%H_%M_%S'))
      elif cwd == 'posts':
        f = open(os.path.join(root, name))
        for line in f:
          if line.strip():
            try:
              ftime = time.mktime(time.strptime(line.strip('\xef\xbb\xbf<!-->\r\n'), '%Y-%m-%d %H:%M:%S'))
            except:
              ftime = None
              print fname, 'use None date'
          break
      else:
        ftime = os.path.getmtime(os.path.join(root, name))

      mfiles.append([ subj, title, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ftime)) ]) 

mfiles.sort(key=lambda x: x[2], reverse=True)
msubj = []
mtitles = []

for i, f in enumerate(mfiles):
  if not f[0] in msubj:
    msubj.append(f[0])
  if f[1] != 'about':
    mtitles += [['0' + str(msubj.index(f[0])), '1' + str(len(mtitles)), f[1], f[2]]]
  print( i )

msubj.sort()

open('index.js', 'w').write('SUBJ=' + json.dumps(msubj, indent=1, ensure_ascii=0) + ';\n')
open('index.js', 'a').write('TITLES=' + json.dumps(mtitles, indent=1, ensure_ascii=0) + ';')
time.sleep(1)

try:
  import subprocess
  if os.name == 'nt':
    os.putenv('PATH', '"c:/program files/git/bin"')
  if gitskip == 0: gitskip = subprocess.call('git add *.txt *.js *.html', shell=True)
  comment = '++' + os.path.basename(os.getcwd())
  if gitskip == 0: raw_input(comment + ' Continue commit and push to github.com?')
  if gitskip == 0: gitskip = subprocess.call('git config --global user.email egax@ya.ru', shell=True)
  if gitskip == 0: gitskip = subprocess.call('git config --global user.name  egax', shell=True)
  if gitskip == 0: gitskip = subprocess.call('git config core.fileMode false', shell=True)
  if gitskip == 0: gitskip = subprocess.call('git commit -m "' + comment + '"', shell=True)
  if gitskip == 0: gitskip = subprocess.call('git push origin master', shell=True)
except:
  raise
