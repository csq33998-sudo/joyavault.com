# JoyaVault 品牌与导航统一

后续 URL 迁移已完成，本文记录上一轮品牌修改；当前页面路径及重定向详见 [URL 迁移说明](URL-MIGRATION.md)。

## 修改结果

- 原有 36 个页面的正文保留；Header/Footer 改用统一静态模板。
- 主品牌为 JoyaVault，副标题为 Joyagoo Spreadsheet discovery hub。
- 旧 MaisonLooks 站点品牌和 SEO 分享标题替换，MaisonLooks 仅作为外部商品库。
- Header/Footer 按要求统一文案及顺序；Categories 指向 finds-spreadsheet.html#categories。
- 新增 JV SVG 标识，统一 Header 和 favicon。
- 品牌卡片使用真实锚点链接并保留筛选交互。
- Contact 与三项政策页面为待补充说明页，设置 noindex, follow；尚未提供联系邮箱和完整政策文本。

## 验证

- 40 个页面，1,056 条静态内部链接：无缺失页面、无效锚点或空链接。
- 原有页面 main 正文逐一与修改前比对一致，仅分类区增加锚点。
- 共享模板同步检查通过；JavaScript 语法检查通过。
- 桌面及 375px 手机宽度 Header、手机 Footer、Categories 跳转已在浏览器检查，所查页面无控制台错误。

## 后续维护

编辑 components/header.html 和 components/footer.html 后运行：

```text
python scripts/sync-layout.py
python scripts/sync-layout.py --check
```

生成结果直接写入 HTML，浏览器无需通过 JavaScript 加载导航。

## 文件清单

- [1688-finds-spreadsheet.html](C:/Users/chu/Documents/joyavault.com/en/marketplaces/1688/index.html)
- [accessories-finds-spreadsheet.html](C:/Users/chu/Documents/joyavault.com/en/best-joyagoo-finds/accessories/index.html)
- [articles.html](C:/Users/chu/Documents/joyavault.com/en/articles/index.html)
- [articles/best-sneaker-finds.html](C:/Users/chu/Documents/joyavault.com/en/articles/best-sneaker-finds/index.html)
- [articles/joyagoo-spreadsheet-coupon-fee-checklist.html](C:/Users/chu/Documents/joyavault.com/en/articles/joyagoo-spreadsheet-coupon-fee-checklist/index.html)
- [articles/joyagoo-spreadsheet-qc-checklist.html](C:/Users/chu/Documents/joyavault.com/en/articles/joyagoo-spreadsheet-qc-checklist/index.html)
- [articles/joyagoo-spreadsheet-shipping-planning.html](C:/Users/chu/Documents/joyavault.com/en/articles/joyagoo-spreadsheet-shipping-planning/index.html)
- [articles/joyagoo-spreadsheet-vs-traditional-spreadsheet.html](C:/Users/chu/Documents/joyavault.com/en/articles/joyagoo-spreadsheet-vs-traditional-spreadsheet/index.html)
- [articles/taobao-weidian-1688-finds-guide.html](C:/Users/chu/Documents/joyavault.com/en/articles/taobao-weidian-1688-finds-guide/index.html)
- [assets/icons/joyavault.svg](C:/Users/chu/Documents/joyavault.com/assets/icons/joyavault.svg)
- [bag-finds-spreadsheet.html](C:/Users/chu/Documents/joyavault.com/en/best-joyagoo-finds/accessories/bags/index.html)
- [blog/category-discovery-notes-for-joyagoo-haul-planning.html](C:/Users/chu/Documents/joyavault.com/en/blog/category-discovery-notes-for-joyagoo-haul-planning/index.html)
- [blog/choosing-an-agent-route-after-category-research.html](C:/Users/chu/Documents/joyavault.com/en/blog/choosing-an-agent-route-after-category-research/index.html)
- [blog/how-to-use-trending-lists-in-a-joyagoo-haul.html](C:/Users/chu/Documents/joyavault.com/en/blog/how-to-use-trending-lists-in-a-joyagoo-haul/index.html)
- [blog/index.html](C:/Users/chu/Documents/joyavault.com/en/blog/index.html)
- [blog/joyagoo-haul-guide-workflow-from-list-to-shipping.html](C:/Users/chu/Documents/joyavault.com/en/blog/joyagoo-haul-guide-workflow-from-list-to-shipping/index.html)
- [blog/qc-notes-before-warehouse-consolidation.html](C:/Users/chu/Documents/joyavault.com/en/blog/qc-notes-before-warehouse-consolidation/index.html)
- [blog/review-notes-that-keep-haul-finds-organized.html](C:/Users/chu/Documents/joyavault.com/en/blog/review-notes-that-keep-haul-finds-organized/index.html)
- [blog/routes.html](C:/Users/chu/Documents/joyavault.com/en/blog/routes/index.html)
- [blog/shipping-route-planning-for-a-joyagoo-haul.html](C:/Users/chu/Documents/joyavault.com/en/blog/shipping-route-planning-for-a-joyagoo-haul/index.html)
- [brands.html](C:/Users/chu/Documents/joyavault.com/en/brands/index.html)
- [components/footer.html](C:/Users/chu/Documents/joyavault.com/components/footer.html)
- [components/header.html](C:/Users/chu/Documents/joyavault.com/components/header.html)
- [contact.html](C:/Users/chu/Documents/joyavault.com/en/contact/index.html)
- [editorial-policy.html](C:/Users/chu/Documents/joyavault.com/en/editorial-policy/index.html)
- [finds-spreadsheet.html](C:/Users/chu/Documents/joyavault.com/en/best-joyagoo-finds/index.html)
- [guide.html](C:/Users/chu/Documents/joyavault.com/en/joyagoo-buying-guide/index.html)
- [guides.html](C:/Users/chu/Documents/joyavault.com/en/joyagoo-buying-guide/index.html)
- [hoodie-finds-spreadsheet.html](C:/Users/chu/Documents/joyavault.com/en/best-joyagoo-finds/clothing/hoodies/index.html)
- [index.html](C:/Users/chu/Documents/joyavault.com/en/index.html)
- [jersey-finds-spreadsheet.html](C:/Users/chu/Documents/joyavault.com/en/best-joyagoo-finds/clothing/jerseys/index.html)
- [jordan-finds-spreadsheet.html](C:/Users/chu/Documents/joyavault.com/en/brands/jordan/index.html)
- [joyagoo-spreadsheet-updates.html](C:/Users/chu/Documents/joyavault.com/en/joyagoo-spreadsheet-updates/index.html)
- [joyagoo-spreadsheet.html](C:/Users/chu/Documents/joyavault.com/en/joyagoo-spreadsheet/index.html)
- [js/i18n.js](C:/Users/chu/Documents/joyavault.com/js/i18n.js)
- [js/main.js](C:/Users/chu/Documents/joyavault.com/js/main.js)
- [nike-finds-spreadsheet.html](C:/Users/chu/Documents/joyavault.com/en/brands/nike/index.html)
- [polo-shirt-finds-spreadsheet.html](C:/Users/chu/Documents/joyavault.com/en/best-joyagoo-finds/clothing/polo-shirts/index.html)
- [preview.cmd](C:/Users/chu/Documents/joyavault.com/preview.cmd)
- [preview.ps1](C:/Users/chu/Documents/joyavault.com/preview.ps1)
- [privacy-policy.html](C:/Users/chu/Documents/joyavault.com/en/privacy-policy/index.html)
- [scripts/sync-layout.py](C:/Users/chu/Documents/joyavault.com/scripts/sync-layout.py)
- [shorts-finds-spreadsheet.html](C:/Users/chu/Documents/joyavault.com/en/best-joyagoo-finds/clothing/shorts/index.html)
- [sneaker-finds-spreadsheet.html](C:/Users/chu/Documents/joyavault.com/en/best-joyagoo-finds/shoes/index.html)
- [styles.css](C:/Users/chu/Documents/joyavault.com/styles.css)
- [t-shirt-finds-spreadsheet.html](C:/Users/chu/Documents/joyavault.com/en/best-joyagoo-finds/clothing/t-shirts/index.html)
- [taobao-finds-spreadsheet.html](C:/Users/chu/Documents/joyavault.com/en/marketplaces/taobao/index.html)
- [terms-of-service.html](C:/Users/chu/Documents/joyavault.com/en/terms-of-service/index.html)
- [weidian-finds-spreadsheet.html](C:/Users/chu/Documents/joyavault.com/en/marketplaces/weidian/index.html)
