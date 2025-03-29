import sys
import json
from collections import defaultdict

current_business = None
combined_stats = None

def merge_time_patterns(existing, new):
    if existing is None:
        return new
    if new is None:
        return existing
        
    # Merge checkin counts
    existing['checkin_count'] += new.get('checkin_count', 0)
    
    # Merge hour patterns
    for hour, count in new.get('time_patterns', {}).get('hours', {}).items():
        existing['time_patterns']['hours'][hour] = existing['time_patterns']['hours'].get(hour, 0) + count
        
    # Merge weekday patterns
    for day, count in new.get('time_patterns', {}).get('weekdays', {}).items():
        existing['time_patterns']['weekdays'][day] = existing['time_patterns']['weekdays'].get(day, 0) + count
        
    return existing

for line in sys.stdin:
    try:
        business_id, stats_json = line.strip().split('\t', 1)
        stats = json.loads(stats_json)
        
        if current_business == business_id:
            combined_stats = merge_time_patterns(combined_stats, stats)
        else:
            if current_business:
                print("{}\t{}".format(current_business, json.dumps(combined_stats)))
            current_business = business_id
            combined_stats = stats
            
    except Exception as e:
        sys.stderr.write("ERROR: {}\n".format(str(e)))
        continue

if current_business:
    print("{}\t{}".format(current_business, json.dumps(combined_stats)))