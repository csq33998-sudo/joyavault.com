# JoyaVault JSON-LD

以下 5 个代码块已接入对应页面的 head。每个代码块均包含完整 script 标签；手动接入时替换已有 JSON-LD，不要重复添加。FAQ 和 HowTo 内容来自对应页面正文。未添加未经确认的作者、发布日期或修改日期。

SearchAction 使用现有目录搜索 /en/best-joyagoo-finds/?q=。FAQ 和 HowTo 是 Schema.org 标记，不代表 Google 富媒体结果资格。

## /en/

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://joyavault.com/#organization",
      "name": "JoyaVault",
      "url": "https://joyavault.com/en/",
      "description": "Independent product discovery and buying guides. Not the official Joyagoo website."
    },
    {
      "@type": "WebSite",
      "@id": "https://joyavault.com/#website",
      "url": "https://joyavault.com/en/",
      "name": "JoyaVault",
      "description": "Find Joyagoo spreadsheet picks, explore shoes and accessories, and choose your next buying step with JoyaVault's independent browsing guides.",
      "inLanguage": "en",
      "publisher": {
        "@id": "https://joyavault.com/#organization"
      },
      "potentialAction": {
        "@type": "SearchAction",
        "target": {
          "@type": "EntryPoint",
          "urlTemplate": "https://joyavault.com/en/best-joyagoo-finds/?q={search_term_string}"
        },
        "query-input": "required name=search_term_string"
      }
    }
  ]
}
</script>
```

## /en/joyagoo-spreadsheet/

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Article",
      "@id": "https://joyavault.com/en/joyagoo-spreadsheet/#article",
      "url": "https://joyavault.com/en/joyagoo-spreadsheet/",
      "headline": "Joyagoo Spreadsheet 2026 Guide",
      "description": "Learn what a Joyagoo spreadsheet is good at, where it becomes slow, and which category or guide pages help you narrow products faster.",
      "inLanguage": "en",
      "image": [
        "https://joyavault.com/assets/social/joyagoo-spreadsheet-og.jpg"
      ],
      "mainEntityOfPage": {
        "@type": "WebPage",
        "@id": "https://joyavault.com/en/joyagoo-spreadsheet/",
        "breadcrumb": {
          "@id": "https://joyavault.com/en/joyagoo-spreadsheet/#breadcrumb"
        }
      },
      "publisher": {
        "@type": "Organization",
        "@id": "https://joyavault.com/#organization",
        "name": "JoyaVault",
        "url": "https://joyavault.com/en/",
        "description": "Independent product discovery and buying guides. Not the official Joyagoo website."
      }
    },
    {
      "@type": "BreadcrumbList",
      "@id": "https://joyavault.com/en/joyagoo-spreadsheet/#breadcrumb",
      "itemListElement": [
        {
          "@type": "ListItem",
          "position": 1,
          "name": "Home",
          "item": "https://joyavault.com/en/"
        },
        {
          "@type": "ListItem",
          "position": 2,
          "name": "Joyagoo Spreadsheet",
          "item": "https://joyavault.com/en/joyagoo-spreadsheet/"
        }
      ]
    },
    {
      "@type": "FAQPage",
      "@id": "https://joyavault.com/en/joyagoo-spreadsheet/#faq",
      "url": "https://joyavault.com/en/joyagoo-spreadsheet/#faq",
      "inLanguage": "en",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "What should I open after the spreadsheet?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Usually a tighter category page such as shoes or accessories, or a buying guide if you are closer to checks, links, and the next official step."
          }
        },
        {
          "@type": "Question",
          "name": "Can I skip the spreadsheet and go to a category page directly?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Yes. Once the rough direction is clear, category pages are usually easier to scan than more rows."
          }
        },
        {
          "@type": "Question",
          "name": "Does the spreadsheet replace the official Joyagoo site?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "No. This site helps with discovery and browsing. Joyagoo handles your account, orders, payment, warehouse QC, and shipping."
          }
        }
      ]
    }
  ]
}
</script>
```

## /en/shoes/

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "CollectionPage",
      "@id": "https://joyavault.com/en/shoes/#webpage",
      "url": "https://joyavault.com/en/shoes/",
      "name": "Joyagoo Spreadsheet Shoes — Browse Footwear Finds Faster",
      "description": "Browse example shoe finds by brand and style, including sneakers, flats, boots and slides.",
      "inLanguage": "en",
      "isPartOf": {
        "@type": "WebSite",
        "@id": "https://joyavault.com/#website",
        "url": "https://joyavault.com/en/",
        "name": "JoyaVault"
      },
      "breadcrumb": {
        "@id": "https://joyavault.com/en/shoes/#breadcrumb"
      }
    },
    {
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {
          "@type": "ListItem",
          "position": 1,
          "name": "Home",
          "item": "https://joyavault.com/en/"
        },
        {
          "@type": "ListItem",
          "position": 2,
          "name": "Shoes",
          "item": "https://joyavault.com/en/shoes/"
        }
      ],
      "@id": "https://joyavault.com/en/shoes/#breadcrumb"
    }
  ]
}
</script>
```

## /en/accessories/

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "CollectionPage",
      "@id": "https://joyavault.com/en/accessories/#webpage",
      "url": "https://joyavault.com/en/accessories/",
      "name": "Joyagoo Spreadsheet Accessories — Bags, Jewelry & More",
      "description": "Browse example accessory finds, including bags, jewelry, watches, belts, sunglasses and hats.",
      "inLanguage": "en",
      "isPartOf": {
        "@type": "WebSite",
        "@id": "https://joyavault.com/#website",
        "url": "https://joyavault.com/en/",
        "name": "JoyaVault"
      },
      "breadcrumb": {
        "@id": "https://joyavault.com/en/accessories/#breadcrumb"
      }
    },
    {
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {
          "@type": "ListItem",
          "position": 1,
          "name": "Home",
          "item": "https://joyavault.com/en/"
        },
        {
          "@type": "ListItem",
          "position": 2,
          "name": "Accessories",
          "item": "https://joyavault.com/en/accessories/"
        }
      ],
      "@id": "https://joyavault.com/en/accessories/#breadcrumb"
    }
  ]
}
</script>
```

## /en/how-to-buy/

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "HowTo",
      "@id": "https://joyavault.com/en/how-to-buy/#buying-flow",
      "name": "How to Buy on Joyagoo — A Clearer Guide to the Official Flow",
      "description": "A clearer guide to the official Joyagoo buying flow. Learn how to find products, place orders, check QC photos, and ship internationally.",
      "inLanguage": "en",
      "step": [
        {
          "@type": "HowToStep",
          "position": 1,
          "name": "Find Your Product",
          "url": "https://joyavault.com/en/how-to-buy/#step-1",
          "text": "Start with the Spreadsheet Guide when your shortlist is still broad. If you already know what you want, open Shoes or Accessories and narrow the choice before moving into an order. Your aim is to leave browsing with a specific item and its original marketplace URL. Keep a short note about why you chose it, the option that caught your attention, and anything the listing has not answered. Check whether a card is a live source listing or a labeled example. A placeholder button is not a product link, and a directory image alone is not enough information to place an order."
        },
        {
          "@type": "HowToStep",
          "position": 2,
          "name": "Paste the Link on Joyagoo",
          "url": "https://joyavault.com/en/how-to-buy/#step-2",
          "text": "Open Joyagoo and paste the original Taobao, Weidian, or 1688 product URL into its search field. Compare the loaded item with your saved reference before continuing. Joyagoo also describes keyword or image search and a DIY order option when a listing cannot be retrieved through the normal search flow. If the result looks different, return to the original listing instead of assuming it is the same product. Check the title, main image, seller information, and available options. For a DIY order, be specific about the item you want and the details that are still unclear. Ask for clarification before submitting incomplete instructions."
        },
        {
          "@type": "HowToStep",
          "position": 3,
          "name": "Select Size, Color & Options",
          "url": "https://joyavault.com/en/how-to-buy/#step-3",
          "text": "Choose your size, color, quantity, and any other required options. Use the listing’s measurements rather than relying only on a familiar size label. Leave concise order notes for details that matter, such as the exact option you mean or a measurement you want checked. Review the completed selection before adding the item to your cart or paying. A practical note describes something observable. “Please check the selected black color and size label” is easier to act on than “make sure everything is perfect.” For shoes, keep your measurement reference nearby. For accessories, think about dimensions and intended use. Save the final option names so you have a clear reference when the warehouse photos arrive."
        },
        {
          "@type": "HowToStep",
          "position": 4,
          "name": "Pay and Wait for Warehouse",
          "url": "https://joyavault.com/en/how-to-buy/#step-4",
          "text": "Review the payment breakdown on Joyagoo, then pay for the selected goods and applicable delivery from the seller to the warehouse. International parcel shipping is a separate part of the process. Keep your order reference and follow the status in your account while purchasing and domestic delivery take place. Do not treat the first payment as a complete delivered total. Keep a simple note of the item cost, domestic delivery, optional services you select, and the later international shipping charge. If an order asks for your confirmation or an additional payment, read the explanation before responding. An item being purchased, dispatched by the seller, or stored at the warehouse represents a different stage."
        },
        {
          "@type": "HowToStep",
          "position": 5,
          "name": "Review QC Photos",
          "url": "https://joyavault.com/en/how-to-buy/#step-5",
          "text": "When the warehouse inspection photos are available, compare them with your saved listing and selected options. Check the visible color, quantity, labels, shape, and construction details that matter to you. Decide whether you are ready to keep the item or whether you need clarification, more detail, or an after-sales request before shipping it onward. A useful QC question points to a specific uncertainty: a size label you cannot read, a mark you cannot identify, or a dimension missing from the photos. Joyagoo lists additional detail photos as an optional service. Check its current return conditions promptly if you see a problem; seller eligibility, timing, and packaging can affect your options. Photos cannot establish how something will feel in use."
        },
        {
          "@type": "HowToStep",
          "position": 6,
          "name": "Submit for Shipping",
          "url": "https://joyavault.com/en/how-to-buy/#step-6",
          "text": "Choose the warehouse items you want to send, then review the delivery address, available shipping routes, and packing options. Compare the quote for the parcel you are actually preparing. Confirm the selected contents and packaging instructions, review the shipping payment, and submit the parcel when the details are right. Keep the address complete, including any apartment or unit information you need the carrier to use. Consider both protection and parcel size when choosing packaging. Joyagoo publishes different weighing rules for different routes, so a lighter parcel does not always produce the same saving on every line. If you need a firmer packing reference, review the available rehearsal-packing service and its current charge."
        },
        {
          "@type": "HowToStep",
          "position": 7,
          "name": "Track and Receive",
          "url": "https://joyavault.com/en/how-to-buy/#step-7",
          "text": "After dispatch, follow the parcel information provided in your Joyagoo account and keep the tracking number with your order notes. Check any carrier messages that require a response. The published delivery estimate is a reference, and the parcel can pass through several transport and delivery stages before it reaches you. When the parcel arrives, compare its contents with the items you submitted. Keep the packaging while you check the order, and record clear photos if something appears missing or damaged. If you need help, give the relevant support team the parcel reference and a concise explanation. A dated record of what you received is more useful than trying to reconstruct the details later."
        }
      ],
      "url": "https://joyavault.com/en/how-to-buy/",
      "mainEntityOfPage": {
        "@type": "WebPage",
        "@id": "https://joyavault.com/en/how-to-buy/",
        "breadcrumb": {
          "@id": "https://joyavault.com/en/how-to-buy/#breadcrumb"
        }
      }
    },
    {
      "@type": "BreadcrumbList",
      "@id": "https://joyavault.com/en/how-to-buy/#breadcrumb",
      "itemListElement": [
        {
          "@type": "ListItem",
          "position": 1,
          "name": "Home",
          "item": "https://joyavault.com/en/"
        },
        {
          "@type": "ListItem",
          "position": 2,
          "name": "How To Buy",
          "item": "https://joyavault.com/en/how-to-buy/"
        }
      ]
    },
    {
      "@type": "FAQPage",
      "@id": "https://joyavault.com/en/how-to-buy/#faq",
      "inLanguage": "en",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "What does Joyagoo handle?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Joyagoo handles your account, payment, communication with sellers, warehouse storage, QC photos, and international shipping."
          }
        },
        {
          "@type": "Question",
          "name": "What does this site handle?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "This site helps with discovery, picks, categories, and visual browsing. It does not process orders or payments."
          }
        }
      ],
      "url": "https://joyavault.com/en/how-to-buy/#faq"
    }
  ]
}
</script>
```

