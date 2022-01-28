#!/usr/bin/python
#
# Make index.md files with list of dir files.
# Convert song .txt files to .md from current dir.
#
# python ../list.py
#

import re
import os
import sys

def E_OS(text):
  if os.name == 'nt':
    return text.decode('cp1251').encode('utf-8')
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

  for name in files:
    fname, ext = os.path.splitext(name)
    title = E_OS(fname)

    if name in ('index.md', 'sitemap.txt'):
      continue

    if cwd in ('songs',) and ext in ('.txt',):
      text = open(os.path.join(root, name)).read()
      text = re.sub('[\t ]*\n', '\n', text)
      text = re.sub('(^|\n)!([\t ]*)(.*)', r'\1\2*\3*', text)
      text = re.sub('(^|\n)>([\t ]*)(.*)', r'\1\2***\3***', text)
      text = re.sub('<([\t ]*)([^!>]*)([\t ]*)>', r'\1***\2***\3', text)
      text = re.sub('^[\r\n]+|[\r\n]+$', '', text)
      text = re.sub('\r', '', text)
      text = re.sub('\t', ' ', text)
      text = re.sub(' ', r' ', text)  # en space
      text = re.sub('\n', '  \n', text) # two spaces newline
      text = re.sub('(^<\!--.*-->)\s*', r'\1\n', text) # revert comments
      open(os.path.join(root, fname + '.md'), 'w').write(text)
    elif cwd in ('books', 'posts', 'songs', 'vesti') and ext in ('.md',):
      if fname == 'about':
        text = open(os.path.join(root, name)).read()
    else:
      continue

    lntit = '[' + title + '](' + os.path.normpath(os.path.join('/', cwd, roots, SP(subj), SP(title))) + ')'
    if fname == 'about': # +about text
      text = re.sub('(^<\!--.*-->)', '', text)
      ititles = [text + '\n'] + ititles
    else:
      if os.path.isfile(os.path.join(root, title + '.jpg')): # exists book image
        ititles.append('* ![](' + os.path.normpath(os.path.join('/', cwd, roots, SP(subj), SP(title) + '.jpg')) + ') ' + lntit)
      else:
        ititles.append('* ' + lntit)

    print(roots, subj, name)      

  if ititles: # titles list
    text = ''
    if os.path.isfile(os.path.join(root, TR(subj) + '.jpg')):
      text = '![](' + os.path.normpath(os.path.join('/', cwd, roots, SP(subj), TR(subj) + '.jpg')) + ')  \n'
    text += '\n'.join(ititles)
    open(os.path.join(root, 'index.md'), 'w').write(text)

  if dirs: # subdirs list
    isubj = []
    dirs.sort()
    for name in dirs:
      if name != '.git':
        isubj.append( '* [' + name + '](' + os.path.normpath(os.path.join('/', cwd, subj, SP(name))) + ')' )
    text = '\n'.join(isubj)
    open(os.path.join(root, 'index.md'), 'w').write(text)
