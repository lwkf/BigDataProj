import sys
import json

current_business = None

for line in sys.stdin:
    try:
        business_id, biz_json = line.strip().split('\t', 1)
        # Just pass through the data (modify this with your actual reducer logic)
        print("{}\t{}".format(business_id, biz_json))
    except Exception as e:
        sys.stderr.write("ERROR: {}\n".format(str(e)))