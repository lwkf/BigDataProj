import sys
import json

def clean_user_value(value):
    # Python 2/3 compatible string type checking
    try:
        is_string = isinstance(value, unicode) or isinstance(value, str)
    except NameError:
        is_string = isinstance(value, str)
    
    if is_string:
        # Remove Python 2 unicode markers
        if value.startswith("u'") and value.endswith("'"):
            return value[2:-1]
        # Convert string lists to actual lists
        if value.startswith("[") and value.endswith("]"):
            try:
                # Handle both Python 2 and 3 string representations
                cleaned = value.replace("u'", "'").replace("'", "\"")
                return json.loads(cleaned)
            except:
                return value
    return value

for line in sys.stdin:
    try:
        user_id, user_json = line.strip().split('\t', 1)
        user_data = json.loads(user_json)
        
        # Clean friends list
        if 'friends' in user_data:
            if isinstance(user_data['friends'], list):
                # Already a list, just ensure clean strings
                user_data['friends'] = [clean_user_value(f) for f in user_data['friends']]
            else:
                # Handle string representation
                user_data['friends'] = clean_user_value(user_data['friends'])
        
        # Clean elite years
        if 'elite_years' in user_data:
            if isinstance(user_data['elite_years'], list):
                # Ensure all years are integers
                user_data['elite_years'] = [int(y) if str(y).isdigit() else y 
                                          for y in user_data['elite_years']]
            else:
                user_data['elite_years'] = clean_user_value(user_data['elite_years'])
        
        print(json.dumps(user_data))
    except Exception as e:
        sys.stderr.write("ERROR: {}\n".format(str(e)))