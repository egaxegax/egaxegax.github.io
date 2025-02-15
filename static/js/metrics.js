//
// make metrics, counters, ads
//
if(!String(window.location).match(/file:|localhost|127.0.0.1/)){
{ // Mail.ru metrica
  (function (d,w,id) {
    (w._tmr = w._tmr || []).push({id:'3210527',type:'pageView',start:(new Date()).getTime()});
    if (d.getElementById(id)) return;
    var ts = d.createElement('script'); ts.type = 'text/javascript'; ts.async = true; ts.id = id;
    ts.src = '//top-fwz1.mail.ru/js/code.js';
    var f = function(){var s = d.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ts, s);};
    if (w.opera == '[object Opera]') { d.addEventListener('DOMContentLoaded', f, false); } else { f(); }
  })(document, window, 'tmr-code');
}
{ // Yandex metrica
  window.YandexRotorSettings={ WaiterEnabled:true, IsLoaded:function(){ return document.getElementById('page_content').innerHTML.length>100; }};
  setTimeout(function(e){ if(e=document.querySelector('img[data-cid="65044687"]')){
    (function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments);};
    m[i].l=1*new Date();k=e.createElement(t),a=e.getElementsByTagName(t)[0];k.async=1;k.src=r;a.parentNode.insertBefore(k,a);})
    (window, document, 'script', '//mc.yandex.ru/metrika/tag.js', 'ym');
    ym(65044687, 'init', { clickmap:true, trackLinks:true, accurateTrackBounce:true, webvisor:true });
    e.src = '//informer.yandex.ru/informer/65044687/3_1_FFFFFFFF_EFEFEFFF_0_pageviews';
  }},100);
}
//{ // Rambler top 100 counter
//  (function (w,d,c) {
//  (w[c] = w[c] || []).push(function() {
//      var options = {project:7715588};
//      try{w.top100Counter = new top100(options);} catch(e){}
//    });
//    var n = d.getElementsByTagName('script')[0],
//    s = d.createElement('script'),
//    f = function () { n.parentNode.insertBefore(s, n); };
//    s.type = 'text/javascript';
//    s.async = true;
//    s.src = 
//    (d.location.protocol == 'https:' ? 'https:' : 'http:') +
//    '//st.top100.ru/top100/top100.js';
//    if (w.opera == '[object Opera]') {
//      d.addEventListener('DOMContentLoaded', f, false);
//    } else { f(); }
//  })(window, document, '_top100q');
//}
{ // Google Analytics 
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
   (i[r].q=i[r].q||[]).push(arguments);},i[r].l=1*new Date();a=s.createElement(o),
   m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m);
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');
  ga('create', 'UA-25857345-4', 'egaxegax.github.io');
  ga('send', 'pageview');
}
//{ // Google Adsense
//  (function(m,e,t,r,i,k,a){m[i]=m[i]||[];
//   m[i].l=1*new Date();k=e.createElement(t),a=document.head;k.async=1;k.crossorigin='anonymous';k.src=r;a.appendChild(k);})
//  (window, document, 'script', '//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2243951601941043', 'googleContextCb');
//}
{ // Yandex reklama
  (function(m,e,t,r,i,k,a){m[i]=m[i]||[];
   m[i].l=1*new Date();k=e.createElement(t),a=e.getElementsByTagName(t)[0];k.async=1;k.src=r;a.parentNode.insertBefore(k,a);})
   (window, document, 'script', '//yandex.ru/ads/system/context.js', 'yaContextCb');
  window.YA_RTB = {1:3, 2:4, 3:5, 4:6, 5:7, 6:8, 7:9, feed:10, widget:11, inimage:12};
  window.YA_TMR = [];
  window.addYaRTB_Block = function(blid,rtbid,typ,p_dark){
    function ads(){ 
      function run(){ console.log(blid,rtbid,typ,p_dark);
        switch(typ){
        case 'flMob':  window.yaContextCb.push(function(){Ya.Context.AdvManager.render({darkTheme:p_dark, blockId:'R-A-7295044-'+rtbid, type:'floorAd'});}); break;
        case 'flDesk': window.yaContextCb.push(function(){Ya.Context.AdvManager.render({darkTheme:p_dark, blockId:'R-A-7295044-'+rtbid, type:'floorAd', platform:'desktop'});}); break;
        case 'fullMob':  window.yaContextCb.push(function(){Ya.Context.AdvManager.render({darkTheme:p_dark, blockId:'R-A-7295044-'+rtbid, type:'fullscreen', platform:'touch'});}); break;
        case 'inImg':  (function addInImage(images) {
                          if(!images.length) return;
                          const image = images.shift();
                          image.id = `ya_rtb_${blid}-${Math.random().toString(16).slice(2)}`;
                          // console.log(image);
                          window.yaContextCb.push(function(){Ya.Context.AdvManager.render({darkTheme:p_dark, blockId:'R-A-7295044-'+rtbid, renderTo:image.id, type:'inImage'});});
                          addInImage(images);
                        })(Array.from(document.getElementById('page_content').querySelectorAll('img'))); break;
        case 'widget': window.yaContextCb.push(function(){Ya.Context.AdvManager.renderWidget({darkTheme:p_dark, blockId:'C-A-7295044-'+rtbid, renderTo:blid});}); break;
        default:       window.yaContextCb.push(function(){Ya.Context.AdvManager.render({darkTheme:p_dark, blockId:'R-A-7295044-'+rtbid, renderTo:blid, type:typ});}); break;
      }}
      // run();
      if(!blid) run();
      else if(document.getElementById(blid))
        (new IntersectionObserver(function(es){ es.forEach(function(e){ if(e.isIntersecting){ run(); }}); },{threshold:0.9}).observe(document.getElementById(blid)));
    };
    while(YA_TMR.length) clearInterval(YA_TMR.pop());
    YA_TMR.push( setInterval(ads, (Math.random()*20+9)*1000) );
    setTimeout(ads);
  };
  [].slice.call(document.getElementsByTagName('script')).filter(function(s){return s.src.indexOf('metrics.js')>-1;}).map(function(sp){
    if(sp.getAttribute('data-floor')) addYaRTB_Block('', 1, 'flMob', sp.getAttribute('data-dark')!=null);
    if(sp.getAttribute('data-floordesk')) addYaRTB_Block('', 2, 'flDesk', sp.getAttribute('data-dark')!=null);
    if(sp.getAttribute('data-fullscr')) addYaRTB_Block('', 13, 'fullMob', sp.getAttribute('data-dark')!=null);
  });
}
{ // VK reklama
  (function(m,e,t,r,i,k,a){m[i]=m[i]||[];
   m[i].l=1*new Date();k=e.createElement(t),a=e.getElementsByTagName(t)[0];k.async=1;k.src=r;a.parentNode.insertBefore(k,a);})
   (window, document, 'script', '//ad.mail.ru/static/ads-async.js', 'MRGtag');
  window.VK_STS = ['https://egax.ru', 'https://egaxegax.github.io'];
  window.VK_RTB = {'0_1':1542915, '0_f':1768373, '0_c':1768394, '0_s':1768388, '0_240':1768926, '0_300':1774555, '0_32':1774906, '0_36':1779833,
                   '1_1':1490223, '1_f':1768405, '1_c':1772383, '1_s':1779837, '1_240':1772802, '1_300':1774557, '1_32':1774908, '1_36':1779835 };
  window.addVkRTB_Block = function(){ 
    (MRGtag = window.MRGtag || []).push({});
  };
}
{ // VK Widget Like
  (function(m,e,t,r,i,k,a){
    k=e.createElement(t),a=e.getElementsByTagName(t)[0];k.async=1;k.src=r;k.charset='windows-1251';a.parentNode.insertBefore(k,a);})
    (window, document, 'script', '//vk.com/js/api/openapi.js?168');
}
}
