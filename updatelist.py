#!/usr/bin/python
#
# Make README.md files with list of dir files.
# Convert song .txt files to .md from current dir.
#
# python ../updatelist.py (from songs, posts, vesti)
#

import re
import os
import sys

def E_OS(text):
  return text

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
  t = re.sub(r'[ъь\'"`\(\)\.,%]+','',t)
  t = re.sub(r'\s','_',t)
  for s in t:
    tr.append( ru.get( s ) or ru.get( s.lower(), s ) )
  return ''.join(tr).lower()

def SP(text):
  return text.replace(' ', '%20')

path = '.'
cwd = os.path.basename(os.getcwd())

for root, dirs, files in os.walk(path, topdown=False):
  ititles = []
  files.sort()

  roots = E_OS(os.path.basename(os.path.dirname(root)))
  subj = E_OS(os.path.basename(root))

  if '.git' in root:
    continue

  about = ''
  for name in files:
    fname, ext = os.path.splitext(name)
    title = E_OS(fname)

    if name in ('README.md', 'sitemap.txt'):
      continue

    if cwd in ('books', 'foto', 'posts', 'songs', 'vesti') and ext in ('.md',):
      if fname == 'about':
        text = open(os.path.join(root, name), encoding='utf-8', newline='\n').read()
        about = text.strip() + '\n\n'      # save about text
    elif cwd in ('foto'):
      pass
    else:
      continue

    lntit = '[' + title + '](' + SP(title) + ext + ')'
    if fname == 'about': # +about text
      text = re.sub('(^<\!--.*-->)\s*', '', text)
      ititles = [text + '\n'] + ititles
    else:
      if os.path.isfile(os.path.join(root, title + '.jpg')): # exists book image
        ititles.append('![](' + SP(title) + '.jpg' + ')  \n' + lntit + '\n')
      else:
        ititles.append('* ' + lntit)

    print(roots, subj, name)      

  if ititles: # titles list
    text = ''
    if os.path.isfile(os.path.join(root, TR(subj) + '.jpg')):
      text = '![](' + TR(subj) + '.jpg' + ')\n\n'
    text += '\n'.join(ititles)
    open(os.path.join(root, 'README.md'), 'w', encoding='utf-8', newline='\n').write(text)

  if dirs: # subdirs list
    isubj = []
    dirs.sort()
    for name in dirs:
      if name not in ('.git', 'th', '_layouts'): # skip dir
        isubj.append( '* [' + name + '](' + SP(name) + ')' )
    text = '\n'.join(isubj)
    if text:
      open(os.path.join(root, 'README.md'), 'w', encoding='utf-8', newline='\n').write(about + text)
