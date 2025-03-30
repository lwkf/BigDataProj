import sys
import json

def clean_tip_value(value):
    if isinstance(value, str) or isinstance(value, unicode):
        if value.startswith("u'") and value.endswith("'"):
            return value[2:-1]
    return value

for line in sys.stdin:
    try:
        business_id, tip_json = line.strip().split('\t', 1)
        tip_data = json.loads(tip_json)
        
        # Clean text fields
        if 'text' in tip_data:
            tip_data['text'] = clean_tip_value(tip_data['text'])
        
        print(json.dumps(tip_data))
    except Exception as e:
        sys.stderr.write("ERROR: {}\n".format(str(e)))