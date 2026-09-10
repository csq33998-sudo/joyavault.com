# 全站 SEO 配置

所有 170 个语言目录页面通过 `scripts/localization.py` 调用 `scripts/seo.py`，统一生成 head。首页、选品、分类、多语言、文章及布局更新都使用此入口，避免各脚本相互覆盖。没有发布到线上。

## 内容与元数据

- 本地化文案继续维护在 `src/locales/*.json`，文章继续维护在 `src/content/articles/*.md`。
- `src/seo/pages.json` 为旧页面提供人工改写的标题与描述，也支持单页 `image` 配置。新页面应在其内容源中填写自己的标题与描述。
- 商品详情使用对应记录的名称和研究说明。重名记录用保存记录编号区分；示例记录仍明确说明没有已验证的卖家报价，并保留 noindex。
- OG、Twitter 标题和描述与页面元数据保持一致。商品照片可用时使用该记录已有图片，其余默认使用网站现有分享图；共享默认图不代表每页拥有不同图片。
- canonical 使用自身语言的无参数 URL，保留现有 hreflang 和 RTL 配置。
- 构建检查只有一个 H1，且每张图片都有 alt 属性。装饰性图片保留空 alt，避免重复朗读旁边的品牌名称；内容图片保留原有描述。

## 结构化数据

- WebSite 和 Organization 使用稳定的站点级 @id，不虚构组织地址、评价、资质或官方关系。
- SearchAction 指向已有搜索入口 `/en/best-joyagoo-finds/?q={search_term_string}`，其查询参数由现有搜索脚本读取。依据 [Schema.org SearchAction](https://schema.org/SearchAction) 配置。
- 所有页面包含 BreadcrumbList；正文文章包含 Article，不为文章目录添加 Article。
- FAQPage 从 main 正文的问答折叠项读取，排除 header 语言菜单及隐藏内容。可展开的答案参与标记。以后若采用其他 FAQ 布局，需要同步扩展提取器及测试。
- Article 不虚构作者、发布日期或修改日期。已有其他类型（例如购买指南 HowTo）保留。
- 同类结构化数据统一为一个 JSON-LD graph，避免重复声明。

## 抓取与外链

`scripts/sync-routing.py` 维护 robots.txt 与 sitemap.xml。目前 sitemap 包含 103 个可索引页面，保留多语言 alternate；67 个已有 noindex 页面不加入。搜索、筛选、分页参数 URL 和跳转旧地址不加入 sitemap。

现有 MaisonLooks、Joyagoo 及 marketplace 商业域名链接添加 `sponsored nofollow`；新窗口链接同时保留 `noopener`。若将来添加新的商业合作域名，应更新 `scripts/seo.py` 的 commercial 列表并运行检查。

## 验证

用本机 Python 运行：

```text
python scripts/build-finds.py
python scripts/test-seo.py
python scripts/build-finds.py --check
python scripts/build-article-cluster.py --check
python scripts/verify-urls.py
```

SEO 检查覆盖全站标题与描述唯一性、head 单例、canonical、分享元数据、图片 alt、可见 FAQ 对应关系、文章类型、搜索目标、商业外链、完整 sitemap、无参数 URL 和重复生成稳定性。


## Shared indexability gates

scripts/indexability.py now supplies the publication rules used by both SEO robots metadata and sitemap generation. These rules exclude query/fragment routes, test/demo routes, unapproved product records, demo-only directories and marketplaces, and category routes with fewer than eight approved non-demo finds. Localized discovery pages use the same product-data gates as English pages. Translations must also pass the existing authored ready/completeness checks; this is a publication gate, not an automatic assessment of translation accuracy.

Sitemap language alternatives are restricted to URLs actually eligible for the sitemap. Non-indexable pages remain accessible to readers with noindex, follow. The robots file allows crawling so those directives can be read.

The shared SEO renderer validates a single H1 and image alt attributes and emits title, description, canonical, Open Graph, Twitter, Organization, WebSite, BreadcrumbList, and page-specific Article/visible FAQ schemas. Buying Guide steps and HowTo use one authored source. Commercial links carry sponsored nofollow noopener noreferrer; ordinary external links include noopener noreferrer.

Current output: 171 canonical pages, 65 sitemap URLs. Verify with test-seo.py, test-indexability.py, test-locales.py, verify-urls.py, and build-finds.py --check. These checks establish technical consistency; they do not guarantee search engine indexing or rich results.
