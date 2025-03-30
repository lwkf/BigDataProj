import sys
import json
from collections import defaultdict

def clean_checkin_value(value):
    """Handle both Python 2 and 3 string types"""
    try:
        is_string = isinstance(value, unicode) or isinstance(value, str)
    except NameError:
        is_string = isinstance(value, str)
    
    if is_string:
        if value.startswith("u'") and value.endswith("'"):
            return value[2:-1]
        if value.startswith("{") and value.endswith("}"):
            try:
                return json.loads(value.replace("'", "\""))
            except:
                return value
    return value

current_business = None
combined_stats = {
    'total': 0,
    'hours': defaultdict(int),
    'weekdays': defaultdict(int)
}

def merge_time_patterns(existing, new):
    """Merge new checkin stats into existing aggregated stats"""
    if not new:
        return existing
    
    existing['total'] += new.get('checkin_count', 0)
    
    # Merge hour patterns
    time_patterns = new.get('time_patterns', {})
    if isinstance(time_patterns, dict):
        for hour, count in time_patterns.get('hours', {}).items():
            existing['hours'][str(hour)] += int(count)
        
        # Merge weekday patterns
        for day, count in time_patterns.get('weekdays', {}).items():
            existing['weekdays'][str(day)] += int(count)
    
    return existing

for line in sys.stdin:
    try:
        line = line.strip()
        if not line:
            continue
            
        # Handle tab-separated input
        if '\t' in line:
            business_id, stats_json = line.split('\t', 1)
        else:
            # If no tab, assume entire line is JSON
            stats_json = line
            stats = json.loads(stats_json)
            business_id = stats.get('business_id', '')
        
        stats = json.loads(stats_json)
        
        # Clean and parse the input
        if 'time_patterns' in stats:
            if isinstance(stats['time_patterns'], str):
                stats['time_patterns'] = clean_checkin_value(stats['time_patterns'])
                try:
                    stats['time_patterns'] = json.loads(stats['time_patterns'])
                except:
                    stats['time_patterns'] = {}
        
        if current_business == business_id:
            combined_stats = merge_time_patterns(combined_stats, stats)
        else:
            if current_business:
                # Output the previous business's stats
                output = {
                    'business_id': current_business,
                    'checkin_count': combined_stats['total'],
                    'time_patterns': {
                        'hours': dict(combined_stats['hours']),
                        'weekdays': dict(combined_stats['weekdays'])
                    }
                }
                print(json.dumps(output))
            
            current_business = business_id
            combined_stats = {
                'total': 0,
                'hours': defaultdict(int),
                'weekdays': defaultdict(int)
            }
            combined_stats = merge_time_patterns(combined_stats, stats)
            
    except Exception as e:
        sys.stderr.write("ERROR processing line: {} - {}\n".format(line, str(e)))

# Output the last business
if current_business:
    output = {
        'business_id': current_business,
        'checkin_count': combined_stats['total'],
        'time_patterns': {
            'hours': dict(combined_stats['hours']),
            'weekdays': dict(combined_stats['weekdays'])
        }
    }
    print(json.dumps(output))