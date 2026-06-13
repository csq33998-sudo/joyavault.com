(function () {
  const languages = [
    { code: "en", short: "EN", label: "English", dir: "ltr" },
    { code: "zh", short: "\u4e2d", label: "\u4e2d\u6587", dir: "ltr" },
    { code: "pl", short: "PL", label: "Polski", dir: "ltr" },
    { code: "de", short: "DE", label: "Deutsch", dir: "ltr" },
    { code: "fr", short: "FR", label: "Francais", dir: "ltr" },
    { code: "it", short: "IT", label: "Italiano", dir: "ltr" },
    { code: "pt", short: "PT", label: "Portugues", dir: "ltr" },
    { code: "es", short: "ES", label: "Espanol", dir: "ltr" },
    { code: "nl", short: "NL", label: "Nederlands", dir: "ltr" },
    { code: "da", short: "DA", label: "Dansk", dir: "ltr" },
    { code: "sv", short: "SV", label: "Svenska", dir: "ltr" },
    { code: "ar", short: "AR", label: "\u0627\u0644\u0639\u0631\u0628\u064a\u0629", dir: "rtl" },
    { code: "cs", short: "CS", label: "Cestina", dir: "ltr" }
  ];

  const base = {
    zh: {
      Home: "\u9996\u9875", Finds: "\u9009\u54c1", Brand: "\u54c1\u724c", Brands: "\u54c1\u724c", Guide: "\u6307\u5357", Guides: "\u6307\u5357", Articles: "\u6587\u7ae0", Blog: "\u535a\u5ba2", Shop: "\u5546\u5e97", Night: "\u591c\u95f4", Day: "\u65e5\u95f4", Search: "\u641c\u7d22", All: "\u5168\u90e8", View: "\u67e5\u770b", Category: "\u5206\u7c7b", Categories: "\u5206\u7c7b", Marketplace: "\u5e73\u53f0", Route: "\u8def\u7531", Routes: "\u8def\u7531", Core: "\u6838\u5fc3", Workflow: "\u6d41\u7a0b", Article: "\u6587\u7ae0", Overview: "\u6982\u89c8", Comparison: "\u5bf9\u6bd4", Quality: "\u8d28\u68c0", Start: "\u5f00\u59cb", Sneakers: "\u7403\u978b", Hoodies: "\u536b\u8863", Shorts: "\u77ed\u88e4", Accessories: "\u914d\u9970", Jerseys: "\u7403\u8863",
      "Streetwear Spreadsheet": "\u8857\u5934\u670d\u9970\u9009\u54c1\u8868", "MaisonLooks Streetwear Spreadsheet": "MaisonLooks \u8857\u5934\u670d\u9970\u9009\u54c1\u8868", "Browse Finds": "\u6d4f\u89c8\u9009\u54c1", "Brand routes": "\u54c1\u724c\u8def\u7531", "JoyaGoo spreadsheet": "JoyaGoo \u9009\u54c1\u8868", "Built for discovery": "\u4e3a\u53d1\u73b0\u597d\u7269\u800c\u5efa", "Better than a raw spreadsheet": "\u6bd4\u539f\u59cb\u8868\u683c\u66f4\u597d\u7528", "Featured finds": "\u7cbe\u9009\u9009\u54c1", "Searchable starter spreadsheet": "\u53ef\u641c\u7d22\u5165\u95e8\u9009\u54c1\u8868", "Brand hubs": "\u54c1\u724c\u5165\u53e3", "Browse by brand and category intent": "\u6309\u54c1\u724c\u548c\u5206\u7c7b\u610f\u56fe\u6d4f\u89c8", "Open Brand route": "\u6253\u5f00\u54c1\u724c\u8def\u7531", "Core spreadsheet routes": "\u6838\u5fc3\u9009\u54c1\u8868\u8def\u7531", "Read all guides": "\u9605\u8bfb\u5168\u90e8\u6307\u5357", "Finds Spreadsheet": "\u9009\u54c1\u8868", "Brand Finds Spreadsheet": "\u54c1\u724c\u9009\u54c1\u8868", "Independent route": "\u72ec\u7acb\u8def\u7531", "Spreadsheet routes": "\u9009\u54c1\u8868\u8def\u7531", "Spreadsheet rows": "\u9009\u54c1\u8868\u6761\u76ee", "All finds": "\u5168\u90e8\u9009\u54c1", "Articles and FAQ": "\u6587\u7ae0\u4e0e FAQ", "Buying Guide": "\u8d2d\u4e70\u6307\u5357", "How to use the spreadsheet before shopping.": "\u8d2d\u7269\u524d\u5982\u4f55\u4f7f\u7528\u9009\u54c1\u8868\u3002", "Search Nike, hoodie, bag...": "\u641c\u7d22 Nike\u3001\u536b\u8863\u3001\u5305...", "Search sneakers, hoodies, Nike...": "\u641c\u7d22\u7403\u978b\u3001\u536b\u8863\u3001Nike..."
    },
    de: { Home: "Start", Finds: "Finds", Brand: "Marke", Brands: "Marken", Guide: "Guide", Guides: "Guides", Articles: "Artikel", Blog: "Blog", Shop: "Shop", Night: "Nacht", Day: "Tag", Search: "Suchen", All: "Alle", View: "Ansehen", Category: "Kategorie", Categories: "Kategorien", Marketplace: "Marktplatz", Route: "Route", Routes: "Routen", Core: "Kern", Workflow: "Ablauf", Article: "Artikel", Overview: "Uberblick", Sneakers: "Sneaker", Hoodies: "Hoodies", Shorts: "Shorts", Accessories: "Accessoires", "Browse Finds": "Finds ansehen", "Brand routes": "Markenrouten", "Built for discovery": "Fur Discovery gebaut", "Better than a raw spreadsheet": "Besser als ein rohes Spreadsheet", "Featured finds": "Ausgewahlte Finds", "Searchable starter spreadsheet": "Durchsuchbares Starter-Spreadsheet", "Brand hubs": "Marken-Hubs", "Read all guides": "Alle Guides lesen", "Independent route": "Eigenstandige Route", "Spreadsheet routes": "Spreadsheet-Routen", "All finds": "Alle Finds", "Buying Guide": "Kaufguide" },
    fr: { Home: "Accueil", Finds: "Finds", Brand: "Marque", Brands: "Marques", Guide: "Guide", Guides: "Guides", Articles: "Articles", Shop: "Boutique", Night: "Nuit", Day: "Jour", Search: "Rechercher", All: "Tout", View: "Voir", Category: "Categorie", Categories: "Categories", Marketplace: "Marketplace", Route: "Route", Routes: "Routes", Core: "Core", Workflow: "Flux", Article: "Article", Overview: "Apercu", Sneakers: "Sneakers", Hoodies: "Hoodies", Shorts: "Shorts", Accessories: "Accessoires", "Browse Finds": "Voir les finds", "Brand routes": "Routes marque", "Built for discovery": "Concu pour la decouverte", "Better than a raw spreadsheet": "Mieux qu'un spreadsheet brut", "Featured finds": "Finds en vedette", "Searchable starter spreadsheet": "Spreadsheet de depart consultable", "Brand hubs": "Hubs de marques", "Read all guides": "Lire tous les guides", "Independent route": "Route independante", "All finds": "Tous les finds", "Buying Guide": "Guide d'achat" },
    it: { Home: "Home", Finds: "Finds", Brand: "Brand", Brands: "Brand", Guide: "Guide", Guides: "Guide", Articles: "Articoli", Shop: "Shop", Night: "Notte", Day: "Giorno", Search: "Cerca", All: "Tutto", View: "Vedi", Category: "Categoria", Categories: "Categorie", Marketplace: "Marketplace", Route: "Rotta", Routes: "Rotte", Core: "Core", Workflow: "Flusso", Article: "Articolo", Overview: "Panoramica", Sneakers: "Sneaker", Hoodies: "Hoodie", Shorts: "Shorts", Accessories: "Accessori", "Browse Finds": "Sfoglia finds", "Brand routes": "Rotte brand", "Built for discovery": "Pensato per la discovery", "Better than a raw spreadsheet": "Meglio di uno spreadsheet grezzo", "Featured finds": "Finds in evidenza", "Searchable starter spreadsheet": "Spreadsheet iniziale cercabile", "Brand hubs": "Hub brand", "Read all guides": "Leggi tutte le guide", "Independent route": "Rotta indipendente", "All finds": "Tutti i finds", "Buying Guide": "Guida acquisto" },
    es: { Home: "Inicio", Finds: "Finds", Brand: "Marca", Brands: "Marcas", Guide: "Guia", Guides: "Guias", Articles: "Articulos", Shop: "Tienda", Night: "Noche", Day: "Dia", Search: "Buscar", All: "Todo", View: "Ver", Category: "Categoria", Categories: "Categorias", Marketplace: "Marketplace", Route: "Ruta", Routes: "Rutas", Core: "Core", Workflow: "Flujo", Article: "Articulo", Overview: "Resumen", Sneakers: "Sneakers", Hoodies: "Hoodies", Shorts: "Shorts", Accessories: "Accesorios", "Browse Finds": "Ver finds", "Brand routes": "Rutas de marca", "Built for discovery": "Creado para descubrir", "Better than a raw spreadsheet": "Mejor que una spreadsheet bruta", "Featured finds": "Finds destacados", "Searchable starter spreadsheet": "Spreadsheet inicial buscable", "Brand hubs": "Hubs de marca", "Read all guides": "Leer todas las guias", "Independent route": "Ruta independiente", "All finds": "Todos los finds", "Buying Guide": "Guia de compra" },
    pt: { Home: "Inicio", Finds: "Finds", Brand: "Marca", Brands: "Marcas", Guide: "Guia", Guides: "Guias", Articles: "Artigos", Shop: "Loja", Night: "Noite", Day: "Dia", Search: "Pesquisar", All: "Todos", View: "Ver", Category: "Categoria", Categories: "Categorias", Marketplace: "Marketplace", Route: "Rota", Routes: "Rotas", Core: "Core", Workflow: "Fluxo", Article: "Artigo", Overview: "Visao geral", Sneakers: "Sneakers", Hoodies: "Hoodies", Shorts: "Shorts", Accessories: "Acessorios", "Browse Finds": "Ver finds", "Brand routes": "Rotas de marca", "Built for discovery": "Criado para descoberta", "Better than a raw spreadsheet": "Melhor que uma spreadsheet bruta", "Featured finds": "Finds em destaque", "Searchable starter spreadsheet": "Spreadsheet inicial pesquisavel", "Brand hubs": "Hubs de marcas", "Read all guides": "Ler todos os guias", "Independent route": "Rota independente", "All finds": "Todos os finds", "Buying Guide": "Guia de compra" },
    nl: { Home: "Home", Finds: "Finds", Brand: "Merk", Brands: "Merken", Guide: "Gids", Guides: "Gidsen", Articles: "Artikelen", Shop: "Shop", Night: "Nacht", Day: "Dag", Search: "Zoeken", All: "Alles", View: "Bekijk", Category: "Categorie", Categories: "Categorieen", Marketplace: "Marketplace", Route: "Route", Routes: "Routes", Core: "Kern", Workflow: "Workflow", Article: "Artikel", Overview: "Overzicht", Sneakers: "Sneakers", Hoodies: "Hoodies", Shorts: "Shorts", Accessories: "Accessoires", "Browse Finds": "Bekijk finds", "Brand routes": "Merkroutes", "Built for discovery": "Gebouwd voor discovery", "Better than a raw spreadsheet": "Beter dan een ruwe spreadsheet", "Featured finds": "Uitgelichte finds", "Searchable starter spreadsheet": "Doorzoekbare startspreadsheet", "Brand hubs": "Merkenhubs", "Read all guides": "Lees alle gidsen", "Independent route": "Onafhankelijke route", "All finds": "Alle finds", "Buying Guide": "Koopgids" },
    pl: { Home: "Start", Finds: "Finds", Brand: "Marka", Brands: "Marki", Guide: "Poradnik", Guides: "Poradniki", Articles: "Artykuly", Shop: "Sklep", Night: "Noc", Day: "Dzien", Search: "Szukaj", All: "Wszystko", View: "Zobacz", Category: "Kategoria", Categories: "Kategorie", Marketplace: "Marketplace", Route: "Trasa", Routes: "Trasy", Core: "Core", Workflow: "Proces", Article: "Artykul", Overview: "Przeglad", Sneakers: "Sneakersy", Hoodies: "Bluzy", Shorts: "Szorty", Accessories: "Akcesoria", "Browse Finds": "Przegladaj finds", "Brand routes": "Trasy marek", "Built for discovery": "Stworzone do odkrywania", "Better than a raw spreadsheet": "Lepsze niz surowy spreadsheet", "Featured finds": "Wyroznione finds", "Searchable starter spreadsheet": "Przeszukiwalny spreadsheet startowy", "Brand hubs": "Huby marek", "Read all guides": "Czytaj poradniki", "Independent route": "Osobna trasa", "All finds": "Wszystkie finds", "Buying Guide": "Poradnik zakupowy" },
    da: { Home: "Hjem", Finds: "Finds", Brand: "Brand", Brands: "Brands", Guide: "Guide", Guides: "Guides", Articles: "Artikler", Shop: "Shop", Night: "Nat", Day: "Dag", Search: "Sog", All: "Alle", View: "Vis", Category: "Kategori", Categories: "Kategorier", Marketplace: "Marketplace", Route: "Rute", Routes: "Ruter", Core: "Core", Workflow: "Flow", Article: "Artikel", Overview: "Overblik", Sneakers: "Sneakers", Hoodies: "Hoodies", Shorts: "Shorts", Accessories: "Accessories", "Browse Finds": "Se finds", "Brand routes": "Brand-ruter", "Built for discovery": "Bygget til discovery", "Better than a raw spreadsheet": "Bedre end et rat spreadsheet", "Featured finds": "Fremhaevede finds", "Searchable starter spreadsheet": "Sogbart starter-spreadsheet", "Brand hubs": "Brand-hubs", "Read all guides": "Laes alle guides", "Independent route": "Selvstaendig rute", "All finds": "Alle finds", "Buying Guide": "Kobsguide" },
    sv: { Home: "Hem", Finds: "Finds", Brand: "Varumarke", Brands: "Varumarken", Guide: "Guide", Guides: "Guider", Articles: "Artiklar", Shop: "Shop", Night: "Natt", Day: "Dag", Search: "Sok", All: "Alla", View: "Visa", Category: "Kategori", Categories: "Kategorier", Marketplace: "Marketplace", Route: "Rutt", Routes: "Rutter", Core: "Core", Workflow: "Flode", Article: "Artikel", Overview: "Oversikt", Sneakers: "Sneakers", Hoodies: "Hoodies", Shorts: "Shorts", Accessories: "Accessoarer", "Browse Finds": "Bladdra finds", "Brand routes": "Varumarkesrutter", "Built for discovery": "Byggt for discovery", "Better than a raw spreadsheet": "Battre an ett ratt spreadsheet", "Featured finds": "Utvalda finds", "Searchable starter spreadsheet": "Sokbart starter-spreadsheet", "Brand hubs": "Varumarkeshubbar", "Read all guides": "Las alla guider", "Independent route": "Fristaende rutt", "All finds": "Alla finds", "Buying Guide": "Kopguide" },
    ar: { Home: "\u0627\u0644\u0631\u0626\u064a\u0633\u064a\u0629", Finds: "\u0627\u0644\u0627\u0643\u062a\u0634\u0627\u0641\u0627\u062a", Brand: "\u0627\u0644\u0639\u0644\u0627\u0645\u0629", Brands: "\u0627\u0644\u0639\u0644\u0627\u0645\u0627\u062a", Guide: "\u0627\u0644\u062f\u0644\u064a\u0644", Guides: "\u0627\u0644\u0623\u062f\u0644\u0629", Articles: "\u0627\u0644\u0645\u0642\u0627\u0644\u0627\u062a", Shop: "\u062a\u0633\u0648\u0642", Night: "\u0644\u064a\u0644\u064a", Day: "\u0646\u0647\u0627\u0631\u064a", Search: "\u0628\u062d\u062b", All: "\u0627\u0644\u0643\u0644", View: "\u0639\u0631\u0636", Category: "\u0627\u0644\u0641\u0626\u0629", Categories: "\u0627\u0644\u0641\u0626\u0627\u062a", Marketplace: "\u0627\u0644\u0633\u0648\u0642", Route: "\u0645\u0633\u0627\u0631", Routes: "\u0645\u0633\u0627\u0631\u0627\u062a", Core: "\u0623\u0633\u0627\u0633\u064a", Workflow: "\u0627\u0644\u062a\u062f\u0641\u0642", Article: "\u0645\u0642\u0627\u0644", Overview: "\u0646\u0638\u0631\u0629", Sneakers: "\u0623\u062d\u0630\u064a\u0629", Hoodies: "\u0647\u0648\u062f\u064a", Shorts: "\u0634\u0648\u0631\u062a", Accessories: "\u0625\u0643\u0633\u0633\u0648\u0627\u0631\u0627\u062a", "Browse Finds": "\u062a\u0635\u0641\u062d \u0627\u0644\u0627\u0643\u062a\u0634\u0627\u0641\u0627\u062a", "Brand routes": "\u0645\u0633\u0627\u0631\u0627\u062a \u0627\u0644\u0639\u0644\u0627\u0645\u0627\u062a", "Built for discovery": "\u0645\u0635\u0645\u0645 \u0644\u0644\u0627\u0643\u062a\u0634\u0627\u0641", "Featured finds": "\u0627\u0643\u062a\u0634\u0627\u0641\u0627\u062a \u0645\u062e\u062a\u0627\u0631\u0629", "Independent route": "\u0645\u0633\u0627\u0631 \u0645\u0633\u062a\u0642\u0644", "All finds": "\u0643\u0644 \u0627\u0644\u0627\u0643\u062a\u0634\u0627\u0641\u0627\u062a", "Buying Guide": "\u062f\u0644\u064a\u0644 \u0627\u0644\u0634\u0631\u0627\u0621" },
    cs: { Home: "Domu", Finds: "Finds", Brand: "Znacka", Brands: "Znacky", Guide: "Pruvodce", Guides: "Pruvodci", Articles: "Clanky", Shop: "Obchod", Night: "Noc", Day: "Den", Search: "Hledat", All: "Vse", View: "Zobrazit", Category: "Kategorie", Categories: "Kategorie", Marketplace: "Marketplace", Route: "Trasa", Routes: "Trasy", Core: "Core", Workflow: "Postup", Article: "Clanek", Overview: "Prehled", Sneakers: "Tenisky", Hoodies: "Mikiny", Shorts: "Kratasy", Accessories: "Doplnky", "Browse Finds": "Prochazet finds", "Brand routes": "Trasy znacek", "Built for discovery": "Vytvoreno pro objevovani", "Better than a raw spreadsheet": "Lepsi nez surovy spreadsheet", "Featured finds": "Vybrane finds", "Searchable starter spreadsheet": "Prohledavatelny starter spreadsheet", "Brand hubs": "Huby znacek", "Read all guides": "Cist vsechny pruvodce", "Independent route": "Samostatna trasa", "All finds": "Vsechny finds", "Buying Guide": "Nakupni pruvodce" }
  };

  const replacements = {
    zh: [["Spreadsheet", "\u9009\u54c1\u8868"], ["spreadsheet", "\u9009\u54c1\u8868"], ["Finds", "\u9009\u54c1"], ["finds", "\u9009\u54c1"], ["Streetwear", "\u8857\u5934\u670d\u9970"], ["streetwear", "\u8857\u5934\u670d\u9970"], ["Sneaker", "\u7403\u978b"], ["sneaker", "\u7403\u978b"], ["Hoodie", "\u536b\u8863"], ["hoodie", "\u536b\u8863"], ["Bag", "\u5305\u888b"], ["bag", "\u5305"], ["Brand", "\u54c1\u724c"], ["brand", "\u54c1\u724c"], ["category", "\u5206\u7c7b"], ["marketplace", "\u5e73\u53f0"], ["routes", "\u8def\u7531"], ["rows", "\u6761\u76ee"], ["guide", "\u6307\u5357"], ["shopping", "\u8d2d\u7269"], ["discovery", "\u53d1\u73b0"], ["Compare", "\u5bf9\u6bd4"], ["Browse", "\u6d4f\u89c8"], ["Use", "\u4f7f\u7528"], ["All", "\u5168\u90e8"]],
    de: [["Spreadsheet", "Spreadsheet"], ["Finds", "Finds"], ["Streetwear", "Streetwear"], ["category", "Kategorie"], ["marketplace", "Marktplatz"], ["routes", "Routen"], ["rows", "Zeilen"], ["guide", "Guide"], ["shopping", "Shopping"], ["discovery", "Discovery"], ["Compare", "Vergleiche"], ["Browse", "Durchsuche"], ["Use", "Nutze"], ["All", "Alle"]],
    fr: [["Spreadsheet", "spreadsheet"], ["category", "categorie"], ["marketplace", "marketplace"], ["routes", "routes"], ["rows", "lignes"], ["guide", "guide"], ["shopping", "shopping"], ["discovery", "decouverte"], ["Compare", "Comparer"], ["Browse", "Parcourir"], ["Use", "Utiliser"], ["All", "Tous"]],
    it: [["category", "categoria"], ["marketplace", "marketplace"], ["routes", "rotte"], ["rows", "righe"], ["guide", "guida"], ["shopping", "shopping"], ["discovery", "discovery"], ["Compare", "Confronta"], ["Browse", "Sfoglia"], ["Use", "Usa"], ["All", "Tutti"]],
    es: [["category", "categoria"], ["marketplace", "marketplace"], ["routes", "rutas"], ["rows", "filas"], ["guide", "guia"], ["shopping", "compra"], ["discovery", "descubrimiento"], ["Compare", "Compara"], ["Browse", "Explora"], ["Use", "Usa"], ["All", "Todos"]],
    pt: [["category", "categoria"], ["marketplace", "marketplace"], ["routes", "rotas"], ["rows", "linhas"], ["guide", "guia"], ["shopping", "compra"], ["discovery", "descoberta"], ["Compare", "Compare"], ["Browse", "Navegue"], ["Use", "Use"], ["All", "Todos"]],
    nl: [["category", "categorie"], ["marketplace", "marketplace"], ["routes", "routes"], ["rows", "rijen"], ["guide", "gids"], ["shopping", "shoppen"], ["discovery", "discovery"], ["Compare", "Vergelijk"], ["Browse", "Bekijk"], ["Use", "Gebruik"], ["All", "Alle"]],
    pl: [["category", "kategoria"], ["marketplace", "marketplace"], ["routes", "trasy"], ["rows", "wiersze"], ["guide", "poradnik"], ["shopping", "zakupy"], ["discovery", "odkrywanie"], ["Compare", "Porownaj"], ["Browse", "Przegladaj"], ["Use", "Uzyj"], ["All", "Wszystkie"]],
    da: [["category", "kategori"], ["marketplace", "marketplace"], ["routes", "ruter"], ["rows", "raekker"], ["guide", "guide"], ["shopping", "shopping"], ["discovery", "discovery"], ["Compare", "Sammenlign"], ["Browse", "Gennemse"], ["Use", "Brug"], ["All", "Alle"]],
    sv: [["category", "kategori"], ["marketplace", "marketplace"], ["routes", "rutter"], ["rows", "rader"], ["guide", "guide"], ["shopping", "shopping"], ["discovery", "upptackt"], ["Compare", "Jamfor"], ["Browse", "Bladdra"], ["Use", "Anvand"], ["All", "Alla"]],
    ar: [["Spreadsheet", "\u062c\u062f\u0648\u0644"], ["Finds", "\u0627\u0643\u062a\u0634\u0627\u0641\u0627\u062a"], ["Streetwear", "\u0623\u0632\u064a\u0627\u0621 \u0627\u0644\u0634\u0627\u0631\u0639"], ["category", "\u0641\u0626\u0629"], ["marketplace", "\u0633\u0648\u0642"], ["routes", "\u0645\u0633\u0627\u0631\u0627\u062a"], ["rows", "\u0635\u0641\u0648\u0641"], ["guide", "\u062f\u0644\u064a\u0644"], ["shopping", "\u062a\u0633\u0648\u0642"], ["discovery", "\u0627\u0643\u062a\u0634\u0627\u0641"], ["Compare", "\u0642\u0627\u0631\u0646"], ["Browse", "\u062a\u0635\u0641\u062d"], ["Use", "\u0627\u0633\u062a\u062e\u062f\u0645"], ["All", "\u0643\u0644"]],
    cs: [["category", "kategorie"], ["marketplace", "marketplace"], ["routes", "trasy"], ["rows", "radky"], ["guide", "pruvodce"], ["shopping", "nakupovani"], ["discovery", "objevovani"], ["Compare", "Porovnejte"], ["Browse", "Prochazet"], ["Use", "Pouzijte"], ["All", "Vsechny"]]
  };

  const originalText = new WeakMap();
  const originalPlaceholder = new WeakMap();
  const originalTitle = document.title;
  let applying = false;

  function getLanguage() {
    return localStorage.getItem("ml_language") || "en";
  }

  function getInfo() {
    return languages.find((item) => item.code === getLanguage()) || languages[0];
  }

  function cleanKey(value) {
    return String(value || "").replace(/\s+/g, " ").trim();
  }

  function applyReplacements(value, lang) {
    let output = value;
    (replacements[lang] || []).forEach(([from, to]) => {
      output = output.split(from).join(to);
    });
    return output;
  }

  function t(key) {
    const clean = cleanKey(key);
    const lang = getLanguage();
    if (!clean || lang === "en") return clean;
    const pack = base[lang] || {};
    if (pack[clean]) return pack[clean];
    const replaced = applyReplacements(clean, lang);
    return replaced === clean ? clean : replaced;
  }

  function shouldSkip(node) {
    const parent = node.parentElement;
    return !parent || ["SCRIPT", "STYLE", "NOSCRIPT", "TEXTAREA"].includes(parent.tagName) || parent.closest(".language-switcher");
  }

  function translateTextNodes(root) {
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    const nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    nodes.forEach((node) => {
      if (shouldSkip(node) || !node.nodeValue.trim()) return;
      const parent = node.parentElement;
      const key = parent && parent.dataset && parent.dataset.i18nKey ? parent.dataset.i18nKey : null;
      if (key) {
        node.nodeValue = node.nodeValue.replace(node.nodeValue.trim(), t(key));
        return;
      }
      if (!originalText.has(node)) originalText.set(node, cleanKey(node.nodeValue));
      const translated = t(originalText.get(node));
      node.nodeValue = node.nodeValue.replace(node.nodeValue.trim(), translated);
    });
  }

  function translateAttributes(root) {
    root.querySelectorAll("input[placeholder], textarea[placeholder], [title], [aria-label]").forEach((node) => {
      if (node.closest(".language-switcher")) return;
      if (node.hasAttribute("placeholder")) {
        if (!originalPlaceholder.has(node)) originalPlaceholder.set(node, node.getAttribute("placeholder"));
        node.setAttribute("placeholder", t(originalPlaceholder.get(node)));
      }
      ["title", "aria-label"].forEach((attr) => {
        if (!node.hasAttribute(attr)) return;
        const key = `mlOriginal${attr.replace("-", "")}`;
        if (!node.dataset[key]) node.dataset[key] = node.getAttribute(attr);
        node.setAttribute(attr, t(node.dataset[key]));
      });
    });
  }

  function mountLanguageMenu() {
    document.querySelectorAll(".nav-actions").forEach((actions) => {
      if (actions.querySelector(".language-switcher")) return;
      actions.insertAdjacentHTML("afterbegin", `
        <div class="language-switcher">
          <button class="language-toggle" type="button" aria-label="Language" aria-expanded="false">
            <span class="language-current-code"></span>
          </button>
          <div class="language-menu" hidden></div>
        </div>
      `);
    });

    document.querySelectorAll(".language-switcher").forEach((switcher) => {
      const toggle = switcher.querySelector(".language-toggle");
      const menu = switcher.querySelector(".language-menu");
      if (!toggle || !menu || menu.dataset.ready) return;
      menu.dataset.ready = "true";
      menu.innerHTML = languages.map((language) => `
        <button class="language-option" type="button" data-language="${language.code}">
          <span class="language-flag" aria-hidden="true">${language.short}</span>
          <span>${language.label}</span>
        </button>
      `).join("");
      toggle.addEventListener("click", () => {
        const open = menu.hidden;
        menu.hidden = !open;
        toggle.setAttribute("aria-expanded", String(open));
      });
      menu.addEventListener("click", (event) => {
        const option = event.target.closest("[data-language]");
        if (!option) return;
        setLanguage(option.dataset.language);
        menu.hidden = true;
        toggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  function applyLanguage(root = document.body) {
    if (!root || applying) return;
    applying = true;
    const info = getInfo();
    document.documentElement.lang = getLanguage();
    document.documentElement.dir = info.dir;
    document.title = t(originalTitle);
    document.querySelectorAll(".language-current-code").forEach((node) => { node.textContent = info.short; });
    document.querySelectorAll(".language-option").forEach((node) => {
      node.classList.toggle("is-active", node.dataset.language === getLanguage());
    });
    translateTextNodes(root);
    translateAttributes(root);
    applying = false;
  }

  function setLanguage(lang) {
    localStorage.setItem("ml_language", lang);
    applyLanguage();
    window.dispatchEvent(new CustomEvent("ml:languagechange", { detail: { language: lang } }));
    setTimeout(() => applyLanguage(), 0);
  }

  document.addEventListener("click", (event) => {
    document.querySelectorAll(".language-switcher").forEach((switcher) => {
      if (switcher.contains(event.target)) return;
      const menu = switcher.querySelector(".language-menu");
      const toggle = switcher.querySelector(".language-toggle");
      if (menu && toggle) {
        menu.hidden = true;
        toggle.setAttribute("aria-expanded", "false");
      }
    });
  });

  const observer = new MutationObserver((mutations) => {
    if (applying) return;
    mutations.forEach((mutation) => {
      mutation.addedNodes.forEach((node) => {
        if (node.nodeType === Node.ELEMENT_NODE) applyLanguage(node);
      });
    });
  });

  window.ML_I18N = { t, getLanguage, setLanguage, applyLanguage, languages };
  mountLanguageMenu();
  applyLanguage();
  observer.observe(document.body, { childList: true, subtree: true });
})();
