(()=>{'use strict';
const root=document.documentElement;
root.classList.remove('travel-canonical-v3');
root.classList.add('travel-roadtrip-v2');
const commons='https://commons.wikimedia.org/wiki/Special:Redirect/file/';
const photo=(name,width=1200)=>`${commons}${encodeURIComponent(name)}?width=${width}`;
const photos=[
  ['Milan-duomo-front-facade.jpg','Фасад Міланського собору'],
  ['Galleria Vittorio Emanuele II, Milan, Italy.jpg','Galleria Vittorio Emanuele II'],
  ['Quartiere Brera.jpg','Вулиця в районі Brera'],
  ['Naviglio Grande canal Milan 2026.JPG','Канал Naviglio Grande'],
  ['Bosco verticale, Milan, Italy (Unsplash).jpg','Bosco Verticale'],
  ['Milan tram (232519688).jpg','Історичний трамвай у Мілані'],
  ['Milano, via Fiori Chiari 01.jpg','Via Fiori Chiari у Brera'],
  ['Naviglio Grande, Milano.jpg','Вечір біля Naviglio Grande']
];
const $=(sel,base=document)=>base.querySelector(sel);
const $$=(sel,base=document)=>Array.from(base.querySelectorAll(sel));
const txt=(sel,base)=>$(sel,base)?.textContent?.trim()||'';
const make=(tag,cls,text)=>{const el=document.createElement(tag);if(cls)el.className=cls;if(text!==undefined)el.textContent=text;return el};
const safeHref=raw=>{try{const u=new URL(raw,location.href);return ['https:','http:'].includes(u.protocol)?u.href:'#'}catch{return '#'}};
let source=$('#legacyTravelSource');
if(!source){
  source=make('div');source.id='legacyTravelSource';source.hidden=true;
  while(document.body.firstChild)source.append(document.body.firstChild);
  document.body.append(source);
}
let app=$('#roadtripApp');if(!app){app=make('div');app.id='roadtripApp';document.body.append(app)}
function originalTabs(){return $$('#dateTabs .tab,#variantTabs .tab',source)}
function selectedTabIndex(){const tabs=originalTabs();const i=tabs.findIndex(x=>x.getAttribute('aria-selected')==='true');return i>=0?i:0}
function collect(){
  const title=txt('#tripTitle',source)||txt('#pageTitle',source)||txt('h1',source)||'Мілан: мода, дизайн і італійський стиль';
  const subtitle=txt('#subtitle',source)||txt('#pageSubtitle',source)||'Міська подорож із модою, дизайном, Brera та Navigli.';
  const status=txt('#pageStatus',source)||txt('#statusPill',source)||'Кандидат · не заброньовано';
  const price=txt('#totalPrice',source)||txt('#budgetTotal',source)||'—';
  const perPerson=txt('#perPersonPrice',source);
  const dateTitle=txt('#selectedDateTitle',source)||txt('#heroDates',source)||originalTabs()[selectedTabIndex()]?.querySelector('strong')?.textContent?.trim()||'';
  const dateMeta=txt('#selectedDateMeta',source)||txt('#heroWorkdays',source)||'';
  const facts=$$('#heroFacts .fact-chip,.hero__quick strong',source).map(x=>x.textContent.trim()).filter(Boolean);
  const route=$$('#routeLine li',source).map(li=>({title:txt('strong',li),text:txt('span',li)})).filter(x=>x.title);
  const itinerary=$$('.day',source).map((d,i)=>({
    title:txt('.day-title strong',d)||txt('h3',d)||`День ${i+1}`,
    meta:txt('.day-title span',d)||txt('.eyebrow',d)||`День ${i+1}`,
    text:txt('.day-body p',d)||txt('.day-copy p:not(.eyebrow)',d)||txt('p',d),
    link:safeHref($('.day-actions a[href],.day-copy a[href]',d)?.getAttribute('href')||'#')
  })).filter(x=>x.title);
  const stays=$$('.stay',source).map((s,i)=>({
    title:txt('.stay-copy strong',s)||txt('h3',s)||`Варіант проживання ${i+1}`,
    text:txt('.stay-copy p',s)||txt('p',s),
    label:txt('.label-chip',s)||'Проживання',
    link:safeHref($('a[href]',s)?.getAttribute('href')||s.closest('a')?.getAttribute('href')||'#')
  })).filter(x=>x.title);
  const activities=$$('.activity',source).map((s,i)=>({
    title:txt('.activity-copy strong',s)||txt('h3',s)||`Активність ${i+1}`,
    text:txt('.activity-copy p',s)||txt('p',s),
    label:txt('.label-chip',s)||'Опціонально',
    link:safeHref($('a[href]',s)?.getAttribute('href')||s.closest('a')?.getAttribute('href')||'#')
  })).filter(x=>x.title);
  const budget=$$('#budgetBreakdown .budget-row,.cost-list .cost-row',source).map(row=>({label:row.children[0]?.textContent?.trim()||'',value:row.children[row.children.length-1]?.textContent?.trim()||''})).filter(x=>x.label);
  const included=$$('#included li',source).map(x=>x.textContent.trim()).filter(Boolean);
  const excluded=$$('#excluded li',source).map(x=>x.textContent.trim()).filter(Boolean);
  const practical=$$('#practical .practical-item',source).map(x=>({title:txt('strong',x),text:txt('p',x)})).filter(x=>x.title);
  const sources=$$('#sources .source',source).map(x=>({label:txt('strong',x),note:txt('small',x),href:safeHref($('a[href]',x)?.getAttribute('href')||'#')})).filter(x=>x.label);
  const primaryMap=safeHref($('#primaryActions a[href*="google.com/maps"],.day-actions a[href*="google.com/maps"]',source)?.getAttribute('href')||'https://www.google.com/maps/dir/?api=1&origin=Duomo+di+Milano&destination=Naviglio+Grande,+Milano&waypoints=Brera%7CVia+Monte+Napoleone%7CArmani%2FSilos&travelmode=walking');
  return {title,subtitle,status,price,perPerson,dateTitle,dateMeta,facts,route,itinerary,stays,activities,budget,included,excluded,practical,sources,primaryMap};
}
function imageEl(index,cls=''){const img=make('img',cls);img.src=photo(photos[index%photos.length][0],index===0?1600:900);img.alt=photos[index%photos.length][1];img.loading=index===0?'eager':'lazy';img.decoding='async';img.referrerPolicy='no-referrer';return img}
function sectionHead(kicker,title){const head=make('div','rt-section-head');head.append(make('p','rt-eyebrow',kicker),make('h2','',title));return head}
function render(){
  const d=collect();
  app.replaceChildren();
  const header=make('header','rt-site');
  const bar=make('div','rt-bar rt-wrap');bar.append(make('a','rt-logo','Travel route'));
  const nav=make('nav','rt-nav');[['Маршрут','#rt-route'],['Дні','#rt-days'],['Житло','#rt-stays']].forEach(([t,h])=>{const a=make('a','',t);a.href=h;nav.append(a)});bar.append(nav);header.append(bar);app.append(header);

  const hero=make('section','rt-hero');const grid=make('div','rt-hero-grid');for(let i=0;i<5;i++){const wrap=make('div',`rt-hero-photo rt-g${i+1}`);wrap.append(imageEl(i));grid.append(wrap)}hero.append(grid,make('div','rt-hero-badge',d.status),make('div','rt-hero-count','Мілан · 5 фото'));app.append(hero);

  const main=make('main','rt-wrap');
  const facts=make('div','rt-facts');(d.facts.length?d.facts:[d.dateTitle,d.dateMeta,'2 дорослих','малий рюкзак']).filter(Boolean).forEach(x=>facts.append(make('span','rt-fact',x)));main.append(facts);

  const overview=make('section','rt-overview');const intro=make('div','rt-intro');intro.append(make('p','rt-eyebrow','Італія · міська подорож'),make('h1','',d.title),make('p','rt-lead',d.subtitle));
  const price=make('div','rt-price-card');price.append(make('small','',d.dateTitle||'Обрані дати'),make('strong','',d.price),make('span','',d.perPerson||d.dateMeta));overview.append(intro,price);main.append(overview);

  const routeSec=make('section','rt-section');routeSec.id='rt-route';routeSec.append(sectionHead('Маршрут','Точки подорожі'));
  const routeTrack=make('div','rt-route-track');(d.route.length?d.route:[{title:'Duomo'},{title:'Brera'},{title:'Quadrilatero'},{title:'Tortona'},{title:'Navigli'}]).forEach((x,i)=>{const stop=make('div',`rt-stop${i===0?' active':''}`);stop.append(make('span','rt-dot'),make('strong','',x.title),make('small','',x.text||''));routeTrack.append(stop)});routeSec.append(routeTrack);main.append(routeSec);

  const gallery=make('section','rt-section');gallery.append(sectionHead('Враження','Мілан у кадрі'));const gg=make('div','rt-gallery');for(let i=0;i<8;i++)gg.append(imageEl(i));gallery.append(gg);main.append(gallery);

  const days=make('section','rt-section');days.id='rt-days';days.append(sectionHead('День за днем','Мініплан поїздки'));const timeline=make('div','rt-timeline');(d.itinerary.length?d.itinerary:[{title:'Duomo, Galleria та Brera',meta:'День 1',text:'Перше знайомство з містом.'},{title:'Модний квартал',meta:'День 2',text:'Palazzo Morando, Via della Spiga та Monte Napoleone.'},{title:'Armani, Tortona та Navigli',meta:'День 3',text:'Дизайн і вечір біля каналів.'}]).forEach((day,i)=>{const card=make('article','rt-day');card.dataset.day=String(i+1);const media=make('div','rt-day-media');media.append(imageEl(i+1));const copy=make('div','rt-day-copy');copy.append(make('p','rt-eyebrow',day.meta||`День ${i+1}`),make('h3','',day.title),make('p','',day.text));if(day.link&&day.link!=='#'){const a=make('a','rt-text-link','Маршрут у Google Maps ↗');a.href=day.link;a.target='_blank';a.rel='noopener noreferrer';copy.append(a)}card.append(media,copy);timeline.append(card)});days.append(timeline);main.append(days);

  const mapSec=make('section','rt-section rt-map-section');mapSec.append(sectionHead('Мапа','Маршрут у Мілані'));const mapCard=make('div','rt-map-card');const iframe=make('iframe','');iframe.title='Міні-мапа маршруту Міланом';iframe.loading='lazy';iframe.referrerPolicy='no-referrer';iframe.src='https://www.openstreetmap.org/export/embed.html?bbox=9.126%2C45.427%2C9.249%2C45.514&layer=mapnik&marker=45.4642%2C9.19';const mapBar=make('div','rt-map-bar');const mapCopy=make('div');mapCopy.append(make('strong','',d.route.map(x=>x.title).join(' → ')||'Duomo → Brera → Quadrilatero → Tortona → Navigli'),make('span','', 'Міні-мапа для орієнтації; точний пішохідний маршрут відкривається окремо.'));const mapLink=make('a','rt-btn','Відкрити Google Maps');mapLink.href=d.primaryMap;mapLink.target='_blank';mapLink.rel='noopener noreferrer';mapBar.append(mapCopy,mapLink);mapCard.append(iframe,mapBar);mapSec.append(mapCard);main.append(mapSec);

  if(d.stays.length){const stays=make('section','rt-section');stays.id='rt-stays';stays.append(sectionHead('Де зупинитися','Варіанти проживання'));const cards=make('div','rt-card-row');d.stays.slice(0,4).forEach((s,i)=>{const a=make('a','rt-card');a.href=s.link;a.target='_blank';a.rel='noopener noreferrer';a.append(imageEl(i+3));const c=make('div','rt-card-body');c.append(make('span','rt-tag included',s.label),make('h3','',s.title),make('p','',s.text));a.append(c);cards.append(a)});stays.append(cards);main.append(stays)}
  if(d.activities.length){const acts=make('section','rt-section');acts.append(sectionHead('Опціонально','Мода, дизайн і виставки'));const cards=make('div','rt-card-row');d.activities.slice(0,4).forEach((s,i)=>{const a=make('a','rt-card');a.href=s.link;a.target='_blank';a.rel='noopener noreferrer';a.append(imageEl(i+4));const c=make('div','rt-card-body');c.append(make('span','rt-tag optional',s.label),make('h3','',s.title),make('p','',s.text));a.append(c);cards.append(a)});acts.append(cards);main.append(acts)}

  const dates=make('section','rt-section');dates.id='rt-dates';dates.append(sectionHead('Варіанти','Обрати дати'));const booking=make('div','rt-booking');const rows=make('div','rt-date-list');const originals=originalTabs();originals.forEach((b,i)=>{const row=make('button',`rt-date-row${b.getAttribute('aria-selected')==='true'?' best':''}`);row.type='button';const strong=b.querySelector('strong')?.textContent?.trim()||b.textContent.trim();const small=b.querySelector('span')?.textContent?.trim()||'';const copy=make('span');copy.append(make('strong','',strong),make('small','',small));row.append(copy,make('span','rt-date-price',i===selectedTabIndex()?d.price:'обрати'));row.addEventListener('click',()=>{b.click();setTimeout(render,80)});rows.append(row)});const summary=make('aside','rt-summary');summary.append(make('p','rt-eyebrow','Обраний варіант'),make('h3','',d.dateTitle||'Мілан'),make('div','rt-summary-price',d.price),make('p','',d.perPerson||d.dateMeta));const plan=make('a','rt-btn amber','Дивитися план');plan.href='#rt-days';summary.append(plan);booking.append(rows,summary);dates.append(booking);main.append(dates);

  const details=make('section','rt-section');details.append(sectionHead('Практично','Вартість, умови та джерела'));const accordion=make('div','rt-accordion');
  const addDetails=(title,items,open=false)=>{if(!items.length)return;const el=make('details','rt-acc');el.open=open;el.append(make('summary','',title));const box=make('div','rt-acc-body');items.forEach(item=>{if(typeof item==='string')box.append(make('p','',item));else{const row=make('div','rt-info-row');row.append(make('strong','',item.label||item.title),make('span','',item.value||item.text||item.note||''));if(item.href&&item.href!=='#'){const a=make('a','', 'Джерело ↗');a.href=item.href;a.target='_blank';a.rel='noopener noreferrer';row.append(a)}box.append(row)}});el.append(box);accordion.append(el)};
  addDetails('Бюджет',d.budget,true);addDetails('Що включено',d.included);addDetails('Що не включено',d.excluded);addDetails('Документи й ризики',d.practical);addDetails('Офіційні джерела',d.sources);addDetails('Фото й ліцензії',[`Фото: Wikimedia Commons; використано ${photos.length} зображень із відкритими ліцензіями.`]);details.append(accordion);main.append(details);
  app.append(main);

  const footer=make('footer','rt-footer');const fw=make('div','rt-wrap');fw.append(make('strong','', 'Travel · приватний кандидат'),make('span','', 'Без бронювання, оплати або зобов’язання їхати.'));footer.append(fw);app.append(footer);
  const sticky=make('div','rt-sticky');const sc=make('div');sc.append(make('small','',d.dateTitle),make('strong','',d.price));const sa=make('a','rt-btn amber','Дивитися план');sa.href='#rt-days';sticky.append(sc,sa);app.append(sticky);
}
function boot(){if(!txt('#tripTitle',source)&&!txt('#pageTitle',source)){setTimeout(boot,100);return}render();root.dataset.travelTemplate='claude-roadtrip-mexico-v2'}
boot();
})();