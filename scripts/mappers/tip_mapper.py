import sys
import json
from datetime import datetime

def clean_tip_text(text):
    if text is None:
        return ""
    return text.strip()

def clean_tip_date(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').strftime('%Y-%m-%d')
    except:
        return '1970-01-01'

for line in sys.stdin:
    try:
        tip = json.loads(line)
        cleaned = {
            'user_id': tip['user_id'],
            'business_id': tip['business_id'],
            'date': clean_tip_date(tip.get('date')),
            'text': clean_tip_text(tip.get('text')),
            'text_length': len(clean_tip_text(tip.get('text'))),
            'compliment_count': int(tip.get('compliment_count', 0))
        }
        print("{}\t{}".format(tip['business_id'], json.dumps(cleaned)))
    except Exception as e:
        sys.stderr.write("ERROR: {}\n".format(str(e)))