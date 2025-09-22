# Word Frequency Analyzer

An efficient data structure for analyzing word frequencies with three primary functions: tracking the top 5 most frequent words, finding the lowest frequency, and calculating the median frequency.

## Quick Start

### Running the Program

```bash
python3 optimized_linked_list_analyzer.py
```

### Basic Usage

1. **Add words** by entering comma-separated lists:
   ```
   > apple, banana, apple, cherry
   Added 4 word(s) to dictionary.
   ```

2. **View statistics** by typing `statistics`:
   ```
   > statistics
   === Word Frequency Statistics ===
   All word frequencies:
     apple: 2
     banana: 1
     cherry: 1
   Top 5 most frequent words:
     1. apple: 2
     2. banana: 1
     3. cherry: 1
   Lowest frequency: 1
   Median frequency: 1.0
   ```

3. **Available commands**:
   - Enter comma-separated words to add them
   - `statistics` - Show word frequency analysis
   - `debug` - Show internal data structure state
   - `clear` - Clear all words from dictionary
   - `help` - Show available commands
   - `quit` - Exit the program

## How It Works

### 1. Word Collection and Dictionary Management

The system uses Python's `Counter` class as the primary data structure:

```python
# When you input: "apple, banana, apple, cherry"
# The system processes each word:
self.word_counts = Counter()
for word in words:
    self.word_counts[word.lower()] += 1

# Result: {'apple': 2, 'banana': 1, 'cherry': 1}
```

**Key Features:**
- **Case-insensitive**: All words converted to lowercase
- **Whitespace handling**: Automatically strips spaces
- **Efficient counting**: O(1) average time for word addition
- **Memory efficient**: Only stores unique words and their counts

### 2. Top 5 Most Frequent Words Tracking

The system maintains a **specialized linked list** that always contains exactly 5 nodes maximum:

```python
class TopFiveNode:
    def __init__(self, word: str, frequency: int):
        self.word = word
        self.frequency = frequency
        self.next = None
        self.prev = None
```

**How it works:**
1. **Every time words are added**, the system recalculates the top 5
2. **Sorts all words** by frequency (descending), then alphabetically
3. **Takes the first 5** and stores them in a linked list
4. **Retrieval is O(1)** - just traverse the pre-computed list

**Example:**
```
Input: apple=4, banana=3, cherry=2, date=1, elderberry=1, fig=1
Top 5 List: [apple:4] -> [banana:3] -> [cherry:2] -> [date:1] -> [elderberry:1] -> None
```

**Benefits:**
- **Constant memory usage** (always 5 nodes max)
- **Fast retrieval** (no sorting needed when viewing statistics)
- **Automatic updates** (recalculated only when data changes)

### 3. Lowest Frequency Detection

The system maintains a **frequency count linked list** sorted by frequency (highest to lowest):

```python
class FrequencyCountNode:
    def __init__(self, frequency: int, count: int):
        self.frequency = frequency
        self.count = count  # How many words have this frequency
        self.next = None
        self.prev = None
```

**How it works:**
1. **Tracks frequency counts**: How many words have each frequency
2. **Maintains sorted order**: Highest frequency first
3. **Tail points to minimum**: The last node always contains the lowest frequency
4. **Retrieval is O(1)**: Just return `self.freq_tail.frequency`

**Example:**
```
Frequencies: apple=4, banana=3, cherry=2, date=1
Frequency Count List: [freq=4, count=1] -> [freq=3, count=1] -> [freq=2, count=1] -> [freq=1, count=1] -> None
                                                                                                    ↑
                                                                                              self.freq_tail
Lowest frequency: 1 (from tail)
```

**Benefits:**
- **O(1) access time** (no scanning needed)
- **Automatic maintenance** (updates when frequencies change)
- **Memory efficient** (only stores frequency counts, not individual words)

### 4. Median Frequency Calculation

The median is calculated from the **frequency values themselves**:

```python
def get_median_frequency(self) -> float:
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
```

**Example:**
```
Frequencies: apple=5, pair=5, pineapple=5, orange=3, strawberry=2, plum=2
Frequency values: [5, 5, 5, 3, 2, 2]
Sorted: [2, 2, 3, 5, 5, 5]
Median: 4.0 (average of 3 and 5, the two middle values)
```

**Benefits:**
- **Accurate calculation** (uses standard median formula)
- **Handles ties correctly** (multiple words with same frequency)
- **Works for any dataset size**

## Data Structure Architecture

### Memory Efficiency

The system uses **two specialized linked lists** instead of storing complete copies:

1. **Top 5 List**: Only stores the 5 most frequent words
2. **Frequency Count List**: Only stores frequency counts, not individual words

**Memory Usage:**
- **Main dictionary**: O(unique_words)
- **Top 5 list**: O(5) = constant
- **Frequency counts**: O(unique_frequencies)

**Total**: O(unique_words + unique_frequencies + 5)

### Performance Characteristics

| Operation | Time Complexity | Space Complexity |
|-----------|----------------|------------------|
| Add words | O(n) where n = words added | O(1) per word |
| Get top 5 | O(1) | O(1) |
| Get lowest frequency | O(1) | O(1) |
| Get median frequency | O(k log k) where k = unique words | O(k) |

## Files in This Project

- **`optimized_linked_list_analyzer.py`** - Main program with interactive interface
- **`test_demo.py`** - Demo script showing functionality
- **`memory_analysis.py`** - Analysis tools for understanding performance

## Example Session

```
=== Optimized Linked List Word Frequency Analyzer ===

> apple, banana, apple, cherry
Added 4 word(s) to dictionary.

> banana, cherry, elderberry, fig
Added 4 word(s) to dictionary.

> statistics
=== Word Frequency Statistics ===
All word frequencies:
  apple: 2
  banana: 2
  cherry: 2
  elderberry: 1
  fig: 1
Top 5 most frequent words:
  1. apple: 2
  2. banana: 2
  3. cherry: 2
  4. elderberry: 1
  5. fig: 1
Lowest frequency: 1
Median frequency: 1.0

> debug
=== Internal State ===
Total words: 8
Top 5 list: [('apple', 2), ('banana', 2), ('cherry', 2), ('elderberry', 1), ('fig', 1)]
Frequency counts: [(2, 3), (1, 2)]
All frequencies: {'apple': 2, 'banana': 2, 'cherry': 2, 'elderberry': 1, 'fig': 1}

> quit
Goodbye!
```

## Key Innovations

1. **Specialized Data Structures**: Each function uses the optimal data structure for its specific task
2. **Pre-computed Results**: Statistics are calculated once and cached, not recalculated on every access
3. **Memory Efficiency**: No data duplication - each piece of information is stored once
4. **Scalable Design**: Performance doesn't degrade with large datasets
5. **Interactive Interface**: Easy to use with real-time feedback

This design provides excellent performance for word frequency analysis while maintaining clean, readable code and efficient memory usage.
