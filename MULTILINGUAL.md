# 多语言页面维护

语言目录为 en、zh、de、fr、pt、pl、it、ar。英文保留现有长文与页面；七个新增语言为首批九类页面提供本地化阅读版本，不再通过浏览器逐词替换正文。

## 内容入口

`src/locales/<语言>.json` 包含导航文案、分类名称及九类页面的本地化正文、清单、FAQ、标题和描述。原始商品名称保留来源语言，并使用语言属性标识；示例商品名称和状态在界面中本地化。示例价格不是实时报价。

每个页面的 `status` 必须为 `ready` 才会生成公开 HTML。新增或修改译文时先设为 `draft`，校对完整正文、专业术语、来源边界和元数据，再改为 `ready`。这里的状态是发布门槛，不表示经过外部母语审校。上线前可进一步进行目标市场编辑审阅。

首批路由映射位于 `scripts/localization.py` 的 `PAGE_PATHS`。只包含 Home、Spreadsheet Guide、Buying Guide、Best Finds、Shoes、Clothing、Accessories、QC Checklist、Shipping Planning；其余内容仍为英文。将来新增页面应先完成对应语言内容，再加入路由映射。

## 构建与检查

```text
python scripts/build-finds.py
python scripts/build-finds.py --check
python scripts/test-locales.py
python scripts/verify-urls.py
```

统一构建依次生成英语数据页面、本地化页面、共享导航及 SEO 标记、路由和 sitemap。生成文章的脚本也读取同一语言配置，避免覆盖语言切换器或 hreflang。

页面撤回为 `draft` 后，构建会移除该脚本生成的 HTML，删除对应路由、sitemap 项和其他页面的 hreflang 引用。不会删除非生成器管理的文件；出现此类冲突时会报错。执行检查模式只报告差异，不写入文件。

## SEO 与切换行为

- 已完成的九类页面在 head 中互相列出八个语言版本，加上指向对应英文页的 x-default；canonical 始终指向自身。
- 其他英语页面仅标注真实存在的英文版本和 x-default，不编造未翻译页面。语言切换器为这些页面提供明确标注的其他语言首页链接。
- 切换器是可键盘操作的原生 details 和真实链接，不依赖 JavaScript，不按浏览器语言或历史 localStorage 自动跳转。
- sitemap 同时列出可索引的多语言 URL 和对应的 xhtml:link。没有翻译的地址不会重写为英文或空白模板。
- 阿拉伯语使用 `lang="ar"`、`dir="rtl"`、逻辑方向布局和隔离显示的价格；未译来源名标注原文语言。
- 中文采用简体中文；葡萄牙语正文采用巴西常用表达，按需求使用通用 `pt` 代码；阿拉伯语采用现代标准阿拉伯语。

本次未部署。后续上线时还应在实际域名验证状态码、canonical、语言切换和不存在译文的 404 行为。
