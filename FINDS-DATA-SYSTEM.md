# Finds 数据系统

## 编辑入口

三个 marketplace 页面现由 `scripts/marketplace_page.py` 生成，也纳入 `scripts/build-finds.py`。每页仅显示 `marketplace` 精确匹配的记录，并要求至少八条；分类入口同时携带 category 和 marketplace 条件。页面继续明确区分示例和未核实的保存记录，不为示例生成卖家链接。专用检查：`python scripts/test-marketplaces.py`。

`src/data/finds.json` 是当前首页、Finds 总览和详情页唯一使用的商品数据源。此次保留原有 20 条未独立核实记录，新增 40 条明确标注的示例，共 60 条。示例的 marketplace 和价格仅用于浏览与筛选演示，没有商家来源，不是可购买的真实报价。

修改数据后运行：

```text
python scripts/build-finds.py
```

该命令先验证数据，再生成首页、Finds 总览、所有详情页，并更新 Vercel 路由及 sitemap。无需 Node 包或前端框架。不要手动编辑生成的 HTML 卡片。

检查是否忘记重新生成：

```text
python scripts/build-finds.py --check
python scripts/test-finds.py
node scripts/test-finds-filter.cjs
python scripts/verify-urls.py
```

## 字段约定

| 字段 | 类型 / 约定 |
| --- | --- |
| id | 唯一且稳定的小写字母、数字、连字符 ID |
| title | 展示标题；示例应明确标注 example |
| category | Shoes、Clothing、Accessories、Beauty & Fragrance、Electronics |
| subcategory | category 对应的细分类；见下表 |
| brand | 展示品牌；不要为无品牌示例伪造品牌 |
| marketplace | Taobao、Weidian、1688；未核实的原记录用 Unknown |
| priceCny | 非负数字，不带货币符号；示例价与保存价分别标注，不作为实时报价 |
| image | 本地 /assets/ 路径或 HTTPS 图片 URL |
| sourceUrl | 已有真实来源用 HTTPS；没有来源必须用 # |
| detailUrl | 唯一、稳定的 /en/finds/slug/；避免随标题变化而修改 |
| tags | 非空字符串数组，用于搜索 |
| qcNotes | 非空字符串数组，在详情页显示 |
| shippingNotes | 非空字符串数组，在详情页显示 |
| isIndexable | 必填布尔值；demo 必须为 false，当前所有未核实记录均为 false |
| updatedAt | YYYY-MM-DD；表示本站记录维护日期，不是卖家更新时间或核实日期 |

辅助字段同样由校验器检查：

- `sourceType`：`commercial`、`affiliate`、`editorial`、`unavailable`。
- `isPlaceholder`：布尔值；示例设为 `true`，来源必须为 `#`。
- `featured`：布尔值；首页优先展示前 8 条精选记录，至少保留 8 条精选。
- `imageAlt`：图片替代文字；示例图片说明是占位图。
- `description`：详情说明；示例明确说明价格和平台仅为示意。
- `sourceName`：来源名称，无来源填 Source pending。

`src/data/finds.schema.json` 可用于编辑器提示。`scripts/finds_data.py` 是构建时校验器，会阻止缺字段、重复 ID/URL、错误分类、非法日期、负数价格和不安全链接进入生成步骤。

## 分类

| category | subcategory |
| --- | --- |
| Shoes | Sneakers、Boots、Loafers、Clogs |
| Clothing | Tops、Hoodies、Outerwear、Bottoms |
| Accessories | Bags、Eyewear、Jewelry、Watches |
| Beauty & Fragrance | Perfume |
| Electronics | Audio、Phone Accessories |

## 卡片与外链

- `components/FindCard.html` 是共享组件模板；`scripts/find_card.py` 负责转义、价格与日期格式化、外链策略。
- 商业或联盟来源渲染为 `rel="sponsored nofollow noopener noreferrer"`。
- `#` 只留在数据中；Open product source 使用真实 `<a href="详情地址#product-source">`，跳到来源待补充说明，并明确显示 Source pending，不伪造商家链接。
- 示例商品和 marketplace badge 有明确 example 标记。
- 详情页展示 QC 与 shipping notes；所有 60 个未核实详情页继续 `noindex, follow`，不加入 sitemap。

## 页面行为

- `/en/` 默认显示 8 条，搜索覆盖全部 60 条，每页 8 条。
- `/en/best-joyagoo-finds/` 默认覆盖全部 60 条，每页 24 条；搜索、category、marketplace 和 brand 使用 AND 组合，切换筛选回到第一页。
- 搜索匹配标题、品牌、分类、细分类、marketplace 和 tags，忽略大小写及首尾空格。
- 筛选和分页状态保存在 URL 的 `q`、`category`、`marketplace`、`brand`、`page` 中，刷新可恢复；上一页和下一页使用真实链接。
- 无结果时推荐 Shoes、Clothing、Accessories 的真实分类入口、Buying Guide 和重置链接。
- HTML 已包含卡片和真实详情链接，禁用 JavaScript 仍能看到首页 8 条和总览全部 60 条；交互筛选需要 JavaScript。
- 总览介绍、分类、marketplace、购买指南与五个 FAQ 在 `components/finds-catalog.html` 维护。页面自引用 canonical，构建器生成 BreadcrumbList 和指定 SEO 标题、描述。

## 更换示例为真实记录

保留 id/detailUrl，填写真实标题、图片、来源、价格及已核实平台，设置 `isPlaceholder: false`，按来源性质选择 `sourceType`，更新说明、标签、QC/shipping notes 和本站记录维护日期，再运行构建命令。不要把示例平台或价格直接当作已核实信息。

若确需删除记录或改变 detailUrl，需另外保留旧详情 URL 的 301；构建器不会擅自删除已有详情文件或猜测重定向目标。

## 已验证

检查入口：`scripts/test-finds.py` 验证数据、链接与静态 SEO，`scripts/test-finds-filter.cjs` 验证组合筛选，`scripts/verify-urls.py` 检查路由、资源与 canonical。

改动保留在本地，尚未部署。

## 分类指南维护

五个大分类页共用 `components/CategoryPage.html`，分类独立文案在 `scripts/category_content.py`，由 `scripts/category_page.py` 渲染。运行 `scripts/build-finds.py` 会同步生成分类页、首页、总览、详情和路由配置。

分类网格从 finds.json 精确匹配 category，构建要求每类至少 8 条。细分类 signals 是研究提示，不代表已有库存。每张商品图的 alt 自动包含分类、商品描述和示例状态。

本次补充 3 条 Beauty & Fragrance 示例，数据总数为 63 条；来源保持 #。分类数量：Shoes 17、Clothing 20、Accessories 10、Beauty & Fragrance 8、Electronics 8。首页仍默认 8 条，总览仍每页 24 条。

运行 `scripts/test-categories.py` 检查分类数据归属、至少 8 条、图片描述、单 H1、独立描述、标题长度、FAQ 和面包屑。

## 本次完善：收录控制与卡片提示

保留现有 63 条记录（43 条 demo、20 条未独立核实的保存记录），已超过 30 条需求；每条均包含 isIndexable，目前全部为 false。校验器及 JSON Schema 拒绝把 demo 或无来源记录设为可收录。真实记录经审核后才可手动启用 isIndexable。

详情页按 isIndexable 输出 robots；demo 保留供访客查看的 noindex, follow 详情页，以支持 View details，不生成可收录详情页。sitemap 同时检查数据字段和页面 robots，排除所有 demo 和 isIndexable=false 记录。

FindCard 显示第一条 QC 和 shipping note（最多 140 字符），完整说明在详情页。两个操作均为 a href 链接，无需 onclick。商业和联盟链接包含 sponsored、nofollow、noopener、noreferrer。


## 核心商品发现目录（当前行为）

/en/best-joyagoo-finds/ 由 catalog_records 选择数据：有 isIndexable=true 的非 demo 商品时只展示这些商品；否则只展示 isPlaceholder=true 的 demo。目前展示 43 条 demo，整个目录页输出 noindex, follow，sitemap 不包含该目录 URL 的 loc。未核实的非 demo 保存记录不混入目录。

目录支持搜索（含 QC/shipping notes）、category、subcategory、marketplace、brand/style（品牌或 tags）、CNY 最低/最高价格的 AND 组合。价格包含边界；负值或最低价高于最高价时显示提示与分类/Buying Guide 入口。每页 24 条，筛选条件保存在 URL，翻页保留条件，改变条件回到第一页。禁用 JavaScript 时仍可浏览全部静态卡片及详情链接。

SEO 使用指定标题和描述，面包屑由共享 SEO 构建器生成；FAQPage 仅从页面中可供用户阅读的 FAQ 生成。类别、marketplace 和四个购买指南保留真实链接。

验证：scripts/test-finds.py、scripts/test-finds-filter.cjs、scripts/test-seo.py、scripts/verify-urls.py；Chrome 390/1440px 验证 24/19 分页、组合筛选、价格边界、重置、URL 恢复和无页面溢出。截图：audits/finds-directory-390.png、audits/finds-directory-1440.png。


## 五类 CategoryPage（当前规则）

五个分类共享 components/CategoryPage.html，各自文案位于 scripts/category_content.py，包括指定细分类、独立介绍、QC checklist、shipping notes 和至少四个 FAQ。内部下一步包含 Spreadsheet Guide、Best Joyagoo Finds、Buying Guide、QC Photo Checklist、Shipping Planning。

category_records 只按当前分类统计 isIndexable=true 且非 demo 的商品。达到 8 条时展示这些商品并允许页面收录；不足 8 条时展示分类内研究记录，明确区分未核实记录和 demo，整个页面 noindex, follow。当前五类分别有 17、20、10、8、8 张卡片，但没有达到真实商品门槛，因此均不进入 sitemap。

测试覆盖 7/8 条收录边界、分类归属、独立内容、链接和 SEO。Chrome 在 390px 和 1440px 验证全部五页无横向溢出、卡片数量、FAQ 展开、图片 alt 和 noindex。修改仅保存在本地。
