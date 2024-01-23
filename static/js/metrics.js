//
// make metrics, counters, ads
//
if(!String(window.location).match(/file:|localhost|127.0.0.1/)){
{ // LiveInternet metrica
  (function(d,s){if(d.getElementById('licntADF8'))d.getElementById('licntADF8').src='//counter.yadro.ru/hit?t45.12;r'+escape(d.referrer)+
  ((typeof(s)=='undefined')?'':';s'+s.width+'*'+s.height+'*'+(s.colorDepth?s.colorDepth:s.pixelDepth))+';u'+escape(d.URL)+
  ';h'+escape(d.title.substring(0,150))+';'+Math.random();})(document,screen);
}
{ // Yandex metrica
  (function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments);};
   m[i].l=1*new Date();k=e.createElement(t),a=e.getElementsByTagName(t)[0];k.async=1;k.src=r;a.parentNode.insertBefore(k,a);})
   (window, document, 'script', '//mc.yandex.ru/metrika/tag.js', 'ym');
   ym(65044687, 'init', {
     clickmap:true,
     trackLinks:true,
     accurateTrackBounce:true
   });
}
{ // Google Analytics 
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments);},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m);
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');
  ga('create', 'UA-25857345-4', 'egaxegax.github.io');
  ga('send', 'pageview');
}
{ // Rambler top 100 counter
//  (function (w, d, c) {
//  (w[c] = w[c] || []).push(function() {
//      var options = {project: 7715588};
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
}
{ // Google Adsense
//  (function(m,e,t,r,i,k,a){m[i]=m[i]||[];
//   m[i].l=1*new Date();k=e.createElement(t),a=document.head;k.async=1;k.crossorigin='anonymous';k.src=r;a.appendChild(k);})
//   (window, document, 'script', '//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2243951601941043', 'googleContextCb');
}
{ // Yandex reklama
  (function(m,e,t,r,i,k,a){m[i]=m[i]||[];
   m[i].l=1*new Date();k=e.createElement(t),a=e.getElementsByTagName(t)[0];k.async=1;k.src=r;a.parentNode.insertBefore(k,a);})
   (window, document, 'script', '//yandex.ru/ads/system/context.js', 'yaContextCb');
  window.YA_RTB = {1:1, 2:2, 3:3, 4:9, 5:10, 6:11, 7:13};
  window.YA_TMR = [];
  window.addYaRTB_Block = function(blid,p_dark,rtbid){ 
    function ads(){ if(document.getElementById('yandex_rtb_'+blid)){ 
      window.yaContextCb.push(function(){Ya.Context.AdvManager.render({darkTheme:p_dark, blockId:'R-A-2277013-'+(rtbid||blid), renderTo:'yandex_rtb_'+blid});});
    }};
    while(YA_TMR.length) clearInterval(YA_TMR.pop());
    YA_TMR.push( setInterval(ads, (Math.random()*20+9)*1000));
    ads();
  };
  var sp = [].slice.call(document.getElementsByTagName('script')).filter(function(s){return s.src.indexOf('metrics.js')>-1;})[0];
  var p_dark = Number((sp.getAttribute('data-dark') == null) ? 0 : sp.getAttribute('data-dark'));
  var p_floor = Number((sp.getAttribute('data-floor') == null) ? 0 : sp.getAttribute('data-floor'));
  var p_top = Number((sp.getAttribute('data-top') == null) ? 0 : sp.getAttribute('data-top'));
  var p_full = Number((sp.getAttribute('data-full') == null) ? 0 : sp.getAttribute('data-full'));
  console.log('p_floor', p_floor, 'p_top', p_top, 'p_full', p_full);
  if(p_floor) window.yaContextCb.push(function(){Ya.Context.AdvManager.render({darkTheme:p_dark, blockId:'R-A-2277013-5', type:'floorAd'});});
  if(p_floor) window.yaContextCb.push(function(){Ya.Context.AdvManager.render({darkTheme:p_dark, blockId:'R-A-2277013-12', type:'floorAd', platform:'desktop'});});
  if(p_top) window.yaContextCb.push(function(){Ya.Context.AdvManager.render({darkTheme:p_dark, blockId:'R-A-2277013-7', type:'topAd'});});
  if(p_full) window.yaContextCb.push(function(){Ya.Context.AdvManager.render({darkTheme:p_dark, blockId:'R-A-2277013-8', type:'fullscreen', platform:'touch'});});
}
{ // VK reklama
  (function(m,e,t,r,i,k,a){m[i]=m[i]||[];
   m[i].l=1*new Date();k=e.createElement(t),a=e.getElementsByTagName(t)[0];k.async=1;k.src=r;a.parentNode.insertBefore(k,a);})
   (window, document, 'script', '//ad.mail.ru/static/ads-async.js', 'MRGtag');
  window.VK_RTB = {1:1490223, 2:1490225, 3:1490227};
  window.VK_TMR = [];
  window.addVkRTB_Block = function(rtbid){ 
    function ads(){ 
      (MRGtag = window.MRGtag || []).push({});
    };
    while(VK_TMR.length) clearInterval(VK_TMR.pop());
    VK_TMR.push( setInterval(ads, (Math.random()*20+9)*1000));
    ads();
    return ' data-ad-client="ad-'+rtbid+'" data-ad-slot="'+rtbid+'" ';
  };
}
}
