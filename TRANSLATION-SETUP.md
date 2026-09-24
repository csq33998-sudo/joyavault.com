# 全站静态翻译：Google Cloud Translation

目前已完成全站菜单接入、同页语言对应机制、翻译缓存、静态页面生成和自动检查。
**尚未调用翻译服务，尚未生成全站六种语言的新译文，尚未部署。**
旧版每种语言九个页面仍可访问。没有对应译文时菜单显示“译文暂不可用”，不跳转首页。

## 一次性账号配置

1. 在 [Google Cloud 控制台](https://console.cloud.google.com/) 创建或选择自己的项目。
2. 自行关联结算账号，启用 **Cloud Translation API**。该操作由账号所有者完成。
3. 创建用于本地构建的 API 密钥，并将 API 限制设置为 Cloud Translation API。
4. 在项目根目录的 `.env.translation.local` 中填入：

```dotenv
GOOGLE_TRANSLATE_API_KEY=你的密钥
```

此文件已被 Git 忽略，部署脚本不会复制它；不要把密钥发到聊天中、写入前端或提交到代码仓库。
配置模板为 `.env.translation.example`。浏览器和访客不需要此密钥。

## 操作顺序（在项目目录运行）

### 1. 查看去重后的翻译量，不联网、不收费

```powershell
.\translate-site.ps1 -Action estimate
```

精确统计保存在 `src/translations/estimate.json`。计量包括为保护品牌和商品名而使用的占位符。
Google NMT 标准价目前为每百万输入字符 20 美元，每月前 50 万字符以额度形式抵扣；
已有用量、币种、税费和套餐会影响实际账单，见 [官方价格](https://cloud.google.com/products/translate/pricing)。

### 2. 翻译（此步骤会调用 API，可能收费）

先运行 estimate，再把认可的字符上限填入命令；上限不足则在发请求前停止。

```powershell
# 先做德语，核对术语和实际效果。
.\translate-site.ps1 -Action translate -Languages de -MaxCharacters 250000
.\translate-site.ps1 -Action build -Languages de

# 验收后生成剩余五种语言。请先重跑 estimate 确认最新用量。
.\translate-site.ps1 -Action translate -Languages fr,pt,pl,it,ar -MaxCharacters 1100000
.\translate-site.ps1 -Action build -Languages fr,pt,pl,it,ar
```

示例上限基于本次检查的内容量，未来增加页面后可能需要调高。
译文逐批缓存；中断后再次运行只处理未保存的内容，不会重译已经完成的批次。
网络超时不会自动重试；服务端已处理但本地未收到结果的请求在再次执行时仍可能重复计费。

### 3. 检查与打包（不会自动上线）

```powershell
.\translate-site.ps1 -Action verify
node scripts/test-language-menu.cjs
node scripts/build-cloudflare.cjs
```

部署仍沿用 `CLOUDFLARE-DEPLOY.md`。`dist` 才是构建输出；旧 ZIP 不会自动更新。

## 生成结果与维护

- 每个英文页面保持路径尾部不变，例如 `/en/shoes/` 对应 `/de/shoes/`。
- 保持当前页面布局；正文、标题、描述、图片说明、无障碍标签及 JSON-LD 文案进入翻译目录。
- 商品名称、品牌、源站名称和外部 URL 受到保护；表单筛选值、商品 ID、CSS 和脚本代码不送翻译。
- 搜索数量、筛选数量、分页和主题按钮使用已保存的本地 UI 词典，不在线翻译。
- 对应页面存在时，站内链接切换到同一语言；语言切换保留查询参数和锚点。
- 阿拉伯语生成 `lang="ar"` 与 `dir="rtl"`。布局仍需进行真实浏览器验收。
- canonical、hreflang、站点地图随构建更新，继承英文页面的 noindex 限制。
- 翻译缓存位于 `src/translations/<语言>.json`，可直接修订 `translation` 值；再次 build 即可。
- 英文内容改变后，只新增翻译缺失的文本，再次生成相应语言。打包检查会拦截源内容已改变的旧译文。
- 新页面自动纳入扫描，无需把每个新路由硬编码到旧的九页语言表。
- 所有必需词条完整才生成该批页面；缺少译文不会伪造语言页或发布空壳。
- 中文不在新流程的目标语言和菜单中；历史 `/zh/` 地址暂时保留。

## 验证清单

- [ ] 配置完成，先翻译并构建德语。
- [ ] 抽查首页、商品详情、购买指南、法律页面和含链接的长段落。
- [ ] 核对品牌名、术语、数字及机器翻译质量；必要时修改翻译缓存。
- [ ] 检查手机、桌面与阿拉伯语布局，确认语言切换和筛选正常。
- [ ] 自动检查通过，重新打包，再发布并核对线上页面。

API 参考：[Google Cloud Translation Basic](https://docs.cloud.google.com/translate/docs/reference/rest/v2/translate)。
