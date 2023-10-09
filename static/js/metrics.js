//
// Add metrics, counters
//
if(!String(window.location).match(/file:|localhost|127.0.0.1/)){
{ // liveinternet metrics
  (function(d,s){if(d.getElementById('licntADF8'))d.getElementById('licntADF8').src='//counter.yadro.ru/hit?t45.12;r'+escape(d.referrer)+
  ((typeof(s)=='undefined')?'':';s'+s.width+'*'+s.height+'*'+(s.colorDepth?s.colorDepth:s.pixelDepth))+';u'+escape(d.URL)+
  ';h'+escape(d.title.substring(0,150))+';'+Math.random();})(document,screen);
}
{ // yandex metrics
  (function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments);};
   m[i].l=1*new Date();k=e.createElement(t),a=e.getElementsByTagName(t)[0];k.async=1;k.src=r;a.parentNode.insertBefore(k,a);})
   (window, document, 'script', '//mc.yandex.ru/metrika/tag.js', 'ym');
   ym(65044687, 'init', {
     clickmap:true,
     trackLinks:true,
     accurateTrackBounce:true
   });
}
{ // google analytics
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments);},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m);
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');
  ga('create', 'UA-25857345-4', 'egaxegax.github.io');
  ga('send', 'pageview');
}
//{ // rambler top 100 counter
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
//}
//{ // google adsense
//  (function(m,e,t,r,i,k,a){m[i]=m[i]||[];
//   m[i].l=1*new Date();k=e.createElement(t),a=document.head;k.async=1;k.crossorigin='anonymous';k.src=r;a.appendChild(k);})
//   (window, document, 'script', '//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2243951601941043', 'googleContextCb');
//}
{ // reklama Yandex.RTB
  (function(m,e,t,r,i,k,a){m[i]=m[i]||[];
   m[i].l=1*new Date();k=e.createElement(t),a=e.getElementsByTagName(t)[0];k.async=1;k.src=r;a.parentNode.insertBefore(k,a);})
   (window, document, 'script', '//yandex.ru/ads/system/context.js', 'yaContextCb');
  window.adjustRtbHeight = function(){ // fix Yandex.RTB block height
    var elem, hsum = 0;
    [1,2,3].map(function(i){
      if(elem = document.getElementById('yandex_rtb_R-A-2277013-'+i)){
        elem.style.height = (elem.style.maxHeight || window.getComputedStyle(elem).getPropertyValue('max-height'));
        hsum += elem.offsetHeight;
      }
    });
    return hsum;
  };
  window.addYaRTB_Block = function(n,p_dark){ 
    if(document.getElementById('yandex_rtb_R-A-2277013-'+n)) window.yaContextCb.push(function(){Ya.Context.AdvManager.render({darkTheme: p_dark, blockId:'R-A-2277013-'+n, renderTo:'yandex_rtb_R-A-2277013-'+n});});
    else if(document.getElementById('yandex_rtb_C-A-2277013-'+n)) window.yaContextCb.push(function(){Ya.Context.AdvManager.renderWidget({darkTheme: p_dark, blockId:'C-A-2277013-'+n, renderTo:'yandex_rtb_C-A-2277013-'+n});});
  };
  addYaRTB_Block(1);
  addYaRTB_Block(2);
  addYaRTB_Block(3);
  addYaRTB_Block(4);
  var sp = [].slice.call(document.getElementsByTagName('script')).filter(function(s){return s.src.indexOf('metrics.js')>-1;})[0];
  var p_floor = Number((sp.getAttribute('data-floor') == null) ? 0 : sp.getAttribute('data-floor'));
  var p_top = Number((sp.getAttribute('data-top') == null) ? 0 : sp.getAttribute('data-top'));
  var p_full = Number((sp.getAttribute('data-full') == null) ? 0 : sp.getAttribute('data-full'));
  console.log('p_full', p_full, 'p_floor', p_floor, 'p_top', p_top);
  if(p_floor) window.yaContextCb.push(function(){Ya.Context.AdvManager.render({blockId: 'R-A-2277013-5', type: 'floorAd'});});
  if(p_top) window.yaContextCb.push(function(){Ya.Context.AdvManager.render({blockId: 'R-A-2277013-7', type: 'topAd'});});
  if(p_full) window.yaContextCb.push(function(){Ya.Context.AdvManager.render({blockId: 'R-A-2277013-8', type: 'fullscreen', platform: 'touch'});});
}
}
