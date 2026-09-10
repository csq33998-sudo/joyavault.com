"""Editorial category content. Signals describe research paths, not stock availability."""
CATEGORIES = {
'shoes': {
'name':'Shoes', 'title':'Best Joyagoo Shoes Finds | Sizing & QC Guide',
'description':'Explore shoe finds with fit, sole, stitching, and box-weight checks. Compare sneakers, boots, loafers, sandals, and heels before following a source.',
'intro':'Start here if you are building an everyday rotation, replacing a familiar pair, or comparing a shape you have not worn before. Use your foot measurements and intended use to narrow the directory before getting attached to a photograph.',
'why':'Footwear is easier to compare when fit comes first. A recognizable silhouette cannot tell you the usable internal length, forefoot room, or feel of the sole. Keep those questions beside each saved listing so the shortlist reflects how you will wear the shoes.',
'signals': [('Sneakers','Compare toe shape, outsole profile, and the sizing evidence for the exact version.'),('Boots','Look at shaft height, opening width, fastening, and the space needed for socks.'),('Loafers','Check the heel hold, instep opening, and whether measurements describe the foot or the shoe.'),('Sandals','Study strap adjustment and the usable footbed length, including space at the toes.'),('Heels','Record heel height, platform height, and fastening details before judging proportions.')],
'checks':[('Size','Measure both feet and compare the larger measurement with the listing’s own chart. Ask what its length measurement refers to.'),('Sole','Request clear outsole and side views to inspect tread, edge finishing, and visible separation.'),('Stitching','Look across both shoes for interrupted seams, loose threads, and uneven panels.'),('Box weight','Ask for packed weight and dimensions with the shoe box. Discuss protection before choosing to remove packaging.')],
'faq':[('Can I use my usual shoe size?','Treat it as a starting point. Compare measured foot length and width with the exact listing, and resolve unclear size conversions before ordering.'),('Which QC photos help most with shoes?','Ask for paired top views, side profiles, heels, outsoles, and a close view of the size label. Photos help with visible details but cannot confirm comfort.'),('Should I keep the shoe box?','Compare the packed quote with your need for protection or storage. Removing a box can change protection as well as parcel dimensions.'),('Are all the subcategories available here?','The signals cover research paths. The featured grid contains only records currently assigned to Shoes; a signal is not a stock promise.')],
'cta':'Build a shortlist around the fit you need.',
'extra':[('/en/brands/nike/','Nike finds','Continue comparing Air Force 1, Air Max, Shox, and collaboration listing references.'),('/en/brands/jordan/','Jordan finds','Explore the existing AJ4 and AJ13 listing routes.')]
},
'clothing': {
'name':'Clothing','title':'Best Joyagoo Clothing Finds | Fit & Fabric Guide',
'description':'Compare clothing finds through garment measurements, fabric details, length, and print placement, with research paths for tops, hoodies, and layers.',
'intro':'This route suits shoppers planning a wardrobe around fit, layering, or a particular outfit. Bring the measurements of a garment you already like, then compare the details that affect how a new piece will sit on your body.',
'why':'A consistent measurement reference makes mixed clothing listings easier to read. Separate the look you want from the evidence supplied: an oversized styling photo does not establish chest width, sleeve length, or fabric weight.',
'signals':[('Tops','Compare chest width, shoulder shape, and neckline construction against a familiar garment.'),('Hoodies','Record body and sleeve length, hood shape, and room for a layer underneath.'),('Bottoms','Compare waist, rise, inseam, and leg opening rather than relying on a single size label.'),('Outerwear','Allow for layers and inspect closures, lining information, and pocket placement.'),('Sets','Confirm the measurements and selected size of each piece; matching names do not guarantee matching fit.')],
'checks':[('Size chart','Distinguish body measurements from garment measurements. Check the stated tolerance and how the seller measures.'),('Fabric','Record the supplied composition and ask for close views of texture and construction. A photograph cannot confirm fiber content.'),('Length','Compare body, sleeve, or inseam length with a garment measured in the same way.'),('Print placement','Compare print position with seams and the center line. Request a flat view rather than judging a folded garment.')],
'faq':[('What should I measure first?','Use a garment that fits the way you want. Measure its relevant widths and lengths on a flat surface and compare equivalent points.'),('Does an oversized label explain the fit?','No. It describes an intended look; actual garment measurements determine the room you will have.'),('Can QC photos confirm the fabric?','They can show texture and visible construction. Keep supplied composition information separate from what a photograph can establish.'),('How do I compare a two-piece set?','Record the top and bottom measurements separately, including the selected variant for each. Check whether the listing sells both pieces together.')],
'cta':'Choose the measurements before choosing the size.', 'extra':[]
},
'accessories': {
'name':'Accessories','title':'Best Joyagoo Accessories Finds | Detail & QC Guide',
'description':'Explore bags, eyewear, belts, jewelry, watches, and headwear research with checks for hardware, straps, alignment, and protective packaging.',
'intro':'Use this category when you are looking for a finishing piece or a practical everyday accessory. Start with the objects it must hold, the fit you need, or the way you plan to wear it, then inspect the smaller construction details.',
'why':'Accessories can look similar in a thumbnail while differing in usable dimensions and closures. Writing down practical requirements helps you compare a compact bag, a long strap, or a watch case without relying on brand labels alone.',
'signals':[('Bags','Compare internal space, opening size, and pocket layout with what you carry.'),('Eyewear','Record lens, bridge, and temple measurements; appearance does not establish protective performance.'),('Belts','Check the usable fastening range and buckle dimensions rather than total length alone.'),('Jewelry','Record dimensions, closure details, and the material information provided by the source.'),('Watches','Compare case thickness, strap adjustment range, and the supplied movement information.'),('Headwear','Look for circumference measurements, adjustment range, and crown depth.')],
'checks':[('Hardware','Inspect zipper pulls, clasps, buckles, and attachment points from more than one angle.'),('Strap','Confirm length, adjustment range, width, and how the strap joins the body of the item.'),('Logo alignment','Compare visible placement against seams and edges. Neat alignment does not prove authenticity.'),('Packaging','Ask how lenses, watch faces, rigid shapes, and small removable parts will be protected.')],
'faq':[('What makes a bag useful beyond its listed size?','The opening and internal layout matter. Compare the space with the largest item you intend to carry and check how the bag closes.'),('Can a logo close-up establish authenticity?','No. It can help inspect placement and visible finishing, but it is not proof of origin or authenticity.'),('How should I compare watch fit?','Record case diameter and thickness, then check the strap or bracelet adjustment range against your wrist.'),('Which accessories need extra packing questions?','Ask about protection for lenses, exposed hardware, watch faces, and shapes that could be crushed. Confirm what packaging the quote includes.')],
'cta':'Keep useful details beside every accessory you save.',
'extra':[('/en/best-joyagoo-finds/accessories/bags/','Bag finds','Continue into the existing bag research route.'),('/en/brands/','Browse brands','Compare the directory’s brand routes without treating a label as verification.')]
},
'beauty-fragrance': {
'name':'Beauty & Fragrance','title':'Best Joyagoo Beauty & Fragrance Finds | Research Guide',
'description':'Research beauty and fragrance listings with product-label, leakage, and shipping-acceptance questions before adding a liquid or spray to your shortlist.',
'intro':'This page is for shoppers organizing fragrance or personal-care research before deciding whether an item is suitable to order. Begin with the exact product information and the service’s acceptance requirements, rather than treating a bottle photograph as enough evidence.',
'why':'Product identification and transport questions belong at the start of this shortlist. Record the product name, volume, concentration where relevant, and supplied ingredient information so different variants do not become indistinguishable saved links.',
'signals':[('Perfume','Separate concentration, bottle volume, and delivery format when comparing fragrance references.'),('Grooming','Identify the exact product type, supplied instructions, and whether a kit contains liquids or powered items.'),('Personal Care','Read the supplied label and ingredients for the specific variant; keep manufacturer information with the listing.')],
'checks':[('Restrictions','Ask your chosen service to assess the exact item and destination. Keep its response with the listing rather than assuming a broad category is accepted.'),('Leakage','Inspect closure and seal information, and ask what containment and protective packing are available.'),('Shipping limitations','Describe whether the item is a liquid, spray, or another format when requesting acceptance and a quote. Do not infer acceptance from other parcels.'),('Product information','Retain label and packaging photographs and compare the supplied name, size, and variant with manufacturer information. A link does not establish authenticity.')],
'faq':[('Does a perfume record mean it can be shipped to me?','No. Directory inclusion does not confirm transport acceptance. Ask your service about the exact product and destination before ordering.'),('What should I save from a fragrance listing?','Keep the product name, concentration, bottle volume, format, label photographs, seller reference, and the date you checked the information.'),('Can I judge the contents from packaging photos?','Packaging can help identify the claimed variant and visible condition. It cannot verify the contents or their authenticity.'),('Are the featured records verified offers?','The current category uses clearly marked examples with no seller source. Their prices and marketplace labels are illustrative research data.')],
'cta':'Resolve product and shipping questions before ordering.', 'extra':[]
},
'electronics': {
'name':'Electronics','title':'Best Joyagoo Electronics Finds | Compatibility Guide',
'description':'Browse electronics research with battery, plug, compatibility, and shipping questions for audio, phone accessories, wearables, and personal-care devices.',
'intro':'Start here if you need an accessory to work with a device you already own. Write down that device’s exact model and required connection first, then use the directory to organize specification and transport questions before opening a source.',
'why':'An accessory can resemble the right product while using a different connector, power input, or supported model. A specification-led shortlist makes those differences visible before price becomes the deciding factor.',
'signals':[('Audio','Record connectors, supported connection methods, included cables, and the source of power.'),('Phone Accessories','Match the exact phone model, port, case dimensions, and required function.'),('Wearables','Check supported phones or operating systems, sizing, and how charging is handled.'),('Small Devices','Identify the intended function, dimensions, power input, supplied attachments, and operating instructions.')],
'checks':[('Battery','Ask whether a battery is included and obtain the available battery specifications for the service assessing the shipment.'),('Plug','Compare the supplied plug and stated input requirements with the destination. Similar connectors do not establish electrical compatibility.'),('Compatibility','Match exact model identifiers and supported functions with manufacturer information; a shared brand name is insufficient.'),('Shipping restrictions','Give the service the exact product and battery details before requesting a route and quote. Check packing requirements for the accepted item.')],
'faq':[('Is a matching connector enough?','No. Check the supported function, power requirements, and exact device model as well as the physical connector.'),('What should I ask about charging?','Confirm the stated input, cable and charger contents, and whether the product needs a separate power supply.'),('Can QC photos show that a device works?','They can show labels, connectors, and visible condition. Ask what functional checks are available and what those checks actually cover.'),('Can every battery item use the same shipping route?','Do not assume so. Provide the exact item and available battery details to the service and obtain acceptance for the intended destination.')],
'cta':'Start with your device, then check the specification.', 'extra':[]
}}


# Separate visual QC questions from transport planning for each category.
CATEGORIES['shoes']['checks'] = [
    ('Fit and size labels', 'Compare labels on both shoes with the selected size. Ask whether insole measurements represent usable internal length; photos cannot establish comfort.'),
    ('Pair symmetry', 'Request both shoes side by side to compare toe shape, heel height, panel placement, and color.'),
    ('Soles and seams', 'Inspect outsole tread, sole joins, stitching, and edges for visible gaps or loose threads.')]
CATEGORIES['shoes']['shipping'] = [
    ('Box or no box', 'Request packed weight and dimensions with the shoe box before comparing alternatives. Removing a box changes protection as well as parcel size.'),
    ('Protect the shape', 'Ask how toe boxes, boot shafts, and heels will be supported without pressing against one another.'),
    ('Compare the packed parcel', 'Use the packed dimensions for your quote, especially for tall boots or multiple pairs; the shoe weight alone is not the parcel weight.')]
CATEGORIES['clothing']['shipping'] = [
    ('Bulky layers', 'Ask for packed dimensions for padded outerwear and hoodies. A light garment can still take up substantial parcel space.'),
    ('Folding and compression', 'Discuss whether compression or tight folding could affect structured pieces, prints, or trims before approving packing.'),
    ('Keep sets together', 'Confirm that all pieces and selected variants are included. Ask for dry protective wrapping and a final combined parcel weight.')]
CATEGORIES['accessories']['checks'] = [
    ('Closures and hardware', 'Request close views of zippers, clasps, buckles, hinges, and attachment points. Ask what opening and closing checks are available.'),
    ('Dimensions and adjustment', 'Check strap length, belt fastening range, watch sizing, or frame measurements against the exact selected variant.'),
    ('Surfaces and alignment', 'Inspect lenses, watch faces, seams, and decorative placement for visible marks or uneven finishing. Appearance does not establish material quality or authenticity.')]
CATEGORIES['accessories']['shipping'] = [
    ('Rigid shapes', 'Discuss support for structured bags and headwear so surrounding items do not crush their shape.'),
    ('Fragile surfaces', 'Ask for separation and padding around lenses, watch faces, and exposed hardware to reduce rubbing in transit.'),
    ('Small parts and batteries', 'Keep removable straps and jewelry pieces together in labeled packaging. For powered watches, provide battery details when requesting shipment acceptance.')]
CATEGORIES['beauty-fragrance']['checks'] = [
    ('Exact product label', 'Compare the selected name, volume, concentration, and variant with clear label photographs and supplied product information.'),
    ('Seals and condition', 'Inspect caps, seals, bottle edges, and outer packaging for visible damage or leakage. Do not open a seal simply to obtain a photo.'),
    ('Traceable information', 'Retain readable ingredient, batch, and date markings where supplied. Packaging photos cannot verify the contents, authenticity, or suitability for use.')]
CATEGORIES['beauty-fragrance']['shipping'] = [
    ('Confirm acceptance first', 'Describe the exact item, destination, volume, and whether it is a liquid or spray to your chosen service before ordering.'),
    ('Containment and glass', 'Ask what leak containment, cap protection, and cushioning can be provided. Include those materials in the packed quote.'),
    ('Separate incompatible items', 'Ask the service whether the product can share a parcel with the rest of your shortlist. A previously shipped bottle does not confirm acceptance for this item.')]
CATEGORIES['electronics']['checks'] = [
    ('Model and connections', 'Match exact model labels, ports, and supported functions with the intended device. Similar connectors do not establish compatibility.'),
    ('Power and included parts', 'Check input ratings, plug type, and the listed cable or charger contents. Ask for clear label and accessory photos.'),
    ('Visible condition and function', 'Inspect housings, screens, and connectors for damage. Ask which power-on or functional checks are available and what they cover; photos alone do not prove operation.')]
CATEGORIES['electronics']['shipping'] = [
    ('Battery details', 'Tell the service whether a battery is installed, separate, or absent and supply the available specifications before requesting a route.'),
    ('Protect devices and ports', 'Ask for padding around screens and housings, protection for connectors, and packing that prevents accidental activation.'),
    ('Destination and complete parcel', 'Confirm acceptance for the exact device and destination, including spare batteries or accessories. Request the quote after protective packing is accounted for.')]
