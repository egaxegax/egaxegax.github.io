#!python
#
# list files and folders
#
# list_files.py <path_to_files>

import sys, os, time, json, re

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
        ftime = time.mktime(time.strptime(name[:-4], '%y_%m_%d_%H_%M_%S'))
      elif cwd in ('posts', 'songs'):
        f = open(os.path.join(root, name))
        ftime = os.path.getmtime(os.path.join(root, name))
        for line in f:
          if fname != 'about':
            print( fname )
            ftime = time.mktime(time.strptime(line[line.find('<!--')+4:][:19].strip('->'), '%Y-%m-%d %H:%M:%S'))
          break

      mfiles.append([ subj, title, int(time.strftime('%y%m%d%H%M%S', time.localtime(ftime))) ]) 

mfiles.sort(key=lambda f: f[2], reverse=True)
msubj = []
mtitles = []

for i, f in enumerate(mfiles):
  if f[1] == 'about':
    continue
  isubj = -1
  for ii, s in enumerate(msubj):
    if f[0] == s[0]:
      s[1] += 1
      isubj = ii
      break
  if isubj == -1:
    msubj += [[f[0], 1, f[2]]]
    isubj = len(msubj) - 1
  mtitles += [[isubj, len(mfiles) - len(mtitles), f[1], f[2]]]
  print( i )

def compact(s):
  s = re.sub(r'([\[,\]]+)\s*\n','\g<1>',s)
  s = s.replace('\n],[','],\n[').replace('[[','[\n[').replace('\n]]',']\n]')
  return s

open('index.js', 'wb').write('SUBJ=' + compact(json.dumps(msubj, indent=0, ensure_ascii=0)) + ';\n')
open('index.js', 'ab').write('TITLES=' + compact(json.dumps(mtitles, indent=0, ensure_ascii=0)) + ';')
time.sleep(1)

try:
  import subprocess
  if os.name == 'nt':
    os.putenv('PATH', '"c:/program files/git/bin"')
  if gitskip == 0: gitskip = subprocess.call('git add *.txt *.js *.html', shell=True)
  comment = '++' + os.path.basename(os.getcwd())
#  if gitskip == 0: raw_input(comment + ' Continue commit and push to github.com?')
  if gitskip == 0: gitskip = subprocess.call('git config --global user.email egax@ya.ru', shell=True)
  if gitskip == 0: gitskip = subprocess.call('git config --global user.name  egax', shell=True)
  if gitskip == 0: gitskip = subprocess.call('git config core.fileMode false', shell=True)
  if gitskip == 0: gitskip = subprocess.call('git commit -m "' + comment + '"', shell=True)
  if gitskip == 0: gitskip = subprocess.call('git push origin master', shell=True)
except:
  raise
