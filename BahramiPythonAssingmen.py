import re
import os

def read_values(file_path):
    values = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                letter, value = line.strip().split()
                values[letter] = int(value)
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
    except Exception as e:
        print(f"An error occurred while reading values: {e}")
    return values

def tokenize_name(name):
    # Split into words based on non-alphabetic characters and remove apostrophes
    words = [re.sub(r"[']", "", word) for word in re.split(r'[^a-zA-Z]+', name) if word]
    return words

def calculate_score(letter, position, values):
    if position == 1:  # First letter of a word
        return 0
    elif position == 3 and letter == 'E':  # Last letter is 'E'
        return 20
    elif position == 3:  # Last letter of a word
        return 5
    else:  # Neither first nor last letter
        return position + values.get(letter.upper(), 0)

def generate_abbreviations(name, values):
    words = tokenize_name(name)
    abbreviation = ""
    abbreviation_score = 0

    for word in words:
        abbreviation += word[0].upper()  # Add the first letter (uppercase) of the word to the abbreviation
        abbreviation_score += calculate_score(word[0], 1, values)  # First letter of a word

    for i in range(1, min(3, max(len(word) for word in words)) + 1):
        for word in words:
            if i <= len(word):
                position = i if i <= 2 else 3  # Position value
                letter = word[i - 1]

                if i == len(word):
                    score = calculate_score(letter, position, values)
                else:
                    # Letter is neither the first nor last letter of a word
                    score = calculate_score(letter, position, values)

                if i == 1 or i == 2:  # Calculate score only for the second and third letters
                    abbreviation_score += score

    return abbreviation, abbreviation_score

def choose_best_abbreviation(abbreviations):
    best_abbreviation = min(abbreviations, key=lambda x: x[1])
    return best_abbreviation[0]

def main():
    surname = input("Please enter your surname: ")
    input_file_path = input("Enter the name of the input file (e.g., names.txt): ")
    values_file_path = 'values.txt'

    # Check if the input file has the .txt extension
    if not input_file_path.lower().endswith('.txt'):
        print("Error: The input file must have the extension .txt.")
        return

    # Extract surname and input file name without extension
    input_file_name, _ = os.path.splitext(os.path.basename(input_file_path))
    
    letter_values = read_values(values_file_path)

    try:
        with open(input_file_path, 'r') as input_file, open(f'{surname}_{input_file_name}_abbrevs.txt', 'w') as output_file:
            for line in input_file:
                abbreviation, _ = generate_abbreviations(line.strip(), letter_values)
                output_file.write(line.strip() + '\n' + abbreviation + '\n\n')
    except FileNotFoundError:
        print(f"Error: File {input_file_path} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
