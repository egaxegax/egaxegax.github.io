#!/usr/bin/python
#
# Make index.md files with list of dir files.
# Convert song .txt files to .md from current dir.
#
# python list.py
#

import re
import os
import sys

def E_OS(text):
  if os.name == 'nt':
    return text.decode('cp1251').encode('utf-8')
  return text

def SP(text):
  return text.replace(' ', '%20')

path = '.'
cwd = os.path.basename(os.getcwd())

for root, dirs, files in os.walk(path, topdown=False):
  iroots = []
  ititles = []
  files.sort()

  roots = E_OS(os.path.basename(os.path.dirname(root)))
  subj = E_OS(os.path.basename(root))

  for name in files:
    fname, ext = os.path.splitext(name)
    title = E_OS(fname)

    if name in ('index.md', 'sitemap.txt'):
      continue

    if cwd in ('songs') and ext in ('.txt'):
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
    elif cwd in ('books', 'posts', 'vesti') and ext in ('.md'):
      if fname == 'about':
        text = open(os.path.join(root, name)).read()
    else:
      continue
      
    lntit = '[' + title + '](' + os.path.normpath(os.path.join('/', cwd, roots, SP(subj), SP(title))) + ')'
    if fname == 'about': # +about text
      text = re.sub('(^<\!--.*-->)', '', text)
      ititles = [text + '\n'] + ititles
    else:
      ititles.append('* ' + lntit)
    
    print(subj, name)      

  if ititles: # titles list
    text = ''
    if os.path.isfile(os.path.join(root, 'cover.jpg')):
      text = '![](' + os.path.normpath(os.path.join('/', cwd, roots, SP(subj), 'cover.jpg')) + ')  \n'
    text += '\n'.join(ititles)
    open(os.path.join(root, 'index.md'), 'w').write(text)

  if dirs: # subdirs list
    isubj = []
    dirs.sort()
    for name in dirs:
      isubj.append( '* [' + name + '](' + os.path.normpath(os.path.join('/', cwd, subj, SP(name))) + ')' )
    text = '\n'.join(isubj)
    if not os.path.isfile(os.path.join(root, 'index.md')):
      open(os.path.join(root, 'index.md'), 'w').write(text)
