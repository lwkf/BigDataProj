import sys
import json
from datetime import datetime

def clean_checkin_dates(date_str):
    if date_str is None:
        return []
    return [d.strip() for d in date_str.split(',') if d.strip()]

def analyze_time_patterns(dates):
    time_stats = {'total': len(dates)}
    for date_str in dates:
        try:
            dt = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            hour = dt.hour
            weekday = dt.strftime('%A')

            time_stats.setdefault('hours', {}).setdefault(str(hour), 0)
            time_stats['hours'][str(hour)] += 1

            time_stats.setdefault('weekdays', {}).setdefault(weekday, 0)
            time_stats['weekdays'][weekday] += 1
        except:
            continue
    return time_stats

for line in sys.stdin:
    try:
        checkin = json.loads(line)
        dates = clean_checkin_dates(checkin.get('date'))

        cleaned = {
            'business_id': checkin['business_id'],
            'checkin_count': len(dates),
            'time_patterns': analyze_time_patterns(dates),
            'date': ",".join(dates)   
        }

        print("{}\t{}".format(cleaned['business_id'], json.dumps(cleaned)))
    except Exception as e:
        sys.stderr.write("ERROR: {}\n".format(str(e)))