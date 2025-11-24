import json
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

previous_day = date.today() - timedelta(days=1)
previous_day_clean = str(previous_day).replace("-", "")


json_files = [p.name for p in Path("./tweets").glob(f"{previous_day_clean}*.json")]
print(json_files)


def yield_all_full_texts(data):
    def search(obj):
        if isinstance(obj, dict):
            if "full_text" in obj and obj["full_text"]:
                yield obj["full_text"]
            # elif "text" in obj and "full_text" not in obj:
            #    yield obj["text"]
            for v in obj.values():
                yield from search(v)
        elif isinstance(obj, list):
            for item in obj:
                yield from search(item)

    yield from search(data)


all_tweets = defaultdict(list)

for filepath in Path("./tweets").glob(f"{previous_day_clean}*.json"):
    username = filepath.stem  # removes .json → "user1", "user2", etc.

    with open(filepath, encoding="utf-8") as f:
        data = json.load(f)

    for text in yield_all_full_texts(data):
        if text.strip():  # skip empty tweets
            all_tweets[username].append(text.strip())

output_file = Path(f"{previous_day_clean}_all_users_tweets.json")
with open(f"filtering_tweets/{output_file}", "w", encoding="utf-8") as f:
    json.dump(all_tweets, f, ensure_ascii=False, indent=2)

print(
    f"Saved {sum(len(t) for t in all_tweets.values())} tweets from {len(all_tweets)} users → {output_file}"
)
