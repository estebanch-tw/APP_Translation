
import openai

# Replace 'YOUR_API_KEY' with your actual OpenAI API key
api_key = 'myKey'

def translate_text_with_gpt3(text, target_language='es'):
    openai.api_key = api_key
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Translate the following English text to {target_language}, keep letter cases: '{text}'",
        max_tokens=50,  # Adjust this as needed for longer translations
        temperature=0.3  # Set temperature to 0 for deterministic output
    )

    if response.choices:
        translated_text = response.choices[0].text.strip()
        return translated_text
    else:
        print("Translation failed.")
        return None

if __name__ == '__main__':
    text_to_translate = input("Enter text to translate: ")
    translated_text = translate_text_with_gpt3(text_to_translate)

    if translated_text:
        print(f"Translation: {translated_text}")
