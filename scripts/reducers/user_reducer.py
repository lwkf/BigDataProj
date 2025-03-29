import sys
import json

current_user = None

for line in sys.stdin:
    try:
        user_id, user_json = line.strip().split('\t', 1)
        # Just pass through the data (modify this with your actual reducer logic)
        print("{}\t{}".format(user_id, user_json))
    except Exception as e:
        sys.stderr.write("ERROR: {}\n".format(str(e)))