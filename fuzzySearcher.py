from collections import defaultdict, Counter
from typing import List, Dict, Iterable

class FuzzySearcher:
    """
    External Doc
    ------------
    A class that performs fuzzy searching on a list of words based on letter occurrences.

    Attributes:
    -----------
    highestLetterInWordCount: defaultdict
        Stores the highest count of each letter among the given words.
    allWords: defaultdict
        Maps words by letter and count in the format 'letter-count'. E.g., 'a-2' maps to words with 'a' twice.
    settings: dict
        Stores settings like 'tolerance' for fuzzy searching.

    Purpose:
    --------
    FuzzySearcher allows fast and flexible matching of words by analyzing letter frequencies.
    Useful for searches that account for slight variations or typos.

    """

    def __init__(self, words: List[str]):
        """
        External Doc
        ------------
        Initializes the FuzzySearcher with a list of words. Each word is categorized by letter frequencies.

        Purpose:
        --------
        Efficient searching by pre-processing words and mapping them by frequency, reducing the need for calculations during searches.
        """

        """
        Internal Doc
        ------------
        The constructor processes the list of words by counting letter frequencies and creating a lookup table.
        Words are stored in `allWords`, and the highest count for each letter is tracked in `highestLetterInWordCount`.
        """
        self.highestLetterInWordCount = defaultdict(int)
        self.allWords: defaultdict[list[str]] = defaultdict(list)
        self.settings = {
            'tolerance': 5,  # Default tolerance for fuzzy searching
        }

        for word in words:
            for k, v in Counter(word).items():
                self.allWords[f"{k}-{v}"].append(word)
                if v > self.highestLetterInWordCount[k]:
                    self.highestLetterInWordCount[k] = v

    def getAllSearchCandidates(self, searchLetters: str) -> Iterable[str]:
        """
        External Doc
        ------------
        Retrieves all candidate words that match the search letters based on frequency.

        Parameters:
        -----------
        searchLetters: str
            The search string to match based on letter frequencies.
        
        Returns:
        --------
        Iterable[str]
            A list of candidate words matching the letter frequencies.

        Purpose:
        --------
        Efficiently narrows down possible matches before applying more detailed filtering.
        """

        """
        Internal Doc
        ------------
        Converts `searchLetters` to a letter frequency count using `Counter`.
        The method iterates over the search letter frequencies and retrieves words from `allWords` that meet or exceed the letter count.
        Returns a list of words that match the frequency requirements.
        """
        candidates = defaultdict(int)
        searchLetterCounter = Counter(searchLetters)

        for key, value in searchLetterCounter.items():
            for amount in range(value, self.highestLetterInWordCount[key] + 1):
                letterToWordKey = f"{key}-{amount}"
                if letterToWordKey in self.allWords:
                    for word in self.allWords[letterToWordKey]:
                        candidates[word] += 1
        return [word for word in candidates if candidates[word] == len(searchLetterCounter)]

    @staticmethod    
    def filter(candidates: Iterable[str], searchLetters: str) -> List[str]:
        """
        External Doc
        ------------
        Filters candidates by matching the exact sequence of letters.

        Parameters:
        -----------
        candidates: Iterable[str]
            The list of candidate words.
        searchLetters: str
            The sequence of letters to match exactly.

        Returns:
        --------
        List[str]
            Words matching the letter sequence.

        When to use:
        ------------
        Use for exact matching when the order of letters is important.
        """

        """
        Internal Doc
        ------------
        Iterates over candidate words to match the sequence of `searchLetters` letter by letter.
        A match is considered valid when the letters in `searchLetters` appear in order within the word.
        """
        passingCandidates = []
        for candidate in candidates:
            uptoInSearchLetters = 0
            for letter in candidate:
                if letter == searchLetters[uptoInSearchLetters]:
                    uptoInSearchLetters += 1
                    if uptoInSearchLetters == len(searchLetters):
                        passingCandidates.append(candidate)
                        break
        return passingCandidates

    @staticmethod    
    def lessFuzzyFilter(candidates: Iterable[str], searchLetters: str, tolerance: int) -> List[str]:
        """
        External Doc
        ------------
        Filters candidates allowing some tolerance for letter mismatches.

        Parameters:
        -----------
        candidates: Iterable[str]
            The list of candidate words.
        searchLetters: str
            The sequence of letters to match.
        tolerance: int
            Number of allowed mismatches.

        Returns:
        --------
        List[str]
            Words that match with a tolerance for mismatches.

        When to use:
        ------------
        Use when some deviations in letter order or positioning are acceptable.
        """

        """
        Internal Doc
        ------------
        Iterates over the candidates and checks for matches with the search letters while tracking mismatches.
        If mismatches exceed the tolerance, the word is skipped. Otherwise, words with the smallest mismatch are returned.
        """
        passingCandidates: Dict[int, List[str]] = defaultdict(list)
        for candidate in candidates:
            distanceWithNoMatch: int = 0
            uptoInSearchLetters = 0
            greatestDistanceWithNoMatch = 0
            for letter in candidate:
                if letter == searchLetters[uptoInSearchLetters]:
                    distanceWithNoMatch = 0
                    uptoInSearchLetters += 1
                    if uptoInSearchLetters == len(searchLetters):
                        passingCandidates[greatestDistanceWithNoMatch].append(candidate)
                        break
                else:
                    distanceWithNoMatch += 1
                    greatestDistanceWithNoMatch = max(greatestDistanceWithNoMatch, distanceWithNoMatch)
                    if distanceWithNoMatch > tolerance:
                        break
        
        results = []
        for key in sorted(passingCandidates.keys()):
            results.extend(passingCandidates[key])
        return results

    def search(self, searchLetters: str) -> List[str]:
        """
        External Doc
        ------------
        Performs a full search by letter frequency, and then refines it based on tolerance or exact matching.

        Parameters:
        -----------
        searchLetters: str
            The search string to match.
        
        Returns:
        --------
        List[str]
            Words that match the search string.

        Purpose:
        --------
        Wraps around other methods to provide a complete search, applying either exact or fuzzy matching based on settings.
        """

        """
        Internal Doc
        ------------
        This method first retrieves candidates using `getAllSearchCandidates`, and then applies either the `filter` or 
        `lessFuzzyFilter` based on the tolerance setting.
        """
        candidates = self.getAllSearchCandidates(searchLetters)
        if not "tolerance" in self.settings:
            return self.filter(candidates, searchLetters)
        return self.lessFuzzyFilter(candidates, searchLetters, self.settings["tolerance"])
