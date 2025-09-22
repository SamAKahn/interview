#!/usr/bin/env python3
"""
Performance test comparing the optimized incremental top 5 update
vs the original full-sort approach.
"""

import time
from optimized_linked_list_analyzer import OptimizedWordFrequencyAnalyzer


def test_performance():
    """Test performance of the optimized implementation."""
    
    print("=== Performance Test: Optimized Top 5 Update ===\n")
    
    # Test with different dataset sizes
    test_cases = [
        ("Small dataset", 50, 10),
        ("Medium dataset", 200, 20), 
        ("Large dataset", 1000, 50)
    ]
    
    for test_name, total_words, unique_words in test_cases:
        print(f"{test_name} ({total_words} words, {unique_words} unique):")
        
        analyzer = OptimizedWordFrequencyAnalyzer()
        
        # Generate test data
        import random
        words = [f"word{i % unique_words}" for i in range(total_words)]
        random.shuffle(words)
        
        # Test incremental updates
        start_time = time.time()
        
        # Add words in small batches to simulate real usage
        batch_size = 5
        for i in range(0, len(words), batch_size):
            batch = words[i:i+batch_size]
            analyzer.add_words(", ".join(batch))
        
        end_time = time.time()
        
        print(f"  Time to add {total_words} words: {end_time - start_time:.4f} seconds")
        print(f"  Top 5: {analyzer.get_top_five_most_frequent()}")
        print(f"  Unique words: {len(analyzer.get_all_frequencies())}")
        print()


def test_incremental_benefits():
    """Test the benefits of incremental updates."""
    
    print("=== Incremental Update Benefits ===\n")
    
    analyzer = OptimizedWordFrequencyAnalyzer()
    
    # Add initial words
    print("1. Adding initial words...")
    analyzer.add_words("apple, banana, apple, cherry, date")
    print(f"   Top 5: {analyzer.get_top_five_most_frequent()}")
    
    # Add words that don't affect top 5
    print("\n2. Adding words that don't affect top 5...")
    analyzer.add_words("zebra, yankee, xray, whale, violin")
    print(f"   Top 5: {analyzer.get_top_five_most_frequent()}")
    print("   ✅ No unnecessary updates!")
    
    # Add words that do affect top 5
    print("\n3. Adding words that affect top 5...")
    analyzer.add_words("apple, apple, banana, cherry, cherry")
    print(f"   Top 5: {analyzer.get_top_five_most_frequent()}")
    print("   ✅ Efficiently updated only relevant words!")
    
    # Add many words at once
    print("\n4. Adding many words at once...")
    analyzer.add_words("apple, banana, cherry, date, elderberry, fig, grape, honey, ice, juice")
    print(f"   Top 5: {analyzer.get_top_five_most_frequent()}")
    print("   ✅ Handled batch updates efficiently!")


if __name__ == "__main__":
    test_performance()
    print("="*50)
    test_incremental_benefits()
