import unittest
from fuzzySearcher import FuzzySearcher
from sampleData import words  # Assuming `words` is defined in `data`

class TestFuzzySearcher(unittest.TestCase):
    
    def setUp(self):
        self.fuzzy_searcher = FuzzySearcher(words)

    def test_get_all_search_candidates(self):
        candidates = self.fuzzy_searcher.getAllSearchCandidates("there")
        self.assertIn("thermopile", candidates)

    def test_filter(self):
        candidates = ["there", "three", "theme"]
        result = FuzzySearcher.filter(candidates, "thr")
        self.assertIn("there", result)
        self.assertIn("three", result)

    def test_less_fuzzy_filter(self):
        candidates = ["three", "there", "theme", "her"]
        result = FuzzySearcher.lessFuzzyFilter(candidates, "thr", 0)
        self.assertEqual(result, ["three"])

    def test_search(self):
        result = self.fuzzy_searcher.search("theme")
        self.assertNotIn("three", result)

if __name__ == '__main__':
    unittest.main()
