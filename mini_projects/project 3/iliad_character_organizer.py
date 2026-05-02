import zipfile
import os
import re
from collections import defaultdict, Counter

def extract_zip(zip_path, extract_to='temp_extracted'):
    """Extract the zip file to a temporary directory."""
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    return extract_to

def get_text_directory(input_path):
    """Get the directory containing text files, handling both zip files and directories."""
    if os.path.isfile(input_path) and input_path.endswith('.zip'):
        # It's a zip file, extract it
        return extract_zip(input_path)
    elif os.path.isdir(input_path):
        # It's already a directory
        return input_path
    else:
        raise ValueError(f"Input path {input_path} is not a valid zip file or directory")

def read_text_files(directory):
    """Read all text files from the directory."""
    text = ""
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                try:
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        text += f.read() + "\n"
                except UnicodeDecodeError:
                    # Try different encoding
                    try:
                        with open(os.path.join(root, file), 'r', encoding='latin-1') as f:
                            text += f.read() + "\n"
                    except:
                        print(f"Could not read file {file} due to encoding issues")
            elif file.endswith('.html') or file.endswith('.htm'):
                try:
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        html_content = f.read()
                        # Simple HTML text extraction (remove tags)
                        import re
                        text_content = re.sub(r'<[^>]+>', '', html_content)
                        text += text_content + "\n"
                except UnicodeDecodeError:
                    try:
                        with open(os.path.join(root, file), 'r', encoding='latin-1') as f:
                            html_content = f.read()
                            text_content = re.sub(r'<[^>]+>', '', html_content)
                            text += text_content + "\n"
                    except:
                        print(f"Could not read HTML file {file} due to encoding issues")
    return text

def extract_characters(text):
    """Extract potential character names using regex and frequency analysis."""
    # Remove HTML tags more thoroughly
    text = re.sub(r'<[^>]+>', '', text)
    # Remove CSS and JavaScript
    text = re.sub(r'\{[^}]*\}', '', text)
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL|re.IGNORECASE)
    
    # Find capitalized words that might be names (simple heuristic)
    potential_names = re.findall(r'\b[A-Z][a-z]+\b', text)
    
    # Common words to filter out (pronouns, articles, etc.)
    non_character_words = {
        'The', 'And', 'But', 'For', 'Not', 'With', 'From', 'This', 'That', 'When', 'Where', 'What', 'How', 'Why',
        'Who', 'Which', 'Their', 'They', 'Them', 'These', 'Those', 'There', 'Here', 'Then', 'Than', 'So', 'As',
        'At', 'By', 'In', 'On', 'Of', 'To', 'For', 'With', 'About', 'Against', 'Between', 'Into', 'Through',
        'During', 'Before', 'After', 'Above', 'Below', 'Under', 'Over', 'Near', 'Far', 'Left', 'Right',
        'Project', 'Gutenberg', 'Ebook', 'Title', 'Author', 'Chapter', 'Book', 'Part', 'Section', 'Page',
        'Text', 'Html', 'Body', 'Head', 'Title', 'Style', 'Script', 'Div', 'Span', 'Table', 'Row', 'Cell',
        'He', 'His', 'Him', 'Her', 'She', 'It', 'Its', 'We', 'Us', 'Our', 'You', 'Your', 'I', 'Me', 'My',
        'All', 'Some', 'Any', 'Each', 'Every', 'No', 'Nor', 'Or', 'Yet', 'So', 'Such', 'Only', 'Very',
        'Most', 'More', 'Less', 'Few', 'Many', 'Much', 'Little', 'Great', 'Good', 'Bad', 'New', 'Old',
        'First', 'Last', 'Next', 'Same', 'Other', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven',
        'Eight', 'Nine', 'Ten', 'Now', 'Then', 'Here', 'There', 'When', 'Where', 'Why', 'How', 'What',
        'Who', 'Which', 'Whose', 'Whom', 'That', 'This', 'These', 'Those', 'All', 'Both', 'Each', 'Either',
        'Neither', 'None', 'Some', 'Such', 'Enough', 'Little', 'Many', 'Much', 'Several', 'Few'
    }
    
    # Count frequencies, excluding non-character words
    name_counts = Counter(name for name in potential_names if name not in non_character_words)
    
    # Filter names that appear multiple times (likely characters)
    characters = {name: count for name, count in name_counts.items() if count > 3}  # Lower threshold
    
    # Known Iliad characters for reference (expanded list)
    known_characters = {
        'Achilles', 'Hector', 'Agamemnon', 'Odysseus', 'Patroclus', 'Priam', 'Hecuba', 'Andromache', 
        'Paris', 'Helen', 'Ajax', 'Diomedes', 'Nestor', 'Menelaus', 'Sarpedon', 'Glaucus', 'Aeneas', 
        'Apollo', 'Athena', 'Zeus', 'Hera', 'Poseidon', 'Ares', 'Hermes', 'Aphrodite', 'Artemis', 
        'Hephaestus', 'Dionysus', 'Demeter', 'Hades', 'Persephone', 'Cronus', 'Rhea', 'Oceanus',
        'Troy', 'Greece', 'Argos', 'Sparta', 'Mycenae', 'Ithaca', 'Pylos', 'Crete', 'Delphi',
        'Chryses', 'Briseis', 'Pandarus', 'Idomeneus', 'Meriones', 'Teucer', 'Thersites', 'Ulysses',
        'Jove', 'Minerva', 'Mars', 'Venus', 'Vulcan', 'Bacchus', 'Ceres', 'Pluto', 'Proserpine',
        'Saturn', 'Ops', 'Neptune', 'Iris', 'Hebe', 'Thetis', 'Calchas', 'Idaeus', 'Talthybius'
    }
    
    # Prioritize known characters and high-frequency proper names
    filtered_characters = {}
    for name, count in characters.items():
        if name in known_characters or count > 15:  # Higher threshold for unknown names
            filtered_characters[name] = count
    
    return filtered_characters

def extract_character_traits(text, character_name):
    """Extract possible character traits from text contexts."""
    # Common character traits to look for
    trait_keywords = {
        'brave': ['brave', 'courageous', 'valiant', 'fearless', 'bold', 'undaunted'],
        'wise': ['wise', 'sage', 'prudent', 'intelligent', 'clever', 'shrewd', 'discerning'],
        'fierce': ['fierce', 'ferocious', 'savage', 'ruthless', 'cruel', 'furious', 'wrathful'],
        'noble': ['noble', 'honorable', 'dignified', 'majestic', 'regal', 'lofty'],
        'swift': ['swift', 'fast', 'quick', 'rapid', 'fleet', 'speedy'],
        'strong': ['strong', 'powerful', 'mighty', 'robust', 'sturdy', 'vigorous'],
        'skilled': ['skilled', 'expert', 'adept', 'proficient', 'masterful', 'dexterous'],
        'proud': ['proud', 'haughty', 'arrogant', 'conceited', 'lofty'],
        'wrathful': ['wrathful', 'angry', 'furious', 'enraged', 'ireful', 'indignant'],
        'loyal': ['loyal', 'faithful', 'devoted', 'steadfast', 'true'],
        'deceptive': ['deceptive', 'cunning', 'sly', 'treacherous', 'crafty', 'wily'],
        'beautiful': ['beautiful', 'fair', 'lovely', 'handsome', 'comely', 'radiant'],
        'divine': ['divine', 'godlike', 'immortal', 'celestial', 'heavenly', 'eternal'],
        'mortal': ['mortal', 'human', 'earthly', 'fleshly', 'perishable']
    }
    
    # Find sentences containing the character
    sentences = re.split(r'[.!?]+', text)
    character_sentences = [s for s in sentences if character_name in s]
    
    # Count trait mentions in close proximity to character name
    trait_counts = {}
    for sentence in character_sentences:
        sentence_lower = sentence.lower()
        char_pos = sentence_lower.find(character_name.lower())
        
        if char_pos != -1:
            # Look in a window around the character name (±50 characters)
            window_start = max(0, char_pos - 50)
            window_end = min(len(sentence_lower), char_pos + len(character_name) + 50)
            context_window = sentence_lower[window_start:window_end]
            
            for trait, keywords in trait_keywords.items():
                for keyword in keywords:
                    if keyword in context_window:
                        trait_counts[trait] = trait_counts.get(trait, 0) + 1
                        break  # Count each trait only once per sentence
    
    # Return traits that appear at least once, sorted by frequency
    significant_traits = [(trait, count) for trait, count in trait_counts.items() if count >= 2]
    return sorted(significant_traits, key=lambda x: x[1], reverse=True)

def find_character_context(text, character_name, context_window=100):
    """Find contexts where a character is mentioned."""
    contexts = []
    sentences = re.split(r'[.!?]+', text)
    for sentence in sentences:
        if character_name in sentence:
            # Get context around the mention
            start = max(0, sentence.find(character_name) - context_window)
            end = min(len(sentence), sentence.find(character_name) + len(character_name) + context_window)
            context = sentence[start:end].strip()
            contexts.append(context)
    return contexts[:5]  # Return top 5 contexts

def generate_character_report(characters, text):
    """Generate a detailed report of characters."""
    report = "Iliad Character Analysis Report\n"
    report += "=" * 40 + "\n\n"
    
    for name, count in sorted(characters.items(), key=lambda x: x[1], reverse=True):
        report += f"Character: {name}\n"
        report += f"Mentions: {count}\n"
        
        # Add character traits
        traits = extract_character_traits(text, name)
        if traits:
            report += "Possible Traits: "
            trait_names = [trait[0] for trait in traits[:5]]  # Top 5 traits
            report += ", ".join(trait_names) + "\n"
        else:
            report += "Possible Traits: None identified\n"
        
        contexts = find_character_context(text, name)
        if contexts:
            report += "Sample contexts:\n"
            for i, ctx in enumerate(contexts, 1):
                report += f"  {i}. ...{ctx}...\n"
        report += "\n" + "-" * 20 + "\n\n"
    
    return report

def main(input_path):
    """Main function to process the zip file or directory and generate character details."""
    try:
        # Get directory with text files
        text_dir = get_text_directory(input_path)
        
        # Read text
        text = read_text_files(text_dir)
        
        if not text:
            print("No text files found in the input.")
            return
        
        # Extract characters
        characters = extract_characters(text)
        
        # Generate report
        report = generate_character_report(characters, text)
        
        # Save report
        with open('character_report.txt', 'w', encoding='utf-8') as f:
            f.write(report)
        
        print("Character analysis complete. Report saved to 'character_report.txt'")
        print(f"Found {len(characters)} potential characters.")
        
        # Clean up extracted files (only if we extracted a zip)
        if text_dir != input_path and os.path.exists(text_dir):
            import shutil
            shutil.rmtree(text_dir)
        
    except Exception as e:
        print(f"Error processing input: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python iliad_character_organizer.py <path_to_zip_file_or_directory>")
    else:
        main(sys.argv[1])