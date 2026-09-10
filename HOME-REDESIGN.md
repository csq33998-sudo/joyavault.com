# 首页重做说明

本文记录上一轮首页重做。当前商品系统已升级为 60 条记录、首页默认 8 条及总览组合筛选，维护请以 [Finds 数据系统](FINDS-DATA-SYSTEM.md) 为准。

首页按 Hero、Search、Featured finds、Category、Marketplace、Guide、Comparison、FAQ、Final CTA 的顺序实现。

- 首页默认以静态 HTML 展示 12 个商品卡；全部 20 条记录可本地搜索，分页每页最多 12 条。
- 商品数据：src/data/finds.json，沿用原有商品标题、图片、价格参考和 MaisonLooks 来源链接。
- 原始数据没有 marketplace 和商品更新日期，保留 null 并显示 Not verified / Not recorded。没有编造日期或将商品归入未经确认的平台。
- 搜索包含标题、品牌、分类、已记录的 marketplace 和关键词；未记录的平台不会被虚假匹配。
- 商品详情使用 /en/finds/<slug>/ 的真实页面，20 个详情页暂设 noindex, follow，避免将未核实的薄内容加入 sitemap。
- 搜索空状态初始隐藏，仅无匹配结果时出现；清空恢复默认 12 条。
- 搜索无需向第三方发送搜索词；卡片 HTML 在构建时由 JSON 生成，不依赖页面加载后的数据请求。
- 首页及详情页所有 CTA 都是 a href；FAQ 使用原生 details/summary。为保持这些页面仅有链接 CTA，未挂载语言和主题控制，其他页面的工具保留。
- 首页 title、description、OG/Twitter 标题和描述已按要求统一，canonical 保持 https://joyavault.com/en/。
- 一页一个 H1，每个图片都有 alt。外部图片失败时显示本地占位图及文字。
- 未提供真实性、官方背书或实时价格承诺。

## 主要文件

- en/index.html：首页静态输出。
- components/home.html：九个区块的源模板。
- home.css：首页和详情页响应式样式。
- src/data/finds.json：20 条本地数据。
- js/finds-search.js：搜索、分页、清空及图片失败处理。
- scripts/build-home.py：生成首页与详情页。
- en/finds/**/index.html：20 个可直接访问的详情页。
- scripts/site_routes.py、scripts/sync-layout.py、vercel.json：详情页路由及共享布局接入。
- assets/icons/find-image-unavailable.svg：图片加载失败占位图。

## 维护

修改数据或首页模板后运行：

```text
python scripts/build-home.py
python scripts/sync-routing.py
python scripts/build-home.py --check
python scripts/sync-layout.py --check
python scripts/verify-urls.py
```

已核对：九个区块、SEO 文案、单一 H1、图片 alt、默认静态卡片数、无默认空状态、真实链接。浏览器验证 hoodies 返回 2 条、无匹配查询显示空状态、键盘清空恢复 12 条、第二页显示 8 条，以及手机端布局和详情链接。

全站回归检查通过：62 个页面、1,623 条内部链接、371 条直接 301；本地 HTTP 检查对应 301 和 200，保留查询参数，无重定向循环。sitemap 仍为 38 个可索引 URL，未核实详情页不加入。

未部署到线上。可运行 preview.cmd 或 preview.ps1 查看本地站点。


## /en/ homepage refresh

The homepage contains the requested hero and exact description, search, eight featured finds, five category links, three marketplace links, buying/QC/shipping/fee guides, task comparison, five FAQs, final CTA, and the independent-site statement. The hero now includes a three-step research path; search has its own panel, with responsive marketplace cards and keyboard focus states.

The source template is components/home.html; scoped styles are in home.css. Rebuild with scripts/build-finds.py. Search uses the cards generated from src/data/finds.json, preserving noindex demo details and sponsored product-source links.

Verified in Chrome at 390, 768, and 1440 pixels: no horizontal page overflow, eight initial cards, matching and empty searches, Buying Guide fallback, URL restoration, and no JavaScript errors. Finds tests, SEO checks, internal-link validation, and build consistency checks passed. Screenshots are in audits/home-redesign-*.png. Changes remain local.
