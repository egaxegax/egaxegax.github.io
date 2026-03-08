#!/usr/bin/python3
#
# Extract README to .md files in dir.
#
# python3 ../updatelist.py <dir> (from books, posts, songs)
#

import re, os, sys

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

def tr_chars(value, max_length, send='...'):
    """Truncate string to MAX_LENGTH words"""
    if len(value) > max_length:
        truncd_val = value[:max_length]
        if not len(value) == max_length+1 and value[max_length+1] != ' ':
            truncd_val = truncd_val[:truncd_val.rfind(' ')]
        return truncd_val + send
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

def main(path='.', dir='.'):
  cwd = os.path.basename(os.getcwd())
  count = 0

  for root, dirs, files in os.walk(dir, topdown=False):
    if root in ('.git',):
      # print(root, '...skip')
      continue

    for name in files:
      print(name, 'cwd', cwd)
      if name in ('README',) and cwd in ('books', 'foto', 'posts', 'songs'):
        with open(os.path.join(root, name)) as f:
          for item in [item for item in re.split('<!---->', f.read()) if item]:
            m = re.search(r'<!--n:(.+):s:(\d+):e:(\d+)-->', item)
            try:    print(root, name, m.group())
            except: print(root, name, '\n', item); raise
            with open(os.path.join(root, m.group(1)+'.md'), 'w') as ff:
              ff.write(item[:-(len(m.group())+1)])
            count += 1
        os.remove(os.path.join(root, name))
  
  print('Extracted:', count)

if __name__ == '__main__':
  main(*sys.argv)