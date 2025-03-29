import sys
import json
from datetime import datetime

def clean_text(text):
    if text is None:
        return ""
    return text.strip()

def clean_date(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').strftime('%Y-%m-%d')
    except:
        return '1970-01-01'

for line in sys.stdin:
    try:
        review = json.loads(line)
        cleaned = {
            'review_id': review['review_id'],
            'user_id': review['user_id'],
            'business_id': review['business_id'],
            'stars': int(review.get('stars', 0)),
            'date': clean_date(review.get('date')),
            'text': clean_text(review.get('text')),
            'text_length': len(clean_text(review.get('text'))),
            'useful': int(review.get('useful', 0)),
            'funny': int(review.get('funny', 0)),
            'cool': int(review.get('cool', 0))
        }
        print("{}\t{}".format(cleaned['review_id'], json.dumps(cleaned)))
    except Exception as e:
        sys.stderr.write("ERROR: {}\n".format(str(e)))