import sys
import json
from datetime import datetime

def clean_friends(friends):
    if friends is None:
        return []
    if isinstance(friends, str):
        return [f.strip() for f in friends.split(',') if f.strip()]
    return friends

def clean_elite(elite):
    if elite is None:
        return []
    if isinstance(elite, str):
        return [int(y.strip()) for y in elite.split(',') if y.strip().isdigit()]
    return elite

def calculate_account_age(yelping_since):
    try:
        join_date = datetime.strptime(yelping_since, '%Y-%m-%d')
        delta = datetime.now() - join_date
        return delta.days // 365 
    except:
        return 0

for line in sys.stdin:
    try:
        user = json.loads(line)
        cleaned = {
            'user_id': user['user_id'],
            'name': user.get('name', '').strip(),
            'yelping_since': user.get('yelping_since', '1970-01-01'),
            'account_age_years': calculate_account_age(user.get('yelping_since', '1970-01-01')),
            'review_count': int(user.get('review_count', 0)),
            'friends': clean_friends(user.get('friends')),
            'friends_count': len(clean_friends(user.get('friends'))),
            'useful': int(user.get('useful', 0)),
            'funny': int(user.get('funny', 0)),
            'cool': int(user.get('cool', 0)),
            'fans': int(user.get('fans', 0)),
            'elite_years': clean_elite(user.get('elite')),
            'average_stars': float(user.get('average_stars', 0)),
            'compliments': {
                k.replace('compliment_', ''): int(v) 
                for k, v in user.items() 
                if k.startswith('compliment_') and str(v).isdigit()
            }
        }
        print("{}\t{}".format(cleaned['user_id'], json.dumps(cleaned)))
    except Exception as e:
        sys.stderr.write("ERROR: {}\n".format(str(e)))