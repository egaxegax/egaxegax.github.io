#!/usr/bin/python3
#
# Remove files in folder by date filter.
#

import linecache, re, os, sys, time, datetime

def main(path='.', fcount=3, doremove=0):
  cwd = os.path.basename(os.path.abspath(path))

  for root, dirs, files in os.walk(path, topdown=False):
    # files.sort()
    roots = (os.path.basename(os.path.dirname(root)))
    subj = (os.path.basename(root))
    dts = {}

    if root in ('.git',):
      print('SKIP', root)
      continue

    for name in files:
      fname, ext = os.path.splitext(name)

      if name in ('README.md', 'about.md'):
        continue

      if ext in ('.md',):
        ftime = os.path.getmtime(os.path.join(root, name))
        line = linecache.getline(os.path.join(root, name), 1)
        if re.search(r'^\d+-\d+-\d+\s\d+:\d+:\d+', line[line.find('<!--')+4:][:19].strip('->')):
          ftime = time.mktime(time.strptime(line[line.find('<!--')+4:][:19].strip('->'), '%Y-%m-%d %H:%M:%S'))
        elif re.search(r'^\d{2}\d{2}\d{2} \d{2}\d{2}', name[:11]):
          ftime = time.mktime(time.strptime(name[:11], '%y%m%d %H%M'))
        else:
          raise ValueError(root, name, line)
        
        dtime = datetime.datetime.fromtimestamp(ftime).date()

        if not cwd in dts: dts[cwd] = {}
        if not dtime in dts[cwd]: dts[cwd][dtime] = []
        dts[cwd][dtime].append( os.path.join(root, name) )
    
    ii = 0
    for cwd, v in dts.items():
      for dt, files in dict(sorted(v.items())).items():
        for fn in files[int(fcount):]:
          print(ii, cwd, dt, fn)
          ii += 1
          if doremove: os.remove(fn)

if __name__ == '__main__':
  main(*sys.argv[1:])