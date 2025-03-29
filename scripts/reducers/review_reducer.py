import sys
import json

current_review = None

for line in sys.stdin:
    try:
        review_id, review_json = line.strip().split('\t', 1)
        # Just pass through the data (modify this with your actual reducer logic)
        print("{}\t{}".format(review_id, review_json))
    except Exception as e:
        sys.stderr.write("ERROR: {}\n".format(str(e)))