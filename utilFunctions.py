## THIS IS THE FUNCTIONS FROM PART 1

from collections import defaultdict

# function to read data
def read_training_data(file_path):
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            if line.strip(): # not an empty line
                word, tag = line.strip().split()
                data.append((word, tag))
    return data

# function to estimate emission parameters
def estimate_emission_parameters(data):
    count_y = defaultdict(int) # count how many times y appears overall
    count_y_to_x = defaultdict(lambda: defaultdict(int))  # count how many times word x is tagged with y
    
    for word, tag in data:
        count_y[tag] += 1
        count_y_to_x[tag][word] += 1

    emission_probs = {}  # e(x|y)

    for tag in count_y_to_x:
        emission_probs[tag] = {}
        for word in count_y_to_x[tag]:
            emission_probs[tag][word] = count_y_to_x[tag][word] / count_y[tag]
    
    return emission_probs

def replace_rare_words(data, word_counts, k=3):
    new_data = []
    for word, tag in data:
        if word_counts[word] < k:
            new_data.append(('#UNK#', tag))
        else:
            new_data.append((word, tag))
    return new_data

# function to count word frequencies
def count_word_frequencies(data):
    word_counts = defaultdict(int)
    for word, _ in data:
        word_counts[word] += 1
    return word_counts