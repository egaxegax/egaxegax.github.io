#!/usr/bin/python3
#
# Extract README to .md files in dir.
#
# python3 updatelist.py [dir]
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
  t = re.sub(r'[\(\)\.,]+',' ',t).strip()
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
    if ch.lower() in r' \'`().,-_абвгдеёжзийклмнопрстуфхцчшщыъьэюяabcdefghjijklmnopqrstuvwxyz0123456789':
      tr.append( ch )
    else:
      tr.append(' ')
  t = ''.join(tr)
  t = re.sub(r'\s+',' ',t)
  t = t.strip()
  return t

def tr_url(text):
  """Urlencode string"""
  return text.replace(' ', '%20')

def main(path='.', cwd='', count=0, count_noim=0):
  if not cwd: cwd = os.path.normpath(path).split('/')[0]
  for root, dirs, files in os.walk(path, topdown=False):
    for name in files:
      if 'README' in name and cwd in ('books', 'foto', 'fotosite', 'posts', 'songs'):
        with open(os.path.join(root, name), encoding='utf-8', newline='\n') as f:
          for item in [item for item in re.split('<!---->', f.read()) if item]:
            m = re.search(r'<!--n:(.+):s:(\d+):e:(\d+)-->', item)
            try:    subj, titl = m.group(1).split('/')
            except: subj = '' ; print(root, name, '\n', item); titl = m.group(1)
            os.makedirs(os.path.join(root, subj), exist_ok=True)
            with open(os.path.join(root, subj, tr_cut(titl)+'.md'), 'w', encoding='utf-8', newline='\n') as ff:
              ff.write(item[:-(len(m.group())+1)])
            # if cwd in ('books',):
            #   try:
            #     import io, base64
            #     from PIL import Image
            #     m = re.search(r'<!--cover:([^>]*)-->', item)
            #     im = Image.open(io.BytesIO(base64.b64decode(m.group(1))))
            #     im_rgb = im.convert('RGB')
            #     im_rgb.thumbnail((240,240))
            #     buffer = os.path.join(root, subj, tr_cut(titl)+'.jpg')
            #     im_rgb.save(buffer, format='JPEG')
            #   except:
            #     print('No image:', count_noim, ff)
            #     count_noim += 1
            count += 1
        os.remove(os.path.join(root, name))
  print('Extracted:', count)

if __name__ == '__main__':
  if sys.argv[1:]: main(*sys.argv[1:])
  else:            main(os.getcwd(), os.path.basename(os.getcwd()))
