from fuzzySearcher import FuzzySearcher
from sampleData import words  # Assuming `words` is defined in `data`

fuzzy_searcher = FuzzySearcher(words)
result = fuzzy_searcher.search("theme")
print(result)