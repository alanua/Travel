(()=>{'use strict';
const root=document.documentElement;
root.classList.add('travel-canonical-v3');
const body=document.body;
if(body)body.classList.add('travel-canonical-body');

const commons='https://commons.wikimedia.org/wiki/Special:Redirect/file/';
const file=(name,width=1200)=>`${commons}${encodeURIComponent(name)}?width=${width}`;
const photos=[
  {file:'Milan-duomo-front-facade.jpg',alt:'Фасад Міланського собору на площі Дуомо',title:'Duomo',author:'Skarkkai',license:'CC0',source:'https://commons.wikimedia.org/wiki/File:Milan-duomo-front-facade.jpg'},
  {file:'Galleria Vittorio Emanuele II, Milan, Italy.jpg',alt:'Інтер’єр галереї Вітторіо Емануеле II',title:'Galleria Vittorio Emanuele II',author:'Wikimedia Commons contributor',license:'Commons licence',source:'https://commons.wikimedia.org/wiki/File:Galleria_Vittorio_Emanuele_II,_Milan,_Italy.jpg'},
  {file:'Quartiere Brera.jpg',alt:'Вулиця в районі Брера у Мілані',title:'Brera',author:'Wikimedia Commons contributor',license:'Commons licence',source:'https://commons.wikimedia.org/wiki/File:Quartiere_Brera.jpg'},
  {file:'Naviglio Grande canal Milan 2026.JPG',alt:'Канал Навільйо-Гранде з історичними будинками',title:'Navigli',author:'Mike is Michi',license:'CC BY-SA 4.0',source:'https://commons.wikimedia.org/wiki/File:Naviglio_Grande_canal_Milan_2026.JPG'},
  {file:'Bosco verticale, Milan, Italy (Unsplash).jpg',alt:'Bosco Verticale у сучасному Мілані',title:'Porta Nuova',author:'Chris Barbalis',license:'CC0',source:'https://commons.wikimedia.org/wiki/File:Bosco_verticale,_Milan,_Italy_(Unsplash).jpg'},
  {file:'Milan tram (232519688).jpg',alt:'Історичний жовтий трамвай у Мілані',title:'Міський транспорт',author:'LHOON',license:'CC BY-SA',source:'https://commons.wikimedia.org/wiki/File:Milan_tram_(232519688).jpg'}
];

function image(photo,eager=false,width=1200){
  const el=document.createElement('img');
  el.src=file(photo.file,width);
  el.alt=photo.alt;
  el.loading=eager?'eager':'lazy';
  el.decoding='async';
  el.referrerPolicy='no-referrer';
  el.addEventListener('error',()=>{
    el.removeAttribute('src');
    el.alt=`Фото тимчасово недоступне: ${photo.alt}`;
    el.parentElement?.classList.add('photo-unavailable');
  },{once:true});
  return el;
}
function ensureViewport(){
  let viewport=document.querySelector('meta[name="viewport"]');
  if(!viewport){
    viewport=document.createElement('meta');
    viewport.name='viewport';
    document.head.prepend(viewport);
  }
  viewport.content='width=device-width,initial-scale=1,viewport-fit=cover';
}
function normaliseShell(){
  document.querySelectorAll('.layout').forEach(el=>el.classList.add('page-grid'));
  document.querySelectorAll('.card').forEach(el=>el.classList.add('section-block'));
  const first=document.querySelector('.content-column > .date-switcher');
  if(first)first.classList.add('section-block');
}
function hero(){
  const gallery=document.getElementById('heroGallery');
  if(!gallery)return;
  gallery.dataset.milanCanonical='true';
  gallery.replaceChildren(...photos.slice(0,5).map((photo,index)=>{
    const wrap=document.createElement('div');
    wrap.className='hero-photo';
    wrap.append(image(photo,index===0,index===0?1600:900));
    return wrap;
  }));
}
function photoGallery(){
  let section=document.getElementById('milanPhotoGallery');
  if(section)section.remove();
  const anchor=document.querySelector('.intro-block')||document.querySelector('.route-section');
  if(!anchor)return;
  section=document.createElement('section');
  section.id='milanPhotoGallery';
  section.className='milan-gallery-block section-block';
  section.setAttribute('aria-labelledby','milanGalleryTitle');
  const heading=document.createElement('div');
  heading.className='section-heading';
  const copy=document.createElement('div');
  const kicker=document.createElement('p');
  kicker.className='section-kicker';
  kicker.textContent='Мілан у кадрі';
  const title=document.createElement('h2');
  title.id='milanGalleryTitle';
  title.textContent='Місця маршруту';
  copy.append(kicker,title);
  heading.append(copy);
  const grid=document.createElement('div');
  grid.className='milan-gallery-grid';
  photos.forEach(photo=>{
    const figure=document.createElement('figure');
    figure.className='milan-gallery-card';
    const link=document.createElement('a');
    link.href=photo.source;
    link.target='_blank';
    link.rel='noopener noreferrer';
    link.append(image(photo,false,900));
    const caption=document.createElement('figcaption');
    caption.textContent=photo.title;
    link.append(caption);
    figure.append(link);
    grid.append(figure);
  });
  section.append(heading,grid);
  anchor.after(section);
}
function dayPhotos(){
  document.querySelectorAll('.day').forEach((day,index)=>{
    const summary=day.querySelector('summary');
    if(!summary)return;
    let media=summary.querySelector('.day-image');
    if(!media){
      media=document.createElement('span');
      media.className='day-image';
      summary.prepend(media);
    }
    media.replaceChildren(image(photos[(index+1)%photos.length],false,640));
  });
}
function cardPhotos(){
  document.querySelectorAll('.stay-media,.activity-media').forEach((box,index)=>{
    box.replaceChildren(image(photos[(index+3)%photos.length],false,800));
  });
  document.querySelectorAll('.highlight').forEach((box,index)=>{
    box.querySelector(':scope > img')?.remove();
    box.prepend(image(photos[(index+2)%photos.length],false,800));
    box.classList.add('has-image');
  });
}
function attribution(){
  document.getElementById('photoAttribution')?.remove();
  const sources=document.getElementById('sources')?.closest('section');
  if(!sources)return;
  const details=document.createElement('details');
  details.id='photoAttribution';
  details.className='photo-attribution';
  const summary=document.createElement('summary');
  summary.textContent='Фото та ліцензії';
  const list=document.createElement('ul');
  photos.forEach(photo=>{
    const item=document.createElement('li');
    const link=document.createElement('a');
    link.href=photo.source;
    link.target='_blank';
    link.rel='noopener noreferrer';
    link.textContent=photo.title;
    item.append(link,document.createTextNode(` — ${photo.author}, ${photo.license}`));
    list.append(item);
  });
  details.append(summary,list);
  sources.append(details);
}
function mobileAction(){
  const bar=document.querySelector('.mobile-actionbar');
  if(!bar)return;
  const action=bar.querySelector('a');
  if(action){
    action.textContent='Дивитися маршрут';
    action.href='#itineraryTitle';
  }
}
function run(){
  ensureViewport();
  normaliseShell();
  hero();
  photoGallery();
  dayPhotos();
  cardPhotos();
  attribution();
  mobileAction();
  root.dataset.travelTemplate='claude-mobile-first-v1';
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run,{once:true});
else run();
let attempts=0;
const timer=setInterval(()=>{
  run();
  if(++attempts>=8)clearInterval(timer);
},300);
})();
