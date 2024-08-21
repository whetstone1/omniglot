from googletrans import Translator, LANGUAGES
import os
from concurrent.futures import ThreadPoolExecutor
import time

def translate_text(text, target_language):
    translator = Translator()
    translated = translator.translate(text, dest=target_language)
    return translated.text

def process_file(filename, input_dir, output_dir):
    with open(os.path.join(input_dir, filename), 'r', encoding='utf-8') as file:
        text = file.read()
    
    translator = Translator()
    
    for language_code, language_name in LANGUAGES.items():
        try:
            translated_text = translator.translate(text, dest=language_code).text
            
            output_filename = f"{os.path.splitext(filename)[0]}_{language_code}.txt"
            language_output_dir = os.path.join(output_dir, language_name)
            
            os.makedirs(language_output_dir, exist_ok=True)
            with open(os.path.join(language_output_dir, output_filename), 'w', encoding='utf-8') as file:
                file.write(translated_text)
            
            print(f"Translated {filename} to {language_name} and saved as {output_filename}")
        
        except Exception as e:
            print(f"Failed to translate {filename} to {language_name} due to {str(e)}")

def process_chapters(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    files = [f for f in os.listdir(input_dir) if f.endswith(".txt")]
    
    with ThreadPoolExecutor() as executor:
        executor.map(lambda f: process_file(f, input_dir, output_dir), files)

# Example usage:
input_directory = "path/to/input/transcripts"
output_directory = "path/to/output/transcripts"

start_time = time.time()
process_chapters(input_directory, output_directory)
print(f"Total execution time: {time.time() - start_time:.2f} seconds")