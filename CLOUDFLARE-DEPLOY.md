# JoyaVault — Cloudflare Pages 上线

## 构建

在项目根目录运行（需要 Node.js）：

```powershell
node scripts/build-cloudflare.cjs
```

输出为 `dist/`。脚本只重建带有自身标记的 dist；不要在其中手工维护文件。
脚本保留源页面，复制公开资源，生成首页入口、404、统计配置、缓存头及重定向。
页面目录的 index.html 由 Pages 原生提供，不添加可能引起循环的 200 重写。
后续增加公开资源目录时，更新脚本中的复制白名单。

打包可上传的 ZIP（不要把 dist 外层目录包进去）：

```powershell
Get-ChildItem dist -Force | Where-Object Name -ne '.joyavault-pages-build' | Compress-Archive -DestinationPath joyavault-cloudflare.zip -Force
```

## 方式一：直接上传

1. 登录 https://dash.cloudflare.com/，进入 Workers & Pages，创建应用，选择 Pages 的静态文件上传入口。
2. 项目名称输入 joyavault，上传 joyavault-cloudflare.zip，部署。
3. 检查分配的 pages.dev 地址，首页应跳到 /en/。
4. 下次更新：重新构建和打包，在同一个项目创建新的生产部署。

网页上传上限为 1,000 个文件、单文件 25 MiB。超过文件数量时使用 Git 集成或 Wrangler。
Direct Upload 项目不能直接切换为 Git 集成项目。需要自动部署时，从开始就选择方式二。

## 方式二：GitHub 自动部署

1. 将源码仓库上传 GitHub；Cloudflare 可连接私有仓库，不要求公开源码。
2. Pages 创建项目时选择连接 Git，授权并选择该仓库。
3. Framework preset：None。
4. Build command：`node scripts/build-cloudflare.cjs`。
5. Build output directory：`dist`。
6. Production branch：选择仓库实际的生产分支。
7. 部署后，每次提交到生产分支将触发重新构建。

不必将 dist 提交到仓库。当前 .gitignore 已忽略 dist。
构建所需源页面、assets、css、js、根目录 CSS、robots.txt、sitemap.xml、vercel.json、src/data/analytics.json，以及两个 build 脚本必须提交。
统计 ID 可由 Cloudflare 构建环境变量 GA4_MEASUREMENT_ID 覆盖；留空字符串可禁用初始化。

## 域名与 HTTPS

1. 在 Cloudflare 添加 joyavault.com，选择 Free。
2. 核对并保留现有邮箱 MX/TXT 等记录。
3. 在域名注册商处更换为 Cloudflare 实际分配的两个 Nameserver。若启用了 DNSSEC，按迁移指引处理旧 DS 记录。
4. 等待域名 Active。
5. 在 Pages 项目 Custom domains 依次添加 joyavault.com 和 www.joyavault.com，由向导创建记录。
6. 对应 CNAME 的目标应是项目实际分配的 pages.dev 主机名；根域名由 Cloudflare flattening 处理。不添加其他托管商的 A 记录。
7. 等待自定义域名及证书 Active，开启域名的 Always Use HTTPS。
8. 使用 Redirect Rules 将 www.joyavault.com 301 跳转到裸域名，保留路径与查询参数。

动态目标表达式：`concat("https://joyavault.com", http.request.uri.path)`，勾选保留查询参数。
必须先在 Pages 添加域名，不能仅创建 DNS 记录。

## 缓存与压缩

- HTML、JS 配置、robots、sitemap：每次使用前验证。
- 根目录 CSS 与 css/：1 小时；assets/（包括其中的 CSS）：1 天。
- 同名资源更新可能保留到缓存期限；需要立即更新时更换资源 URL 并更新引用。
- 不为未版本化资源使用一年 immutable。
- pages.dev 及预览域名加 noindex；正式域名不受影响。
- Cloudflare 自动处理传输压缩；不要手写 Content-Encoding。
- 需要指定 Brotli/Gzip 时，在域名的 Compression Rules 选择 Enable Brotli and Gzip compression。
- 本次不批量转换图片；已有图片按原样发布。

## 上线验证清单

- 根路径 301 到 /en/；各语言页和商品页打开正常。
- 旧 .html、/index.html、无尾斜杠路径没有跳转循环。
- 随机不存在的 URL 返回 HTTP 404，而不是首页 200。
- HTTP 转 HTTPS，www 转裸域名并保留路径与参数。
- CSS、JS、图片无 404，统计配置正确。
- robots.txt 和 sitemap.xml 可以访问。
- 检查 Cache-Control、Content-Encoding；正式域名不应带 X-Robots-Tag: noindex。
- 本地构建和文件检查不等于 Cloudflare 线上路由、证书与 DNS 已验证；部署后完成上述检查。

官方参考：
- https://developers.cloudflare.com/pages/get-started/direct-upload/
- https://developers.cloudflare.com/pages/configuration/custom-domains/
- https://developers.cloudflare.com/pages/configuration/headers/
- https://developers.cloudflare.com/pages/configuration/redirects/
