# Internal links

The shared rules in `scripts/internal_links.py` render ordinary `<a href="...">` links directly into HTML. Homepages, spreadsheet guides, finds directories, buying guides and all category pages have contextual navigation in the main content. Every article and blog post ends with a Next Pages module containing 3–5 topic-specific destinations.

Translated pages prefer ready translations. Guides without translations (including Updates and Coupon Guide) link to English pages with an explicit `(English)` label and `lang="en"`.

The common `localization.decorate` pipeline applies these rules during home, category, article and locale builds and layout synchronization. For manually edited pages, run `python scripts/internal_links.py` to synchronize only the navigation. The operation is idempotent.

Verification:

```text
python scripts/internal_links.py --check
python scripts/test-internal-links.py
```

Add new category destinations to `CATEGORIES` and topic-specific article recommendations to `ARTICLE_LINKS`. The audit enumerates actual category and article pages, checks required links inside main content, validates destinations, and checks article module placement, link counts, labels and duplicates.


## Core route contracts

- Home: Spreadsheet Guide, Best Finds, Shoes, Clothing, Accessories, Buying Guide, QC and Shipping.
- Spreadsheet Guide: Best Finds, category routes, Buying Guide, QC and Shipping.
- Best Finds: Spreadsheet Guide, all five primary categories, Taobao/Weidian/1688, Buying Guide, QC and Shipping.
- Every category: Best Finds, Spreadsheet Guide, Buying Guide, QC and Shipping.
- Every article: one Next Pages module at the end, with 3–5 authored related destinations and no self-links.

English labels describe the destination: Joyagoo Spreadsheet Guide, Best Joyagoo Finds, QC Photo Checklist, Shipping Planning Guide, and How to Buy With Joyagoo. Localized pages use available translated labels and explicitly mark English fallbacks.

Run scripts/build-finds.py to rebuild all publishing pipelines; --check detects stale output. The static audit checks actual HTML without JavaScript, required routes, existing destinations, duplicate links, self-links, labels, and article endings. Current result: 93 modules, 29 articles, 541 generated navigation links; all 171 pages pass internal-link validation. Changes are local and have not been deployed.


## Stage-specific CTAs and external handoffs

scripts/conversion.py runs in the shared publishing pipeline. Finds offers Read QC Checklist; QC offers Browse Finds, Plan Shipping, Continue to Buying Guide; Shipping offers Browse Finds, Read Coupon and Fee Checklist, Continue to Buying Guide. CategoryPage provides Browse more in this category, Read Shipping Planning, Open Buying Guide. Home keeps its discovery and buying-guide actions.

FindCard retains View details and Open product source. Real source CTAs open a new tab with noopener noreferrer; commercial/affiliate sources additionally use sponsored nofollow. A visible handoff notice immediately follows external product CTAs and external action buttons, including the Joyagoo continuation. Demo source actions remain internal links to the pending-source explanation.

The global header now leads to the internal Finds directory. Rebuilds regenerate CTAs and notices without duplicates, and article Next Pages remains at the end. Check with scripts/test-conversion.py and scripts/build-finds.py --check.
