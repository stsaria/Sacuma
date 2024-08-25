import math
from collections import Counter

with open("TOKEN", encoding="utf-8") as f:
    TOKEN = f.read()
URL_PATTERN = r"\b(?:https?:\/\/)?(?:www\.)?[^\s]+\b"
MEMTION_PATTERN = r"<@!?(\d+)>|<@&(\d+)>"
ENTROPY_THRESHOLD = 2.0

HELP_MESSAGE = """## Commands
```
/help: Show this message
```"""

def calcEntropy(s):
    length = len(s)
    if length == 0:
        return 0
    
    freq = Counter(s)
    probabilities = [freq[char] / length for char in freq]
    entropy = -sum(p * math.log2(p) for p in probabilities)
    return entropy