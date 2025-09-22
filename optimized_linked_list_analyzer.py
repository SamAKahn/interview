#!/usr/bin/env python3
"""
Optimized Word Frequency Analyzer using two specialized linked lists:
1. Top 5 list - only stores the 5 most frequent words
2. Frequency count list - only stores frequency counts, not words
"""

from collections import Counter
from typing import List, Dict, Tuple, Optional
import sys


class TopFiveNode:
    """Node for top 5 most frequent words list."""
    
    def __init__(self, word: str, frequency: int):
        self.word = word
        self.frequency = frequency
        self.next: Optional['TopFiveNode'] = None
        self.prev: Optional['TopFiveNode'] = None


class FrequencyCountNode:
    """Node for frequency count list - only stores counts, not words."""
    
    def __init__(self, frequency: int, count: int):
        self.frequency = frequency
        self.count = count  # How many words have this frequency
        self.next: Optional['FrequencyCountNode'] = None
        self.prev: Optional['FrequencyCountNode'] = None


class OptimizedWordFrequencyAnalyzer:
    """
    Memory-efficient word frequency analyzer using two specialized linked lists.
    """
    
    def __init__(self):
        # Main dictionary - only stores unique words and their counts
        self.word_counts = Counter()
        
        # Top 5 list - only stores 5 most frequent words
        self.top_five_head: Optional[TopFiveNode] = None
        self.top_five_tail: Optional[TopFiveNode] = None
        
        # Frequency count list - only stores frequency counts
        self.freq_head: Optional[FrequencyCountNode] = None
        self.freq_tail: Optional[FrequencyCountNode] = None
        
        # Total word count for median calculation
        self.total_words = 0
    
    def add_words(self, words_string: str) -> None:
        """Add words and update both linked lists efficiently."""
        words = [word.strip().lower() for word in words_string.split(',') if word.strip()]
        
        if not words:
            return
        
        # Track changes to update linked lists
        changes = {}
        changed_words = set()
        
        # Add words to main dictionary
        for word in words:
            old_count = self.word_counts[word]
            self.word_counts[word] += 1
            new_count = self.word_counts[word]
            
            # Track frequency changes
            if old_count > 0:
                changes[old_count] = changes.get(old_count, 0) - 1
            changes[new_count] = changes.get(new_count, 0) + 1
            
            # Track which words changed frequency
            if old_count != new_count:
                changed_words.add(word)
            
            self.total_words += 1
        
        # Update frequency count list
        self._update_frequency_counts(changes)
        
        # Update top 5 list incrementally
        if changed_words:
            self._update_top_five_incremental(changed_words)
    
    def _update_frequency_counts(self, changes: Dict[int, int]) -> None:
        """Update the frequency count list based on changes."""
        for frequency, change in changes.items():
            if change == 0:
                continue
                
            # Find or create node for this frequency
            node = self._find_frequency_node(frequency)
            
            if node:
                # Update existing node
                node.count += change
                if node.count <= 0:
                    # Remove node if count becomes 0 or negative
                    self._remove_frequency_node(node)
            else:
                # Create new node for this frequency
                if change > 0:
                    self._insert_frequency_node(frequency, change)
    
    def _find_frequency_node(self, frequency: int) -> Optional[FrequencyCountNode]:
        """Find the node with the specified frequency."""
        current = self.freq_head
        while current:
            if current.frequency == frequency:
                return current
            current = current.next
        return None
    
    def _insert_frequency_node(self, frequency: int, count: int) -> None:
        """Insert a new frequency node in sorted order."""
        new_node = FrequencyCountNode(frequency, count)
        
        if not self.freq_head:
            # First node
            self.freq_head = new_node
            self.freq_tail = new_node
        else:
            # Insert in sorted order (highest frequency first)
            current = self.freq_head
            while current and current.frequency > frequency:
                current = current.next
            
            if not current:
                # Insert at tail
                self.freq_tail.next = new_node
                new_node.prev = self.freq_tail
                self.freq_tail = new_node
            else:
                # Insert before current
                new_node.next = current
                new_node.prev = current.prev
                if current.prev:
                    current.prev.next = new_node
                else:
                    self.freq_head = new_node
                current.prev = new_node
    
    def _remove_frequency_node(self, node: FrequencyCountNode) -> None:
        """Remove a frequency node."""
        if node.prev:
            node.prev.next = node.next
        else:
            self.freq_head = node.next
        
        if node.next:
            node.next.prev = node.prev
        else:
            self.freq_tail = node.prev
    
    def _update_top_five_incremental(self, changed_words: set) -> None:
        """Update top 5 list incrementally based on changed words."""
        # Get current top 5 as a list for easier manipulation
        current_top5 = self._get_current_top5_list()
        
        # If no current top 5, build from scratch
        if not current_top5:
            self._build_initial_top5()
            return
        
        # Check if any changed word should be in top 5
        for word in changed_words:
            freq = self.word_counts[word]
            
            # Check if this word should be in top 5
            if self._should_be_in_top5(word, freq, current_top5):
                self._insert_or_update_in_top5(word, freq, current_top5)
        
        # Rebuild linked list from updated list
        self._rebuild_top5_linked_list(current_top5)
    
    def _build_initial_top5(self) -> None:
        """Build initial top 5 list from scratch."""
        # Get all words with their frequencies
        all_words = list(self.word_counts.items())
        
        # Sort by frequency (descending) then by word (ascending) for consistency
        all_words.sort(key=lambda x: (-x[1], x[0]))
        
        # Take top 5
        top_five = all_words[:5]
        
        # Build linked list
        self._rebuild_top5_linked_list(top_five)
    
    def _get_current_top5_list(self) -> List[Tuple[str, int]]:
        """Get current top 5 as a list."""
        result = []
        current = self.top_five_head
        while current:
            result.append((current.word, current.frequency))
            current = current.next
        return result
    
    def _should_be_in_top5(self, word: str, freq: int, current_top5: list) -> bool:
        """Check if a word should be in the top 5."""
        # If we have less than 5 words, always include
        if len(current_top5) < 5:
            return True
        
        # If frequency is higher than the 5th word, include it
        if freq > current_top5[4][1]:
            return True
        
        # If frequency equals the 5th word, use alphabetical tie-breaker
        if freq == current_top5[4][1] and word < current_top5[4][0]:
            return True
        
        return False
    
    def _insert_or_update_in_top5(self, word: str, freq: int, current_top5: list) -> None:
        """Insert or update a word in the top 5 list."""
        # Remove existing entry if it exists
        current_top5[:] = [(w, f) for w, f in current_top5 if w != word]
        
        # Add new entry
        current_top5.append((word, freq))
        
        # Sort by frequency (desc) then alphabetically (asc)
        current_top5.sort(key=lambda x: (-x[1], x[0]))
        
        # Keep only top 5
        current_top5[:] = current_top5[:5]
    
    def _rebuild_top5_linked_list(self, top5_list: List[Tuple[str, int]]) -> None:
        """Rebuild the top 5 linked list from a list."""
        # Clear existing top 5 list
        self.top_five_head = None
        self.top_five_tail = None
        
        # Build new top 5 list
        for word, frequency in top5_list:
            new_node = TopFiveNode(word, frequency)
            
            if not self.top_five_head:
                self.top_five_head = new_node
                self.top_five_tail = new_node
            else:
                self.top_five_tail.next = new_node
                new_node.prev = self.top_five_tail
                self.top_five_tail = new_node
    
    def get_top_five_most_frequent(self) -> List[Tuple[str, int]]:
        """Get top 5 most frequent words."""
        result = []
        current = self.top_five_head
        while current:
            result.append((current.word, current.frequency))
            current = current.next
        return result
    
    def get_lowest_frequency(self) -> int:
        """Get the lowest frequency."""
        if not self.freq_tail:
            return 0
        return self.freq_tail.frequency
    
    def get_median_frequency(self) -> float:
        """Calculate median of the frequency values themselves."""
        if not self.word_counts:
            return 0.0
        
        # Get all unique frequency values
        frequency_values = list(self.word_counts.values())
        
        # Sort the frequency values
        frequency_values.sort()
        
        # Calculate median
        n = len(frequency_values)
        if n % 2 == 0:
            return (frequency_values[n//2 - 1] + frequency_values[n//2]) / 2
        else:
            return float(frequency_values[n//2])
    
    def get_all_frequencies(self) -> Dict[str, int]:
        """Get all word frequencies (for debugging)."""
        return dict(self.word_counts)
    
    def get_frequency_counts(self) -> List[Tuple[int, int]]:
        """Get frequency counts (for debugging)."""
        result = []
        current = self.freq_head
        while current:
            result.append((current.frequency, current.count))
            current = current.next
        return result
    
    def clear(self) -> None:
        """Clear all data."""
        self.word_counts.clear()
        self.top_five_head = None
        self.top_five_tail = None
        self.freq_head = None
        self.freq_tail = None
        self.total_words = 0


def memory_comparison():
    """Compare memory usage between approaches."""
    
    print("=== Memory Usage Comparison ===\n")
    
    # Test data
    test_inputs = [
        "apple, banana, apple, cherry",
        "banana, cherry, elderberry, fig",
        "apple, grape, apple, banana",
        "date, elderberry, fig, grape, honey",
        "ice, juice, kiwi, lemon, mango"
    ]
    
    # Optimized linked list approach
    optimized = OptimizedWordFrequencyAnalyzer()
    for words in test_inputs:
        optimized.add_words(words)
    
    print("Memory usage:")
    
    # Calculate optimized memory usage
    optimized_memory = sys.getsizeof(optimized.word_counts)
    
    # Top 5 list memory
    top5_memory = 0
    current = optimized.top_five_head
    while current:
        top5_memory += sys.getsizeof(current)
        current = current.next
    
    # Frequency count list memory
    freq_memory = 0
    current = optimized.freq_head
    while current:
        freq_memory += sys.getsizeof(current)
        current = current.next
    
    total_optimized = optimized_memory + top5_memory + freq_memory
    
    print(f"  Optimized: {total_optimized} bytes")
    print(f"    - Main dictionary: {optimized_memory} bytes")
    print(f"    - Top 5 list: {top5_memory} bytes")
    print(f"    - Frequency counts: {freq_memory} bytes")
    
    print(f"\nFrequency counts: {optimized.get_frequency_counts()}")
    print(f"Top 5: {optimized.get_top_five_most_frequent()}")
    print(f"Lowest frequency: {optimized.get_lowest_frequency()}")
    print(f"Median frequency: {optimized.get_median_frequency()}")


def interactive_demo():
    """Interactive demo of the optimized analyzer."""
    
    print("=== Optimized Linked List Word Frequency Analyzer ===\n")
    print("Enter comma-separated words to add to the dictionary.")
    print("Type 'statistics' to see the analysis results.")
    print("Type 'debug' to see internal state.")
    print("Type 'help' for more commands.")
    print("Type 'quit' to exit.\n")
    
    analyzer = OptimizedWordFrequencyAnalyzer()
    
    while True:
        try:
            user_input = input("> ").strip()
            
            if user_input.lower() == 'quit':
                print("Goodbye!")
                break
            elif user_input.lower() == 'help':
                print("\nAvailable commands:")
                print("  - Enter comma-separated words to add them to the dictionary")
                print("  - 'statistics' - Show word frequency analysis")
                print("  - 'debug' - Show internal linked list state")
                print("  - 'clear' - Clear all words from the dictionary")
                print("  - 'help' - Show this help message")
                print("  - 'quit' - Exit the program\n")
            elif user_input.lower() == 'clear':
                analyzer.clear()
                print("Dictionary cleared.\n")
            elif user_input.lower() == 'debug':
                print("\n=== Internal State ===")
                print(f"Total words: {analyzer.total_words}")
                print(f"Top 5 list: {analyzer.get_top_five_most_frequent()}")
                print(f"Frequency counts: {analyzer.get_frequency_counts()}")
                print(f"All frequencies: {analyzer.get_all_frequencies()}")
                print()
            elif user_input.lower() == 'statistics':
                if not analyzer.word_counts:
                    print("No words in dictionary. Add some words first.\n")
                else:
                    print("\n=== Word Frequency Statistics ===")
                    
                    # Show all word frequencies
                    print("All word frequencies:")
                    for word, count in sorted(analyzer.get_all_frequencies().items()):
                        print(f"  {word}: {count}")
                    
                    # Show top 5 most frequent words
                    print(f"\nTop 5 most frequent words:")
                    top_five = analyzer.get_top_five_most_frequent()
                    for i, (word, count) in enumerate(top_five, 1):
                        print(f"  {i}. {word}: {count}")
                    
                    # Show lowest frequency
                    print(f"\nLowest frequency: {analyzer.get_lowest_frequency()}")
                    
                    # Show median frequency
                    print(f"Median frequency: {analyzer.get_median_frequency()}")
                    print()
            elif user_input:
                # Add words to the dictionary
                analyzer.add_words(user_input)
                word_count = len([word for word in user_input.split(',') if word.strip()])
                print(f"Added {word_count} word(s) to dictionary.\n")
            else:
                print("Please enter some words or a command.\n")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    # Run interactive demo
    interactive_demo()
    
    print("\n" + "="*50)
    memory_comparison()
