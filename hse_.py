from lxml import html
import json
import pprint
 
pp = pprint.PrettyPrinter(indent=4)
 
metadata = {
    'address': ['Адрес',
                'адрес',
                'ул.'],
    'tel': ['(495)',
            '-495-'],
    'email': ['E-mail',
              'e-mail',
              'email'],
    'head': ['Руководитель',
             'руководитель'],
    'subhead': ['Заместитель',
                'заместитель']
    }
 
 
def get_content_or_None(tree, text):
    
    items = tree.xpath('.//*[starts-with(text(),"{}")]'.format(text))
    return items[0].text_content() if items else None
 
 
def get_page_data(href):
    
    if not href.startswith('http://'):
        return None
 
    try:
        webpage = html.parse(href)
    except:
        return None
 
    page_dict = {'href': href}
    for key in metadata.keys():
        parsed_data = next((get_content_or_None(webpage, item) for item in
            metadata[key] if get_content_or_None(webpage, item)), None)
 
        if parsed_data:
            page_dict[key] = parsed_data
 
    
    pp.pprint(page_dict)
 
    return page_dict
 
 
def main():
    root_page = html.parse('http://www.hse.ru/education/faculty/')
 
    
    content = root_page.getroot().find_class("posts_general").pop()
 
    
    hse = {}
 
    for d in content.xpath('.//p[@class="text"]//a[@class="link" and @href]'):
        department = d.text_content()
        hse[department] = {}
        hse[department]['href'] = d.attrib['href']
 
        
        page_dict = get_page_data(d.attrib['href'])
        hse[department] = page_dict
 
        if not hse[department]:
            continue
        
        if getattr(d.xpath('../..')[0].getnext(), 'tag', None) == 'ul':
            list_root = d.xpath('../..')[0].getnext()
            hse[department]['units'] = {item.text_content():
                get_page_data(item.attrib['href'])
                for item in list_root.xpath('.//a')}
 
    print(hse)
    with open('hse.json', 'w') as f:
        json.dump(hse, f)
 
if __name__ == "__main__":
    main()
