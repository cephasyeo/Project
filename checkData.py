from collections import Counter

def analyze_predictions(pred_path, devin_path=None, emission_probs=None):
    tag_counts = Counter()
    word_tag_pairs = []
    lines_checked = 0

    with open(pred_path) as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split()
                if len(parts) == 2:
                    word, tag = parts
                    tag_counts[tag] += 1
                    word_tag_pairs.append((word, tag))
                    lines_checked += 1

    print("=== Tag Distribution in dev.p2.out ===")
    for tag, count in tag_counts.most_common():
        print(f"{tag:7} : {count} ({count / lines_checked:.2%})")

    print("\nTotal lines checked:", lines_checked)
    print("Unique tags used:", len(tag_counts))

    if devin_path:
        with open(devin_path) as f:
            dev_words = [line.strip() for line in f if line.strip()]
        total_dev_words = len(dev_words)
        print("\n=== dev.in Coverage Check ===")
        if total_dev_words != lines_checked:
            print(f"WARNING: Mismatch in word counts between dev.in ({total_dev_words}) and dev.p2.out ({lines_checked})")
        else:
            print("✅ Word counts match between dev.in and dev.p2.out")

    if emission_probs:
        print("\n=== #UNK# Emission Check (selected tags) ===")
        for tag in ["B-NP", "I-NP", "B-VP", "I-VP", "O"]:
            prob = emission_probs.get(tag, {}).get("#UNK#", 0)
            print(f"{tag:5} -> #UNK#: {prob:.6f}")

        print("\n=== Emission Sum Sanity Check (sample tags) ===")
        for tag in ["B-NP", "I-NP", "O"]:
            total = sum(emission_probs.get(tag, {}).values())
            print(f"{tag:5} emission sum: {total:.3f}")


# Example usage
if __name__ == "__main__":
    from utilFunctions import (
        estimate_emission_parameters,
        read_training_data,
        replace_rare_words,
        count_word_frequencies
    )

    train_data = read_training_data("EN/train")
    word_counts = count_word_frequencies(train_data)
    train_data_unk = replace_rare_words(train_data, word_counts, k=3)
    emission_probs = estimate_emission_parameters(train_data_unk)

    analyze_predictions("EN/dev.p2.out", devin_path="EN/dev.in", emission_probs=emission_probs)
