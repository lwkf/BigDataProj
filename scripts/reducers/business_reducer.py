# business_reducer.py (Python 2.7+ compatible)
import sys
import json

def clean_value(value):
    if isinstance(value, str) or isinstance(value, unicode):
        # Remove Python-specific string markers (u')
        if value.startswith("u'") and value.endswith("'"):
            return value[2:-1]
        # Convert string-dicts to actual dicts
        if value.startswith("{") and value.endswith("}"):
            try:
                return json.loads(value.replace("'", "\""))
            except:
                return value
    return value

for line in sys.stdin:
    try:
        business_id, biz_json = line.strip().split('\t', 1)
        biz_data = json.loads(biz_json)

        # Clean nested dictionaries
        if 'attributes' in biz_data and isinstance(biz_data['attributes'], dict):
            biz_data['attributes'] = {k: clean_value(v) for k, v in biz_data['attributes'].items()}

        if 'hours' in biz_data and isinstance(biz_data['hours'], dict):
            biz_data['hours'] = {k: clean_value(v) for k, v in biz_data['hours'].items()}

        # Final cleaned JSON
        print(json.dumps(biz_data))
    except Exception as e:
        sys.stderr.write("ERROR: {}\n".format(str(e)))