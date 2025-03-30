import sys
import json

def clean_review_value(value):
    if isinstance(value, str) or isinstance(value, unicode):
        if value.startswith("u'") and value.endswith("'"):
            return value[2:-1]
        if value.startswith("{") and value.endswith("}"):
            try:
                return json.loads(value.replace("'", "\""))
            except:
                return value
    return value

for line in sys.stdin:
    try:
        review_id, review_json = line.strip().split('\t', 1)
        review_data = json.loads(review_json)
        
        # Clean text fields
        if 'text' in review_data:
            review_data['text'] = clean_review_value(review_data['text'])
        
        print(json.dumps(review_data))
    except Exception as e:
        sys.stderr.write("ERROR: {}\n".format(str(e)))