#!/usr/bin/python3
#
# Update Dzen RSS page in {songs, posts} dir
#
# python3 ../updaterssd.py (gen rss-dzen.xml)
#

import sys, os, io, time, re
from updatelist import tr, tr_cut

surls = {'egax.ru':'', 'egaxegax.github.io':'1'}

def main(path='.', icount=0, surl='egax.ru', sdir='', chadult='nonadult'):
  icount = int(icount)
  if icount and icount < 100: 
    raise Exception('icount < 100 !!!')
  cwd = os.path.basename(os.path.abspath(path))
  sind = cwd
  if sind == 'posts':
    sind = 'index'
  chtitl = {'books': 'Книги', 'foto':'Фото', 'posts': 'Подборка статей на разные темы', 'songs':'Аккорды и тексты песен'}.get(cwd, cwd)
  try:
    exec(open(os.path.join(path, 'index.js'), encoding='utf-8', newline='\n').read())
  except:
    raise

  roots = locals()['ROOTS']
  subjects = locals()['SUBJ']
  titles = locals()['TITLES']
  for i, part_titles in enumerate([titles[p:p + icount] for p in range(0, len(titles), icount)] if icount else [titles[:100]]):
    rcount = ('_'+ str(i) if icount else '')
    items = []
    for title in part_titles:
      subj = subjects[title[0]][0]
      root = roots[title[4]][0]
      mroot = ('' if cwd in ('books', 'songs', 'vesti') else root +' / ')
      troot = ('' if cwd in ('songs', 'vesti') else ' / '+ tr_cut(root))
      titl = title[2]
      ulink = ''
      pdt = time.strptime(str(title[3]), '%y%m%d%H%M%S')
      pdate = time.strftime('%a, %d %b %Y %H:%M:%S +0300', pdt)
      text = open(os.path.join(path, root, subj, titl+'.md'), encoding='utf-8', newline='\n').read()
      if cwd == 'songs': 
        import markdown
        text = markdown.markdown(text)
        mtext = '<p><img src="/'+ os.path.join(cwd, root, subj, tr(subj)+'.jpg') +'" alt=""></p>' if os.path.exists(os.path.join(path, root, subj, tr(subj)+'.jpg')) else ''
        text = mtext + text
        text = re.sub('<(/)?strong>', r'', text)
        text = re.sub('<(/)?em>', r'<\1b>', text)
        text = re.sub('<(/)?code>', r'', text)
        text = re.sub('<(/)?pre>', r'<\1blockquote>', text)
        text = re.sub('<br />', r'<p />', text)
        text = re.sub('<\!--.*-->', r'', text)
      if cwd == 'books':
        genres = {'adv_animal':'Природа и животные','adv_geo':'Путешествия и география','adv_history':'Исторические приключения','adv_indian':'Приключения про индейцев','adv_maritime':'Морские приключения','adventure':'Приключения','antique':'Старинная литература','antique_east':'Древневосточная литература','biogr_leaders':'Биографии','child_adv':'Детские приключения','child_prose':'Детская проза','children':'Детская литература','child_sf':'Детская фантастика','child_tale':'Сказка','city_fantasy':'Городское фэнтези','det_action':'Боевик','det_classic':'Классический детектив','det_crime':'Криминальный детектив','det_espionage':'Шпионский детектив','det_hard':'Крутой детектив','det_history':'Исторический детектив','det_police':'Полицейский детектив','detective':'Детектив','dramaturgy':'Драматургия','economics':'Экономика','fantasy_fight':'Боевое фэнтези','foreign_adventure':'Зарубежные приключения','foreign_contemporary':'Современная зарубежная литература','foreign_detective':'Зарубежные детективы','foreign_fantasy':'Зарубежное фэнтези','foreign_love':'Зарубежные любовные романы','foreign_sf':'Иностранная фантастика','home_cooking':'Домашняя кухня','home_crafts':'Хобби и ремёсла','home_diy':'Сделай сам','home_garden':'Садоводство','home_health':'Здоровое питание','home_pets':'Домашние животные','home_sex':'Эротика, Секс','home_sport':'Спорт, фитнес','humor_prose':'Юмористическая проза','literature_adv':'Приключения','literature_classics':'Классическая литература','literature_drama':'Драма','literature_history':'История','literature_political':'Политика','literature_western':'Вестерн','love_contemporary':'Современные любовные романы','love_detective':'Остросюжетные любовные романы','love_erotica':'Эротика ','love_hard':'Страстная эротика','love_history':'Исторические любовные романы','love_sf':'Любовная фантастика','love_short':'Короткие любовные романы','magician_book':'Магия, волшебство','nonf_biography':'Биографии и Мемуары','nonf_publicism':'Непубличная литература','other':'Прочее','poetry':'Поэзия','popadanec':'Попаданцы','prose':'Проза','prose_classic':'Классическая проза','prose_contemporary':'Современная проза','prose_counter':'Контркультура','prose_history':'Историческая проза','prose_military':'Военная проза','prose_rus_classic':'Русская классическая проза','prose_su_classics':'Советская классическая проза','ref_dict':'Словари','ref_encyc':'Энциклопедии','reference':'Справочная литература','religion_esoterics':'Эзотерика','religion_orthodoxy':'Ортодоксальные учения','religion_rel':'Религия','religion_self':'Самосовершенствование','religion':'Религиозная литература','romance_fantasy':'Рыцарское фэнтези','romance_sf':'Рыцарская фантастика','romance':'Рыцарский роман','russian_fantasy':'Русское фэнтези','science':'Наука','sci_cosmos':'Научный космос','sci_culture':'Научная культура','sci_history':'История','sci_linguistic':'Языкознание','sci_philosophy':'Философия','sci_phys':'Научная физика','sf_action':'Боевая фантастика','sf_cyberpunk':'Киберпанк','sf_detective':'Детективная фантастика','sf_epic':'Эпическая фантастика','sf_etc':'Разная фантастика','sf_fantasy':'Фэнтези','sf_fantasy_city':'Городское фэнтези','sf_heroic':'Героическая фантастика','sf_history_avant':'Историческая авантюра','sf_history':'Альтернативная история','sf_horror':'Ужасы и Мистика','sf_humor':'Юмористическая фантастика','sf_mystic':'Мистика','sf_social':'Социально-психологическая фантастика','sf_space':'Космическая фантастика','sf':'Научная Фантастика ','thriller':'Триллер','vampire_book':'Вампиры','unrecognised':'Без рубрики'}
        gtext = '<p>Жанр: <i>'+ genres.get(root, root) +'</i></p>'
        mtext = '<p><img src="/'+ os.path.join(cwd, root, subj, titl+'.jpg') +'" alt=""></p>' if os.path.exists(os.path.join(path, root, subj, titl+'.jpg')) else ''
        stext = '<p><a class="light" href="//yandex.ru/search/?text='+subj+' '+titl+' скачать читать "> Найти и читать... </a></p>'
        text = mtext + gtext + text + stext
        ulink = '/'+ tr(root)
      items.append("""
<item>
<title>{trsubj} - {trtitl}{troot}</title>
<link>https://{link}</link>
<guid>{guid}</guid>
<pubDate>{pdate}</pubDate><media:rating scheme="urn:simple">{chadult}</media:rating><category>comment-subscribers</category>
<content:encoded><![CDATA[<title>{trsubj} - {trtitl}{troot}</title><h1>{mroot}{subj}</h1><h2>{titl}</h2>{text}]]></content:encoded>
</item>""".format(mroot=mroot, subj=subj, titl=titl, troot=troot, trsubj=tr_cut(subj), trtitl=tr_cut(titl), guid=tr(subj) +'_'+ tr(titl) +ulink, link=surl +'/'+ sind +'.html?'+ tr(subj) +'/'+ tr(titl) +ulink, text=re.sub('\n\s*',' ',text), pdate=pdate, chadult=chadult))
  
    rsstext = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:media="http://search.yahoo.com/mrss/" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:georss="http://www.georss.org/georss">
<channel>
<title>{chtitl}</title>
<link>https://{surl}/{sind}.html</link><language>ru</language>{items}
</channel>
</rss>
""".format(surl=surl, sind=sind, chtitl=chtitl, items=''.join(items))

    io.open(os.path.join(sdir or path, 'rss-dzen'+surls.get(surl, '')+ rcount +'.xml'), 'w', encoding='utf-8', newline='\n').write(rsstext)
    print(os.path.join(sdir or path, 'rss-dzen'+surls.get(surl, '')+ rcount +'.xml'), len(items))

if __name__ == '__main__':
  main(*sys.argv[1:])