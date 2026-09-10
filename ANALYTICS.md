# GA4 event tracking

All 171 HTML pages load the small, shared tracker with `defer`. The Google tag loads asynchronously only when `GA4_MEASUREMENT_ID` is set. If `window.gtag` already exists, it is reused without loading or configuring a second tag. With no measurement ID and no existing gtag, tracking is inactive and links work normally.

## Enable

Set the public measurement ID (for example, `G-XXXXXXXXXX`) as `GA4_MEASUREMENT_ID` in the deployment environment. The Vercel build command runs `node scripts/build-analytics.cjs`, which writes only that allowlisted value into `js/analytics-config.js`. The build helper is explicitly included in `.vercelignore`. Redeploy after changing the value. Leave the variable empty for environments where collection should be disabled.

For a local build in PowerShell:

```powershell
$env:GA4_MEASUREMENT_ID = 'G-XXXXXXXXXX'
node scripts/build-analytics.cjs
```

`.env.example` documents the variable. This static project does not automatically load `.env` files; provide an environment variable when running the build. The checked-in config is empty. No real GA property has been configured or contacted as part of implementation.

## Event definitions

| Event | When | Parameters |
| --- | --- | --- |
| `search_submit` | English search form submission; Enter on localized live search | `query` (trimmed), `page_path` |
| `category_click` | Category or subcategory link; category filter selection | `category` (route slug or lowercase filter value), `page_path` |
| `marketplace_click` | Marketplace route, marketplace filter, or directory link with marketplace parameter | `marketplace` (lowercase), `page_path` |
| `find_card_click` | A link within a product card, including its source link | `find_id`, `title`, `category`, `marketplace` from the source dataset |
| `external_product_click` | A marked product source link on a card or detail page | `find_id`, `source_domain` (destination hostname), `destination_url` (complete href), `page_path` |
| `joyagoo_click` | External link to joyagoo.com or its subdomains | `page_path`, `cta_location` |
| `guide_click` | Spreadsheet guide, buying guide or article link | `guide_name` (stable, language-independent route slug), `page_path` |
| `language_switch` | Language menu link to another language | `from_language`, `to_language` |

`page_path` is the source page pathname without query parameters. Typing alone does not emit search events; resets do not emit category selections. Language-menu links do not also emit guide/category events. A product source clicked inside a card intentionally emits both card and external-product events. Pending sources link to an internal explanation: they can emit a card click but never an external-product event. `cta_location` uses `data-cta-location` when provided, otherwise header, footer, find_card, enclosing section ID, or main.

## Delivery and performance

The tracker uses delegated listeners rather than individual handlers or a product-data download. Event calls happen in the capture phase before normal link navigation. Events request beacon transport. A same-tab external click waits for event callbacks with an independent 180 ms fallback; failures cannot strand the visitor. New-tab, middle-click, modifier-key and download actions retain native behavior without waiting. Callback completion is not a guarantee of receipt by GA; blocked requests, browser shutdown or unavailable connectivity can still prevent delivery.

Google documents the callback controls in its [gtag parameter reference](https://developers.google.com/tag-platform/gtagjs/reference/parameters).

## Validation

```text
node scripts/test-analytics.cjs
python scripts/test-analytics-markup.py
```

The first test runs the production tracker in a simulated browser event environment and checks all eight events, initialization, duplicate protection, navigation order and failure fallbacks. The second audits every rendered HTML page and product metadata against the source records. Existing finds, locales, SEO and internal-link tests should also pass. These are automated checks, not live GA receipt verification.

After configuring a real measurement ID and deploying, confirm events in GA4 Realtime or Tag Assistant/DebugView. To use parameters in standard reports, register the needed event-scoped custom dimensions in GA4. Avoid treating high-cardinality fields such as full URLs, titles and search queries as routine report dimensions.


The main scripts/build-finds.py build also regenerates analytics configuration when GA4_MEASUREMENT_ID is explicitly present in the environment. When it is absent, the existing generated configuration is preserved; set it to an empty value to disable initialization. --check does not change configuration. Update trust pages after changing analytics configuration so the privacy notice reflects the active build.

Verified in real Chrome using a local gtag recorder: all eight events fire from actual page controls, and an existing gtag is reused without another Google script. The tests do not send events to Google. A real measurement ID is still required to enable collection and verify receipt in the intended property.
