const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const handlers = {};
let focused = false;
const link = {href:'https://joyavault.com/de/shoes/'};
const menu = {open:true, contains:target=>target.inside, querySelector:()=>({focus:()=>{focused=true;}})};
const document = {
  documentElement:{lang:'de'},
  addEventListener:(name,callback,capture)=>{(handlers[name] ||= []).push(callback); if (name==='click') assert.equal(capture,true);},
  querySelectorAll:selector=>selector==='.locale-options a'?[link]:menu.open?[menu]:[],
};
const window = {location:{href:'https://joyavault.com/en/shoes/?brand=Nike#finds',search:'?brand=Nike',hash:'#finds'},ML_TRANSLATIONS:{'Page {page} of {total}':'Seite {page} von {total}'}};
vm.runInNewContext(fs.readFileSync(require('node:path').join(__dirname,'../js/i18n.js'),'utf8'), {document,window,URL});
assert.equal(window.ML_I18N.t('Page {page} of {total}',{page:2,total:5}),'Seite 2 von 5');
handlers.DOMContentLoaded.forEach(fn=>fn());
assert.equal(link.href,'https://joyavault.com/de/shoes/?brand=Nike#finds');
const click=inside=>handlers.click.forEach(fn=>fn({target:{inside,closest:()=>inside}}));
click(true);assert(menu.open);
click(false);assert(!menu.open);
menu.open=true;handlers.keydown.forEach(fn=>fn({key:'Escape'}));assert(!menu.open);assert(focused);
console.log('PASS: translated dynamic UI, query/hash preservation, inside/outside clicks and Escape.');
