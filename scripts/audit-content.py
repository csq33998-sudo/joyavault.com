"""Read-only site audit; writes reports only, never changes pages or redirects."""
import csv
import json
import re
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from seo import Document, Element, visible_faqs
from site_routes import CANONICAL_ROUTES, ROOT, page_path

DATA=json.loads((ROOT/'src/data/finds.json').read_text(encoding='utf-8'))
RECORDS={r['detailUrl']:r for r in DATA}
OUT=ROOT/'audits/2026-09-08-content'
OUT.mkdir(parents=True,exist_ok=True)

def words(node):
    return ' '.join(words(c) if isinstance(c,Element) else c for c in node.children)

merges={
 '/en/best-joyagoo-finds/accessories/bags/':('/en/best-joyagoo-finds/accessories/','包袋尺寸、容量、肩带与五金对照；加入实际包袋记录'),
 '/en/brands/nike/':('/en/brands/','Nike 搜索语境与鞋服筛选说明，引用真实匹配记录'),
 '/en/brands/jordan/':('/en/best-joyagoo-finds/shoes/','复古鞋型比较、尺码测量与鞋底/左右脚 QC'),
 '/en/articles/best-sneaker-finds/':('/en/best-joyagoo-finds/shoes/','运动鞋比较维度、尺码案例和已有真实来源记录'),
 '/en/blog/category-discovery-notes-for-joyagoo-haul-planning/':('/en/joyagoo-spreadsheet/','按用途选择分类的决策表与一份完成的 shortlist'),
 '/en/blog/choosing-an-agent-route-after-category-research/':('/en/joyagoo-buying-guide/','选择购物服务前要核对的信息与不能确认时的处理方式'),
 '/en/blog/how-to-use-trending-lists-in-a-joyagoo-haul/':('/en/joyagoo-spreadsheet/','热门清单筛选：兴趣与购买意图、淘汰条件、记录样例'),
 '/en/blog/joyagoo-haul-guide-workflow-from-list-to-shipping/':('/en/joyagoo-buying-guide/','完整下单流程与各阶段退出/暂停条件'),
 '/en/blog/qc-notes-before-warehouse-consolidation/':('/en/articles/joyagoo-spreadsheet-qc-checklist/','QC 未通过时先暂停合箱的操作清单'),
 '/en/blog/review-notes-that-keep-haul-finds-organized/':('/en/joyagoo-spreadsheet/','可复制选品记录表：来源、选项、选择理由、QC 状态'),
 '/en/blog/shipping-route-planning-for-a-joyagoo-haul/':('/en/articles/joyagoo-spreadsheet-shipping-planning/','体积重比较、追踪阶段、无更新时应记录的信息'),
 '/en/blog/':('/en/articles/','按研究、QC、仓库、运费任务组织文章，并纳入迁移内容'),
 '/en/blog/routes/':('/en/articles/','归并重复文章入口；保留每个主题的独立摘要'),
}
for slug,section in {'hoodies':'胸围/衣长/袖长测量及厚度、版型比较','jerseys':'尺码、面料、印号位置及洗护信息比较','polo-shirts':'领型、胸围、衣长和面料比较','shorts':'腰围、裤长、裆长及口袋结构比较','t-shirts':'克重来源、胸围、衣长、印花位置比较'}.items():
    merges[f'/en/best-joyagoo-finds/clothing/{slug}/']=('/en/best-joyagoo-finds/clothing/',section+'；展示相应真实来源记录')

def recommend(route):
    parts=route.strip('/').split('/'); lang=parts[0]; tail='/'.join(parts[1:])
    if route in merges:
        target,sections=merges[route]
        why=('标题/品牌词与一行简介变化，主体仍为两个路由卡，无商品卡、FAQ、表格或细分实操内容。' if '/brands/' in route or '/best-joyagoo-finds/' in route else
             '只有简介、概述和通用入口，无法完成 sneaker comparison 任务。' if tail=='articles/best-sneaker-finds' else
             '与另一文章目录重复组织同一批短博客；不是独立研究目的地。' if tail in ('blog','blog/routes') else
             '仅几段概括性建议，缺少完成任务的例子和判断标准；与现有长指南意图重叠。')
        return '高','合并后301',why,sections,target
    if route in RECORDS:
        r=RECORDS[route]
        if r['isPlaceholder']:
            return '高（已noindex）','删除公开示例；保留至清理完成前noindex','示例价格、示例 marketplace、示意图，sourceUrl=#；模板化 QC/运费文字不是实际商品研究。','仅留开发样例；若改成真实记录，需可靠来源、核验日期、选项、原创比较、缺点与适合人群。','不301；确实移除后404/410'
        return '高（已noindex）','保留noindex并扩展；无维护价值则删除','单张保存图片/价格加通用 QC/运费提示，主按钮导向 MaisonLooks；marketplace=Unknown，缺少针对商品的实证。','原始来源与选项核验；测量/规格；2–3个真实替代项对比；具体优缺点；QC实例与成本假设；核验日期。','不按品牌或标题猜测同款；仅确认同一记录后合并'
    if tail in ('contact','privacy-policy','terms-of-service','editorial-policy'):
        return '信任缺口（已noindex）','保留并完成实际信息','页面明确写尚未公布完整政策/联系方式；属于功能信息缺失，不是关键词 doorway。','Contact：真实联系方式及职责；Privacy：实际数据处理；Terms：实际条款；Editorial：审核方法、商业披露与纠错途径。','不301'
    if tail.startswith('marketplaces/'):
        name={'taobao':'Taobao','weidian':'Weidian','1688':'1688'}[parts[-1]]
        n=sum(r['marketplace']==name for r in DATA)
        return '高','暂时noindex；核验真实选品后扩展并恢复索引',f'{n}张卡全部为示例，无一个经核实的该平台原始商品链接；正文有指南/表格/FAQ，但 finds 承诺缺少数据支撑。','真实平台原始链接、SKU/起订量/选项、实查日期；平台特有失败案例与比较；删除公开示例卡；不要编造商品填数量。','优先保留扩展；若放弃独立选品，合并到 /en/articles/taobao-weidian-1688-finds-guide/ 后301'
    if tail in ('best-joyagoo-finds/beauty-fragrance','best-joyagoo-finds/electronics'):
        return '高','暂时noindex；有真实研究才恢复','各8张商品卡均为示例；通用指南虽存在，但无法支撑可购买 finds 分类定位。','真实来源记录与核验；美妆补标签/成分信息来源/液体运输查证；电子补电池/电压/接口/兼容性依据；案例比较。','暂不301；若撤销并确实整合内容，可301到 /en/best-joyagoo-finds/'
    if tail=='best-joyagoo-finds/accessories':
        return '中高','扩展；优先移除示例卡','10条记录中9条示例，仅1条未核验保存记录；指南有独立价值，但选品证据明显偏弱。','真实包袋/配饰来源；材质与尺寸来源；五金/扣具QC实例；容量、佩戴尺度、用途决策表。','保留；不301'
    if tail=='best-joyagoo-finds' or tail=='':
        return '中','核心保留；清理示例并补编辑筛选',('英文首页和选品总页在HTML中包含63张卡，43条示例；真实保存记录也未核验；' if lang=='en' else '本地化首页展示8条保存记录，选品总页展示63条且43条示例；产品说明较少；')+'有导航/指南/FAQ，不能仅因导向外站就认定 thin affiliate，但需要可验证的选择依据。','公开卡移除示例；来源核验与更新日期；为何入选/不适合谁；真实对比；区分首页概览与选品搜索任务。','保留；不301'
    if tail in ('best-joyagoo-finds/shoes','best-joyagoo-finds/clothing'):
        return '中','核心保留并扩展','鞋类17条中8条示例，衣类20条中10条示例；其余也只是未核验保存记录。已有分类指南/FAQ，不是只有换关键词。','去除示例；实际尺码和测量例子、面料/鞋型对比、针对记录的优缺点、来源检查日期。','保留；不301'
    if tail=='joyagoo-spreadsheet-updates':
        return '中','保留；补真实编辑更新记录','约千词的指南中心有独立价值，但 Latest/Updates 目前是常青文章入口，缺少具体变化和更新依据。','日期、变更摘要、原始来源、受影响范围、用户下一步；真实死链修复记录；未核实优惠/物流状态不可写成实时更新。','保留；不301'
    if tail=='brands':
        return '低至中','保留风格hub并扩展证据','6条风格路线有用途/QC提醒/FAQ和独立声明；不是品牌官方店。但部分筛选结果仍依赖示例，不能支撑真实推荐。','真实匹配记录、每条路线匹配理由、风格差异对照、QC图片或可核实规格。','保留；不301'
    if lang!='en':
        return '低至中','保留本地化框架；按任务补深度','有本地语言实质介绍、检查清单和可见FAQ，并非仅翻译标题；但较英文完整指南明显简化，缺少实操示例。语言等价页本身不构成doorway。','购买页补失败/暂停路径；QC补图片或测量案例；运费补明确假设的计算例；spreadsheet补已填写记录表。由本地语言编辑复核。','保留各语言自canonical；不301到英文'
    return '低','核心保留','页面提供对应任务的独立指南/文章或有摘要的文章目录；没有仅因字数或不含商品卡而删除的依据。','增加可核验案例与编辑维护信息；文章目录按任务分组，不为凑字数重复指南正文。','保留；不301'

rows=[]; titles=Counter(); descs=Counter()
for route in CANONICAL_ROUTES:
    doc=Document(page_path(route).read_text(encoding='utf-8')).root; main=doc.all('main')[0]
    meta={m.attrs.get('name',m.attrs.get('property','')):m.attrs.get('content','') for m in doc.all('meta')}
    title=doc.all('title')[0].text(); titles[title]+=1; descs[meta['description']]+=1
    noindex='noindex' in meta.get('robots','').lower()
    risk,action,why,sections,target=recommend(route)
    cards=[n for n in main.all('article') if 'data-find-id' in n.attrs or 'local-product' in n.attrs.get('class','')]
    rows.append(dict(url=route,index_status='noindex' if noindex else 'indexable',risk=risk,action=action,reason=why,sections=sections,redirect=target,
        text_units=len(re.findall(r"\b[\w]+(?:['’-][\w]+)*\b",words(main))),h2=len(main.all('h2')),faq=len(visible_faqs(doc)),tables=len(main.all('table')),lists=len(main.all('ul'))+len(main.all('ol')),cards=len(cards),
        external_main=sum(bool(urlsplit(a.attrs.get('href','')).hostname) and urlsplit(a.attrs['href']).hostname!='joyavault.com' for a in main.all('a')),title=title,description=meta['description']))
with (OUT/'page-inventory.csv').open('w',encoding='utf-8-sig',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)

report='''# JoyaVault 内容质量审计 — 2026-09-08

范围：工作区当前全部170个canonical HTML页面，含8个语言目录；103个可索引、67个已noindex。已核对页面正文、元数据、卡片数据、指南/FAQ/表格/列表及主内容外链。线上主页与sitemap本次未能读取，因此这不是线上收录或Search Console处罚诊断。旧URL重定向别名不当成独立内容页。没有修改网页、noindex、sitemap或跳转规则。

判断依照 [Google spam policies](https://developers.google.com/search/docs/essentials/spam-policies)：重点是页面是否提供独立价值，是否用相似入口捕获查询再把用户导往同一处。下面是风险判断，不是Google已判定违规。没有固定合格字数；FAQ、表格、结构化数据与sponsored属性也不能替代真实价值。未核实外部佣金关系或逐句比对外站，不声称已证明联盟分成或抄袭。

## 主要结论

- 高优先级合并：6个旧细分类页、2个旧品牌页、1个旧sneaker文章、7篇短博客、2个博客目录，共18个可索引页面。细分类/品牌页主体只有一句简介与两个路由卡，属于最强doorway风险信号。
- 商品证据是系统性短板：63条记录中43条为公开示例，20条为未核验的MaisonLooks保存记录；20条的原始marketplace均为Unknown。不能将这些称为63条真实已验证选品。
- Taobao/Weidian/1688的17/13/13条卡全部是示例。Beauty & Fragrance与Electronics各8条也全是示例。建议这5个可索引页面暂noindex，先补真实来源；已有长文、FAQ和表格不解决商品承诺缺口。
- Accessories仅1条保存记录、9条示例，英文及7个本地化版本均需优先扩展。Shoes为9条保存+8条示例；Clothing为10条保存+10条示例。
- 63个详情页已经noindex：43个示例移出公开站点；20个保存记录保持noindex直到有商品级独立研究。无需为了清理而把不相关商品一律301到首页。
- 4个政策/联系页已经noindex，问题是实际信息缺失；应补完整，不应当作SEO流量页堆字。
- 全170页精确重复title：0组；精确重复description：0组。两个同名短裤记录仅通过记录编号区分了标题，这解决标签重复，不证明正文或商品不同。
- 63个非英语版本不是仅更换语言关键词：有本地介绍、清单、FAQ，但深度比英文指南短。保留真正完成用户任务的翻译；选品证据不足会被同步放大。不要把所有本地化页301到英文，也不要仅因翻译语义一致判为doorway。

## 推荐301清单（均为建议，尚未执行）

先将有用内容和对应细分类说明整合到目标页，再301；同步更新站内链接、canonical/hreflang、sitemap及旧别名，避免跳转链。目标需覆盖原页面意图，不是随便选流量更高的页。

| 原页面 | 更强目标 | 合并前目标需补充 |
|---|---|---|
'''
for route,(target,section) in merges.items():
    report+=f'| `{route}` | `{target}` | {section} |\n'
report+='''
不建议批量301的页面：示例商品删除后返回404/410；20个未核验详情先保持noindex；同名短裤需确认是不是同一商品/同一来源再决定是否合并。Marketplace默认扩展而不是301；只有放弃其独立选品任务时，才把平台特有内容合入marketplace比较指南后301。

## 应保留的核心SEO页面

- `/en/joyagoo-spreadsheet/`：核心概念与研究总入口，补一份真实完成的研究记录样例。
- `/en/joyagoo-buying-guide/`：购买流程入口，补阶段决策/暂停条件与可核实界面示例。
- `/en/best-joyagoo-finds/`：真实选品与比较主目录，移除示例、记录核验状态、说明入选与淘汰理由。
- `/en/best-joyagoo-finds/shoes/`、`/en/best-joyagoo-finds/clothing/`：分类核心；补商品级对比与测量实例。
- `/en/best-joyagoo-finds/accessories/`：保留分类架构，但真实记录不足，不能视为已经完成的强选品页。
- `/en/`：品牌/任务导航首页，与spreadsheet指南区分意图，避免两页追逐同一套介绍和商品网格。
- `/en/articles/`：文章导航hub；有摘要的有效目录不用强行写成千字文章。
- `/en/brands/`：风格研究hub，保留独立声明，确保风格筛选结果有真实内容。
- `/en/joyagoo-spreadsheet-updates/`：保留更新中心，但补真正的变更日期、证据、影响与下一步，不能把常青卡片包装成实时更新。
- 七篇长文章：`joyagoo-spreadsheet-qc-checklist`、`joyagoo-spreadsheet-shipping-planning`、`joyagoo-spreadsheet-coupon-fee-checklist`、`taobao-weidian-1688-finds-guide`、`joyagoo-spreadsheet-vs-raw-spreadsheet`、`dead-product-link-fix`、`warehouse-consolidation-checklist`（均位于`/en/articles/`）。这些有独立任务、清单、决策表和至少4个FAQ，宜保留并补可核验例子。
- 对应本地化核心页：保留各语言自己的URL与canonical，以任务完成程度决定是否继续索引，不以统一字数门槛判断。当前QC/运费短版应补本地语言实操例；不要编造各国税费或物流政策。

## 全部页面逐页结论

下表每个URL独立列出风险、原因、动作和需要补充的内容。完整可筛选数据见同目录page-inventory.csv。CSV的text_units是去除head/header/footer后的词元计数，包含正文导航/卡片，中文等不能按英文词数比较；数字用于定位短壳页，不是排名或质量评分。cards包含示例，绝不能等同真实商品数。lists只是列表数，不自动等于高质量checklist。

'''
for title,predicate in [('需要合并的旧入口',lambda r:r['url'] in merges),('英文指南、目录与分类',lambda r:r['url'].startswith('/en/') and r['url'] not in merges and r['url'] not in RECORDS),('商品详情：逐条处理',lambda r:r['url'] in RECORDS),('多语言页面：逐条处理',lambda r:not r['url'].startswith('/en/'))]:
    report+=f'### {title}\n\n| URL / 当前索引 | 风险与原因 | 建议 | 要补充的section |\n|---|---|---|---|\n'
    for r in filter(predicate,rows):
        report+=f"| `{r['url']}` · {r['index_status']} | **{r['risk']}**：{r['reason']} | {r['action']} | {r['sections']} |\n"
    report+='\n'
report+='''## 执行顺序

1. 将公开示例移出真实finds网格；维持详情noindex，不把营销标签当真实商品资料。
2. 暂noindex上述3个marketplace及2个全示例分类；从sitemap移除对应项，保持可抓取以便读取noindex。
3. 完成18个旧入口的内容归并，再实施逐条301与站内链接更新。
4. 优先核验已有20条保存记录，而不是扩充更多模板行。针对商品提供实测/可追溯规格与原创判断；没有证据的真实性、库存、配送承诺不要写。
5. 完成政策与编辑责任信息；修正privacy中仍提到旧的语言localStorage/外站搜索行为，按实际实现描述。
6. 先把英文核心内容和商品证据做实，再同步各语言；移除示例不等于用另一种语言重新发布示例。

本报告不包含Search Console曝光/点击、外部链接或抓取日志。执行301/删除前，用这些数据检查有无值得迁移的历史需求；这不改变已发现的薄壳页和示例数据事实。
'''
(OUT/'content-risk-audit.md').write_text(report,encoding='utf-8')
print(json.dumps({'pages':len(rows),'indexable':sum(r['index_status']=='indexable' for r in rows),'redirect_candidates':len(merges),'duplicate_title_groups':sum(v>1 for v in titles.values()),'duplicate_description_groups':sum(v>1 for v in descs.values()),'risk_groups':dict(Counter(r['risk'] for r in rows)),'report':str(OUT/'content-risk-audit.md')},ensure_ascii=False))
