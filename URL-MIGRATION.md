# URL 迁移说明

已将旧静态页面迁入 en/ 下的目录式 index.html。正式 URL 以 /en/ 开头并以 / 结尾。

## 重定向配置

- Vercel 配置：vercel.json。291 条显式重定向全部使用 statusCode: 301。
- 覆盖原有 40 个页面的无扩展名、.html、尾斜杠版本，以及首页与 blog/index 的入口变体。
- 新页面的无尾斜杠、.html、index.html、index 别名也直接 301 到规范 URL。
- 关闭 cleanUrls，移除 trailingSlash 自动归一化配置，避免平台默认使用 308。
- 42 条精确 rewrite 将规范 URL 映射到对应的静态 index.html，不改变浏览器地址。
- 所有跳转直接抵达最终页面，没有重定向链或循环。

## 内容与 SEO

- 原有 40 个页面正文保留验证通过，审计记录：scripts/migration-audit.json。
- guide.html 与 guides.html 合并到购买指南；原 guides 内容位于 #guide-routes 区块。
- 服装细分类、Nike/Jordan 品牌页、其他文章及博客保留独立新路径。
- 新增服装分类汇总、美容香氛、电子产品页。后两类明确标注暂无精选商品。
- 全站 canonical 和 og:url 指向各自新 URL；内部链接和静态资源采用根相对路径。
- sitemap.xml 包含 38 个可索引的新 URL。上一轮的联系和三项政策说明页继续 noindex，未加入 sitemap。

## 本地验证

- 42 个页面、1,110 条内部链接、291 条 301 规则通过检查。
- 本地 HTTP 检查：全部 291 个别名返回 301；42 个最终页面返回 200。
- 查询参数保留；不存在的页面返回 404；无缺失锚点、重复 ID 或缺失本地资源。
- 浏览器验证旧 guides.html 跳转到新购买指南并显示合并内容。
- 本地预览读取 vercel.json 的重定向表；它不是 Vercel 边缘网络仿真器。尚未部署，因此不代表线上已生效。

## 维护及发布后验证

```text
python scripts/sync-layout.py
python scripts/sync-routing.py
python scripts/sync-layout.py --check
python scripts/sync-routing.py --check
python scripts/verify-urls.py
python scripts/preview-server.py --port 5191
python scripts/verify-urls.py --base-url http://127.0.0.1:5191
```

部署后使用实际预览域名或正式域名执行：

```text
python scripts/verify-urls.py --base-url https://joyavault.com
```

Vercel 会读取 vercel.json 执行服务器端 301。若实际使用 Nginx、Apache 或其他静态托管，需要在该服务的重定向配置中导入相同映射；直接打开 HTML 或使用普通静态文件服务器不会执行 vercel.json。preview.cmd 和 preview.ps1 已改用支持这些规则的本地预览服务。

配置依据：[Vercel redirects](https://vercel.com/docs/project-configuration/vercel-json#redirects) 与 [trailingSlash](https://vercel.com/docs/project-configuration/vercel-json#trailingslash)。

## 旧页面到新 URL 完整映射

| 旧文件 | 新 URL |
| --- | --- |
| index.html | [/en/](C:/Users/chu/Documents/joyavault.com/en/index.html) |
| joyagoo-spreadsheet.html | [/en/joyagoo-spreadsheet/](C:/Users/chu/Documents/joyavault.com/en/joyagoo-spreadsheet/index.html) |
| joyagoo-spreadsheet-updates.html | [/en/joyagoo-spreadsheet-updates/](C:/Users/chu/Documents/joyavault.com/en/joyagoo-spreadsheet-updates/index.html) |
| guide.html | [/en/joyagoo-buying-guide/](C:/Users/chu/Documents/joyavault.com/en/joyagoo-buying-guide/index.html) |
| guides.html | [/en/joyagoo-buying-guide/](C:/Users/chu/Documents/joyavault.com/en/joyagoo-buying-guide/index.html) |
| finds-spreadsheet.html | [/en/best-joyagoo-finds/](C:/Users/chu/Documents/joyavault.com/en/best-joyagoo-finds/index.html) |
| sneaker-finds-spreadsheet.html | [/en/best-joyagoo-finds/shoes/](C:/Users/chu/Documents/joyavault.com/en/best-joyagoo-finds/shoes/index.html) |
| accessories-finds-spreadsheet.html | [/en/best-joyagoo-finds/accessories/](C:/Users/chu/Documents/joyavault.com/en/best-joyagoo-finds/accessories/index.html) |
| bag-finds-spreadsheet.html | [/en/best-joyagoo-finds/accessories/bags/](C:/Users/chu/Documents/joyavault.com/en/best-joyagoo-finds/accessories/bags/index.html) |
| hoodie-finds-spreadsheet.html | [/en/best-joyagoo-finds/clothing/hoodies/](C:/Users/chu/Documents/joyavault.com/en/best-joyagoo-finds/clothing/hoodies/index.html) |
| shorts-finds-spreadsheet.html | [/en/best-joyagoo-finds/clothing/shorts/](C:/Users/chu/Documents/joyavault.com/en/best-joyagoo-finds/clothing/shorts/index.html) |
| t-shirt-finds-spreadsheet.html | [/en/best-joyagoo-finds/clothing/t-shirts/](C:/Users/chu/Documents/joyavault.com/en/best-joyagoo-finds/clothing/t-shirts/index.html) |
| polo-shirt-finds-spreadsheet.html | [/en/best-joyagoo-finds/clothing/polo-shirts/](C:/Users/chu/Documents/joyavault.com/en/best-joyagoo-finds/clothing/polo-shirts/index.html) |
| jersey-finds-spreadsheet.html | [/en/best-joyagoo-finds/clothing/jerseys/](C:/Users/chu/Documents/joyavault.com/en/best-joyagoo-finds/clothing/jerseys/index.html) |
| brands.html | [/en/brands/](C:/Users/chu/Documents/joyavault.com/en/brands/index.html) |
| nike-finds-spreadsheet.html | [/en/brands/nike/](C:/Users/chu/Documents/joyavault.com/en/brands/nike/index.html) |
| jordan-finds-spreadsheet.html | [/en/brands/jordan/](C:/Users/chu/Documents/joyavault.com/en/brands/jordan/index.html) |
| taobao-finds-spreadsheet.html | [/en/marketplaces/taobao/](C:/Users/chu/Documents/joyavault.com/en/marketplaces/taobao/index.html) |
| weidian-finds-spreadsheet.html | [/en/marketplaces/weidian/](C:/Users/chu/Documents/joyavault.com/en/marketplaces/weidian/index.html) |
| 1688-finds-spreadsheet.html | [/en/marketplaces/1688/](C:/Users/chu/Documents/joyavault.com/en/marketplaces/1688/index.html) |
| articles.html | [/en/articles/](C:/Users/chu/Documents/joyavault.com/en/articles/index.html) |
| contact.html | [/en/contact/](C:/Users/chu/Documents/joyavault.com/en/contact/index.html) |
| privacy-policy.html | [/en/privacy-policy/](C:/Users/chu/Documents/joyavault.com/en/privacy-policy/index.html) |
| terms-of-service.html | [/en/terms-of-service/](C:/Users/chu/Documents/joyavault.com/en/terms-of-service/index.html) |
| editorial-policy.html | [/en/editorial-policy/](C:/Users/chu/Documents/joyavault.com/en/editorial-policy/index.html) |
| blog/index.html | [/en/blog/](C:/Users/chu/Documents/joyavault.com/en/blog/index.html) |
| articles/best-sneaker-finds.html | [/en/articles/best-sneaker-finds/](C:/Users/chu/Documents/joyavault.com/en/articles/best-sneaker-finds/index.html) |
| articles/joyagoo-spreadsheet-coupon-fee-checklist.html | [/en/articles/joyagoo-spreadsheet-coupon-fee-checklist/](C:/Users/chu/Documents/joyavault.com/en/articles/joyagoo-spreadsheet-coupon-fee-checklist/index.html) |
| articles/joyagoo-spreadsheet-qc-checklist.html | [/en/articles/joyagoo-spreadsheet-qc-checklist/](C:/Users/chu/Documents/joyavault.com/en/articles/joyagoo-spreadsheet-qc-checklist/index.html) |
| articles/joyagoo-spreadsheet-shipping-planning.html | [/en/articles/joyagoo-spreadsheet-shipping-planning/](C:/Users/chu/Documents/joyavault.com/en/articles/joyagoo-spreadsheet-shipping-planning/index.html) |
| articles/joyagoo-spreadsheet-vs-traditional-spreadsheet.html | [/en/articles/joyagoo-spreadsheet-vs-traditional-spreadsheet/](C:/Users/chu/Documents/joyavault.com/en/articles/joyagoo-spreadsheet-vs-traditional-spreadsheet/index.html) |
| articles/taobao-weidian-1688-finds-guide.html | [/en/articles/taobao-weidian-1688-finds-guide/](C:/Users/chu/Documents/joyavault.com/en/articles/taobao-weidian-1688-finds-guide/index.html) |
| blog/routes.html | [/en/blog/routes/](C:/Users/chu/Documents/joyavault.com/en/blog/routes/index.html) |
| blog/category-discovery-notes-for-joyagoo-haul-planning.html | [/en/blog/category-discovery-notes-for-joyagoo-haul-planning/](C:/Users/chu/Documents/joyavault.com/en/blog/category-discovery-notes-for-joyagoo-haul-planning/index.html) |
| blog/choosing-an-agent-route-after-category-research.html | [/en/blog/choosing-an-agent-route-after-category-research/](C:/Users/chu/Documents/joyavault.com/en/blog/choosing-an-agent-route-after-category-research/index.html) |
| blog/how-to-use-trending-lists-in-a-joyagoo-haul.html | [/en/blog/how-to-use-trending-lists-in-a-joyagoo-haul/](C:/Users/chu/Documents/joyavault.com/en/blog/how-to-use-trending-lists-in-a-joyagoo-haul/index.html) |
| blog/joyagoo-haul-guide-workflow-from-list-to-shipping.html | [/en/blog/joyagoo-haul-guide-workflow-from-list-to-shipping/](C:/Users/chu/Documents/joyavault.com/en/blog/joyagoo-haul-guide-workflow-from-list-to-shipping/index.html) |
| blog/qc-notes-before-warehouse-consolidation.html | [/en/blog/qc-notes-before-warehouse-consolidation/](C:/Users/chu/Documents/joyavault.com/en/blog/qc-notes-before-warehouse-consolidation/index.html) |
| blog/review-notes-that-keep-haul-finds-organized.html | [/en/blog/review-notes-that-keep-haul-finds-organized/](C:/Users/chu/Documents/joyavault.com/en/blog/review-notes-that-keep-haul-finds-organized/index.html) |
| blog/shipping-route-planning-for-a-joyagoo-haul.html | [/en/blog/shipping-route-planning-for-a-joyagoo-haul/](C:/Users/chu/Documents/joyavault.com/en/blog/shipping-route-planning-for-a-joyagoo-haul/index.html) |

## 主要变更文件

- en/**/index.html：42 个迁移后的页面。
- vercel.json、sitemap.xml：重定向、页面映射与规范 sitemap。
- components/header.html、components/footer.html：新 URL 导航。
- scripts/site_routes.py、scripts/sync-routing.py：统一 URL 映射及配置生成。
- scripts/sync-layout.py：适配 en 目录。
- scripts/preview-server.py、scripts/verify-urls.py：本地 301 预览与 HTTP 校验。
- scripts/migrate-urls.py、scripts/migration-audit.json：一次性迁移及正文保留审计。
- preview.cmd、preview.ps1、.vercelignore、.gitignore：预览入口、发布文件排除和缓存排除。
