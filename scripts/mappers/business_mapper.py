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

def clean_hours(hours):
    if hours is None:
        return {}
    if isinstance(hours, str):
        try:
            return json.loads(hours.replace("'", "\""))
        except:
            return {}
    return hours

for line in sys.stdin:
    try:
        biz = json.loads(line)
        cleaned = {
            'business_id': biz.get('business_id', '').strip(),
            'name': biz.get('name', '').strip(),
            'address': biz.get('address', '').strip(),
            'city': biz.get('city', '').strip(),
            'state': biz.get('state', '').strip(),
            'postal_code': biz.get('postal_code', '').strip(),
            'latitude': float(biz.get('latitude', 0.0)),
            'longitude': float(biz.get('longitude', 0.0)),
            'stars': float(biz.get('stars', 0.0)),
            'review_count': int(biz.get('review_count', 0)),
            'is_open': int(biz.get('is_open', 0)),
            'attributes': clean_attributes(biz.get('attributes')),
            'categories': clean_categories(biz.get('categories')),
            'hours': clean_hours(biz.get('hours'))
        }
        print("{}\t{}".format(cleaned['business_id'], json.dumps(cleaned)))

    except Exception as e:
        sys.stderr.write("ERROR: {}\n".format(str(e)))