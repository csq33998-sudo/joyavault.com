const assert = require('node:assert/strict');
const { matches } = require('../js/finds-filter.js');
const records = [
  { search: 'Leather BOOTS winter', category: 'Shoes', marketplace: 'Taobao', brand: 'Example' },
  { search: 'Cotton hoodie winter', category: 'Clothing', marketplace: 'Weidian' },
  { search: 'Leather loafers', category: 'Shoes', marketplace: '1688' },
];
const filter = (query = '', category = '', marketplace = '') => records.filter((row) => matches(row, { query, category, marketplace }));
assert.equal(filter().length, 3);
assert.equal(filter('  BOOTS  ').length, 1);
assert.equal(filter('winter leather', 'Shoes', 'Taobao').length, 1);
assert.equal(filter('winter', 'Shoes', 'Weidian').length, 0);
assert.equal(filter('', 'Shoes').length, 2);
assert.equal(filter('', '', '1688').length, 1);
assert.equal(filter('<script>alert(1)</script>').length, 0);
assert.equal(matches(records[0], {query: 'boots', category: 'Shoes', marketplace: 'Taobao', brand: 'Example'}), true);
assert.equal(matches(records[0], {brand: 'Different brand'}), false);
assert.equal(matches({search:'Café', category:'', marketplace:''}, {query:'cafe'}), true);
console.log('PASS: case, whitespace, multi-term search, combined filters, reset, no-match, and accent normalization.');

const priced = {search:'Cotton hoodie', category:'Clothing', subcategory:'Hoodies', brand:'Example', styles:'casual|cotton', priceCny:'100'};
assert(matches(priced, {subcategory:'Hoodies', brand:'casual', minPrice:'100', maxPrice:'100'}));
assert(!matches(priced, {subcategory:'Boots'}));
assert(!matches(priced, {minPrice:'101'}));
assert(!matches(priced, {maxPrice:'99'}));
assert(!matches(priced, {minPrice:'200', maxPrice:'100'}));
assert(!matches(priced, {minPrice:'-1'}));
assert(!matches(priced, {maxPrice:'invalid'}));
assert(matches({...priced,priceCny:'0'}, {minPrice:'0',maxPrice:'0'}));
console.log('PASS: subcategory, style, inclusive price boundaries, zero price, invalid and reversed ranges.');
