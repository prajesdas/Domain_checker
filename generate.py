import csv, itertools, string, re


def is_pronounceable(word: str) -> bool:
    vowels = "aeiouy"
    # Must have at least one vowel
    if not any(c in vowels for c in word):
        return False
    # No 3+ consonants in a row
    if re.search(r"[bcdfghjklmnpqrstvwxyz]{3,}", word):
        return False
    # No 3+ vowels in a row
    if re.search(r"[aeiouy]{3,}", word):
        return False
    # Disallow impossible doubles
    if re.search(r"(q|w|x|z|j|v|a|i|u)\1", word):
        return False
    return True


with open("domains.csv", "w", newline="") as f:
    writer = csv.writer(f)
    for combo in itertools.product(string.ascii_lowercase, repeat=5):
        word = ''.join(combo)
        if is_pronounceable(word):
            writer.writerow([word + ".com", "unknown"])
