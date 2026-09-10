"""One authored step list supplies visible content and HowTo markup."""
from finds_data import ROOT
from find_card import e

STEPS = [
    ('Find or paste a product link', 'Paste the original marketplace link into Joyagoo or search for the product.'),
    ('Choose size, color, and quantity', 'Select the exact options and check the order before proceeding.'),
    ('Pay product cost and domestic shipping', 'Review and pay the item cost and Chinese domestic delivery charge in Joyagoo.'),
    ('Wait for seller delivery to warehouse', 'Follow the order status while the seller sends the item to the external warehouse.'),
    ('Review QC photos', 'Inspect the supplied photos promptly and raise any unresolved questions with the service.'),
    ('Build parcel', 'Select stored items, confirm the address, and review packing choices.'),
    ('Choose international shipping route', 'Compare the available routes for your contents and destination.'),
    ('Pay international shipping', 'Review the parcel charge and complete payment through the external service.'),
    ('Track delivery', 'Follow the parcel tracking and contact the relevant provider about delivery questions.'),
]


def buying_output(shell):
    route = '/en/joyagoo-buying-guide/'
    main = (ROOT / 'components/buying-guide.html').read_text(encoding='utf-8-sig')
    main = main.replace('{{steps}}', ''.join(f'<li id="buying-step-{i}"><h3>{e(title)}</h3><p>{e(copy)}</p></li>' for i,(title,copy) in enumerate(STEPS,1)))
    main = main.replace('<li id="buying-step-9"><h3>', '<li id="buying-step-9"><h3 id="track-delivery">')
    howto = {'@context':'https://schema.org', '@type':'HowTo', 'name':'How to Buy From Taobao, Weidian, and 1688 With Joyagoo',
             'description':'Prepare on JoyaVault and complete the buying and shipping process with external providers.',
             'step':[{'@type':'HowToStep','position':i,'name':title,'text':copy,'url':'https://joyavault.com'+route+f'#buying-step-{i}'} for i,(title,copy) in enumerate(STEPS,1)]}
    return {ROOT / route.strip('/') / 'index.html': shell('How to Buy With Joyagoo | Taobao, Weidian & 1688 Guide',
        'Learn how to prepare product links, compare finds, review QC, plan shipping, and continue into the Joyagoo buying flow.',
        route, main, indexable=True, structured_data=howto)}
