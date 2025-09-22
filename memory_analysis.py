#!/usr/bin/env python3
"""
Detailed memory analysis comparing original vs linked list approaches.
"""

import sys
from collections import Counter
from optimized_linked_list_analyzer import OptimizedWordFrequencyAnalyzer


def analyze_memory_growth():
    """Analyze how memory usage grows with more word additions."""
    
    print("=== Memory Growth Analysis ===\n")
    
    # Test with increasing number of word additions
    test_cases = [10, 50, 100, 200, 500]
    
    for num_additions in test_cases:
        print(f"Testing with {num_additions} word additions:")
        
    # Optimized approach
    optimized = OptimizedWordFrequencyAnalyzer()
    for i in range(num_additions):
        optimized.add_words(f"word{i}, word{i+1}, word{i+2}")
    
    # Calculate total memory for optimized approach
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
    print()


def analyze_memory_components():
    """Analyze what takes up memory in the optimized approach."""
    
    print("=== Memory Component Analysis ===\n")
    
    # Create test data
    optimized = OptimizedWordFrequencyAnalyzer()
    
    # Add some words
    test_words = ["apple, banana, cherry, date, elderberry, fig, grape, honey, ice, juice"] * 5
    for words in test_words:
        optimized.add_words(words)
    
    print("Optimized approach memory breakdown:")
    main_memory = sys.getsizeof(optimized.word_counts)
    print(f"  Main dictionary: {main_memory} bytes")
    
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
    
    total_memory = main_memory + top5_memory + freq_memory
    
    print(f"  Top 5 list: {top5_memory} bytes")
    print(f"  Frequency counts: {freq_memory} bytes")
    print(f"  Total: {total_memory} bytes")


def demonstrate_memory_growth():
    """Demonstrate how memory grows with each addition."""
    
    print("=== Memory Growth Per Addition ===\n")
    
    optimized = OptimizedWordFrequencyAnalyzer()
    
    # Track memory after each addition
    memory_usage = []
    
    for i in range(10):
        optimized.add_words(f"word{i}, word{i+1}, word{i+2}")
        
        # Calculate current memory usage
        main_memory = sys.getsizeof(optimized.word_counts)
        
        top5_memory = 0
        current = optimized.top_five_head
        while current:
            top5_memory += sys.getsizeof(current)
            current = current.next
        
        freq_memory = 0
        current = optimized.freq_head
        while current:
            freq_memory += sys.getsizeof(current)
            current = current.next
        
        current_memory = main_memory + top5_memory + freq_memory
        memory_usage.append(current_memory)
        print(f"After addition {i+1}: {current_memory} bytes")
    
    print(f"\nMemory growth pattern:")
    for i in range(1, len(memory_usage)):
        growth = memory_usage[i] - memory_usage[i-1]
        print(f"  Addition {i+1}: +{growth} bytes")


if __name__ == "__main__":
    analyze_memory_growth()
    print("\n" + "="*50 + "\n")
    analyze_memory_components()
    print("\n" + "="*50 + "\n")
    demonstrate_memory_growth()
