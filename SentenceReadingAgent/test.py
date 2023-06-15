import re

# Your sentence
sentence = "David and Lucy walk one mile to go to school every day at 8:00AM when there is no snow."

# The regular expression
time_regex = r"\b\d{1,2}:\d{2}(AM|PM)?\b"

# Search for the time in the sentence
time_match = re.search(time_regex, sentence)

if time_match:
    # If the time was found, print it
    print(f"Found time: {time_match.group()}")
else:
    # If the time wasn't found, print a failure message
    print("Time not found")