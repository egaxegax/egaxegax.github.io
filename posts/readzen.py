#!python3
#
# Parse dzen.ru .json feed page to .md
#

import os, sys, datetime, time
import json
from urllib.request import Request, urlopen

cdir = os.path.dirname(__file__)

sys.path.insert(0, cdir+'/..')
from update import main as update_main
from updatelist import main as updatelist_main, tr, tr_chars, tr_cut
from updaterssd import main as updaterss_main

total = 15
fcount = 0
cdtm = time.localtime()

hdr = 'Подборка с сайтов/Дзен'
feedurl = 'https://dzen.ru/api/v3/launcher/export?clid=300&country_code=ru'

with urlopen(Request(feedurl, headers={'User-Agent': 'Mozilla/5.0'})) as purl:
  for item in [item for ii, item in enumerate(json.loads(purl.read())['items']) if ii < total and item['text']]:
    titl = item['title']
    link = item['link'].split('?')[0]
    authr = item['domain_title']
    imurl = item['image']
    text = item['text']
    mtitl = tr_cut(titl)
    # phref = '/index.html?'+ tr(os.path.basename(hdr)) +'/'+ tr(mtitl)
    udate = item['publication_date']
    pdt = datetime.datetime.fromtimestamp(int(udate))
    rdate = pdt.strftime('%Y-%m-%d')
    ctime = pdt.strftime('<!--%Y-%m-%d %H:%M:%S-->')
    # ctime = time.strftime('<!--{y}-{m}-{d} 14:00:{c}-->'.format(y=time.strftime('%Y', cdtm), m=('%02d' % cdtm.tm_mon), d=('%02d' % cdtm.tm_mday), c=('%02d' % fcount)))
    text = """{ctime}
<div class="yb">
  <div class="inlbl text">
  <p class="table preview">
    <a class="trow nodecor" href="{link}">
      <img src="{imurl}" alt="">
    </a>
    <a class="trow nodecor" href="{link}"><span class="inlbl">{titl}</span></a>
    <i class="trow smaller2"><span class="inlbl">{authr}</span></i>
    <i class="trow smaller3">{rdate}</i>
  </p>
  </div>
  <div class="inlbl text smaller1">{text}</div>
</div>
""".format(ctime=ctime, link=link, imurl=imurl, rdate=rdate, titl=tr_chars(titl, 80), authr=authr, text=text)
    if not os.path.exists(os.path.join(cdir, os.path.dirname(hdr))):
      os.mkdir(os.path.join(cdir, os.path.dirname(hdr)))
    if not os.path.exists(os.path.join(cdir, hdr)):
      os.mkdir(os.path.join(cdir, hdr))
    open(os.path.join(cdir, hdr, mtitl + '.md'), 'w', encoding='utf-8', newline='\n').write(text)
    fcount += 1
  print(hdr, '(%s)' % (fcount,))

if fcount:
  time.sleep(1)
  update_main(cdir)
  updatelist_main(cdir)
  updateturbo_main(cdir)
  