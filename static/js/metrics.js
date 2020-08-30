//
// Add metrics, counters
//
function adLiveCounter(){
  document.getElementById('livecounter').innerHTML = 
'<a href="//www.liveinternet.ru/click" target="_blank"><img id="licntADF8" width="88" height="31" style="border:0" title="LiveInternet: показано число просмотров за 24 часа, посетителей за 24 часа и за сегодня" src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAEALAAAAAABAAEAAAIBTAA7" alt=""/></a>';
  (function(d,s){d.getElementById("licntADF8").src="//counter.yadro.ru/hit?t18.5;r"+escape(d.referrer)+
  ((typeof(s)=="undefined")?"":";s"+s.width+"*"+s.height+"*"+(s.colorDepth?s.colorDepth:s.pixelDepth))+";u"+escape(d.URL)+
  ";h"+escape(d.title.substring(0,150))+";"+Math.random()})(document,screen);
}
function adYaCounter(){
  document.getElementById('yacounter').innerHTML = 
'<a href="https://metrika.yandex.ru/stat/?id=65044687&amp;from=informer" target="_blank" rel="nofollow"><img src="https://informer.yandex.ru/informer/65044687/3_1_FFFFFFFF_EFEFEFFF_0_pageviews" style="width:88px; height:31px; border:0;" alt="Яндекс.Метрика" title="Яндекс.Метрика: данные за сегодня (просмотры, визиты и уникальные посетители)" class="ym-advanced-informer" data-cid="65044687" data-lang="ru" /></a>';
  (function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};
   m[i].l=1*new Date();k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})
   (window, document, "script", "https://mc.yandex.ru/metrika/tag.js", "ym");
   ym(65044687, "init", {
    clickmap:true,
    trackLinks:true,
    accurateTrackBounce:true
   });
}
function adGoogleCounter(){
  // Google Analytics
  let script = document.createElement('script');
  script.type = 'text/javascript';
  script.src  = 'https://www.googletagmanager.com/gtag/js?id=UA-25857345-4';
  document.head.appendChild(script);
  // ---------
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'UA-25857345-4');
}
  //
function addMetrics(){
  adLiveCounter();
  adYaCounter();
  adGoogleCounter();
}