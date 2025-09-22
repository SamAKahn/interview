#!/usr/bin/env python3
"""
Demo script to show how the Optimized WordFrequencyAnalyzer works interactively.
This simulates user input to demonstrate the functionality with incremental updates.
"""

from optimized_linked_list_analyzer import OptimizedWordFrequencyAnalyzer

def demo_interactive_usage():
    """Demonstrate the interactive functionality of OptimizedWordFrequencyAnalyzer."""
    
    print("=== Word Frequency Analyzer Demo ===\n")
    
    # Create analyzer instance
    analyzer = OptimizedWordFrequencyAnalyzer()
    
    # Simulate user inputs
    test_inputs = [
        "apple, banana, apple, cherry",
        "banana, cherry, elderberry, fig",
        "apple, grape, apple, banana",
        "statistics",
        "date, elderberry, fig, grape, honey",
        "statistics",
        "clear",
        "statistics",
        "quit"
    ]
    
    for user_input in test_inputs:
        print(f"> {user_input}")
        
        if user_input.lower() == 'quit':
            print("Goodbye!")
            break
        elif user_input.lower() == 'help':
            print("\nAvailable commands:")
            print("  - Enter comma-separated words to add them to the dictionary")
            print("  - 'statistics' - Show word frequency analysis")
            print("  - 'clear' - Clear all words from the dictionary")
            print("  - 'help' - Show this help message")
            print("  - 'quit' - Exit the program\n")
        elif user_input.lower() == 'clear':
            analyzer.clear()
            print("Dictionary cleared.\n")
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

if __name__ == "__main__":
    demo_interactive_usage()
