import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
import time
import openai
from faster_whisper import WhisperModel

openai.api_key = 'your-openai-api-key'

async def refine_cultural_context(text, language):
    prompt = f"""You are a language model that has been tasked with culturally adapting a translated text to {language} culture. Please preserve the content of the text exactly but replace names, place names, and cultural references with ones that are appropriate for {language} culture.
Here is the text:
{text}
Please provide the culturally adapted text below:
"""
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[{"role": "system", "content": prompt}],
            max_tokens=2000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error in OpenAI API call: {str(e)}")
        return text  # Return original text if API call fails

async def process_file(filename, input_dir, output_dir, language):
    input_path = os.path.join(input_dir, filename)
    output_filename = f"{os.path.splitext(filename)[0]}_refined_{language}.txt"
    output_path = os.path.join(output_dir, output_filename)

    try:
        with open(input_path, 'r', encoding='utf-8') as file:
            text = file.read()
        
        refined_text = await refine_cultural_context(text, language)
        
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(refined_text)
        
        print(f"Refined {filename} for {language} culture and saved as {output_filename}")
    except Exception as e:
        print(f"Failed to process {filename}: {str(e)}")

async def process_translated_chapters(input_dir, output_dir, language):
    os.makedirs(output_dir, exist_ok=True)
    
    files = [f for f in os.listdir(input_dir) if f.endswith(".txt")]
    
    tasks = [process_file(f, input_dir, output_dir, language) for f in files]
    await asyncio.gather(*tasks)

async def main():
    # Assuming the WhisperModel transcription is already done and files are saved
    input_directory = "generated_transcript_combined_texts"
    output_directory = "culturally_adapted_transcripts"
    language = "Spanish"  # Target language cultural context

    start_time = time.time()
    await process_translated_chapters(input_directory, output_directory, language)
    print(f"Total execution time: {time.time() - start_time:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())