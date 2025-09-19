#!/usr/bin/python3
#
# Make README.md files with list of files in run dir.
#
# python3 ../updatelist.py (from songs, posts)
#

import re, os, sys
from urllib.parse import urlencode

def E_OS(text):
  return text

def tr(t):
  """Transliterate string"""
  ru = {
    'а':'a', 'б':'b', 'в':'v', 'г':'g', 'д':'d', 'е':'e', 'ё':'e', 
    'ж':'j', 'з':'z', 'и':'i', 'й':'j', 'к':'k', 'л':'l', 'м':'m', 
    'н':'n', 'о':'o', 'п':'p', 'р':'r', 'с':'s', 'т':'t', 'у':'u', 
    'ф':'f', 'х':'h', 'ц':'c', 'ч':'ch', 'ш':'sh', 'щ':'shch', 
    'ы':'y', 'ъ':'', 'ь':'', 'э':'e', 'ю':'ju', 'я':'ya'
  }
  tr = []
  t = tr_cut(t)
  t = re.sub(r'\s+','_',t)
  for s in t:
    tr.append( ru.get( s ) or ru.get( s.lower(), s ) )
  return ''.join(tr).lower()

def tr_chars(value, max_length):
    """Truncate string to MAX_LENGTH words"""
    if len(value) > max_length:
        truncd_val = value[:max_length]
        if not len(value) == max_length+1 and value[max_length+1] != ' ':
            truncd_val = truncd_val[:truncd_val.rfind(' ')]
        return truncd_val + '...'
    return value

def tr_cut(t):
  """Remove from string cyrillic and special chars"""
  tr = []
  for ch in t:
    if ch.lower() in ' -_абвгдеёжзийклмнопрстуфхцчшщыъьэюяabcdefghjijklmnopqrstuvwxyz0123456789':
      tr.append( ch )
    else:
      tr.append(' ')
  t = ''.join(tr)
  t = re.sub('\s+',' ',t)
  t = t.strip()
  return t

def tr_url(text):
  """Urlencode string"""
  return text.replace(' ', '%20')

def main(path='.'):
  cwd = os.path.basename(os.path.abspath(path))

  for root, dirs, files in os.walk(path, topdown=False):
    ititles = []
    files.sort()

    roots = E_OS(os.path.basename(os.path.dirname(root)))
    subj = E_OS(os.path.basename(root))

    if root in ('.git',):
      print('SKIP', root)
      continue

    about = ''
    for name in files:
      fname, ext = os.path.splitext(name)
      title = E_OS(fname)

      if name in ('README.md',):
        continue

      if cwd in ('books', 'foto', 'posts', 'songs', 'vesti') and ext in ('.md',):
        if fname == 'about':
          text = open(os.path.join(root, name), encoding='utf-8', newline='\n').read()
          about = text.strip() + '\n\n'      # save about text
      elif cwd in ('foto'):
        pass
      else:
        continue

      lntit = '[' + title + '](' + tr_url(title) + ext + ')'
      if fname == 'about': # +about text
        text = re.sub('(^<\!--.*-->)\s*', '', text)
        ititles = [text + '\n'] + ititles
      else:
        if os.path.isfile(os.path.join(root, title + '.jpg')): # image in books, foto
          ititles.append('![](' + tr_url(title) + '.jpg' + ')  \n' + lntit + '\n')
        else:
          ititles.append('* ' + lntit)

      print(roots, subj, name)

    if ititles: # titles list
      text = ''
      if os.path.isfile(os.path.join(root, tr(subj) + '.jpg')):
        text = '![](' + tr(subj) + '.jpg' + ')\n\n'
      text += '\n'.join(ititles)
      open(os.path.join(root, 'README.md'), 'w', encoding='utf-8', newline='\n').write(text)

    if dirs: # subdirs list
      isubj = []
      dirs.sort()
      for name in dirs:
        if name not in ('.git', 'th', '_layouts'): # skip dir
          isubj.append( '* [' + name + '](' + tr_url(name) + ')' )
      text = '\n'.join(isubj)
      if text:
        open(os.path.join(root, 'README.md'), 'w', encoding='utf-8', newline='\n').write(about + text)

if __name__ == '__main__':
  main()