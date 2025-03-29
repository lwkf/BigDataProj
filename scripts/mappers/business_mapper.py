import sys
import json

def clean_categories(categories):
    if categories is None:
        return []
    if isinstance(categories, str):
        return [c.strip() for c in categories.split(',') if c.strip()]
    return categories

def clean_attributes(attributes):
    if attributes is None:
        return {}
    if isinstance(attributes, str):
        try:
            return json.loads(attributes.replace("'", "\""))
        except:
            return {}
    return attributes

for line in sys.stdin:
    try:
        biz = json.loads(line)
        cleaned = {
            'business_id': biz['business_id'],
            'name': biz.get('name', '').strip(),
            'city': biz.get('city', '').strip(),
            'state': biz.get('state', '').strip(),
            'stars': float(biz.get('stars', 0)),
            'categories': clean_categories(biz.get('categories')),
            'attributes': clean_attributes(biz.get('attributes'))
        }
        print("{}\t{}".format(cleaned['business_id'], json.dumps(cleaned)))
    except Exception as e:
        sys.stderr.write("ERROR: {}\n".format(str(e)))