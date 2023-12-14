# MIT License

# Copyright (c) 2023 Esteban Framcisco Chacon Mosquera <estebanfex@gmail.com>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import re
import sys
import openai
from os.path import join, dirname, abspath
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton

def read_api_key_from_file(file_path):
    try:
        with open(file_path, 'r') as key_file:
            api_key = key_file.read().strip()
        return api_key
    except FileNotFoundError:
        print(f"File '{file_path}' not found. Please make sure the file exists.")
        return None

def load_dictionary_from_file(file_path):
    try:
        dictionary = {}
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                
                if line:
                    Language1, Language2 = line.split(':')
                    dictionary[Language1] = Language2
        return dictionary
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def replace_file(source_file_path, destination_file_path):
    try:
        # Read the content of the source file
        with open(source_file_path, 'r') as source_file:
            source_content = source_file.read()

        # Write the content to the destination file, overwriting its existing content
        with open(destination_file_path, 'w') as destination_file:
            destination_file.write(source_content)
    
    except FileNotFoundError:
        print(f"File not found: {source_file_path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def replace_dictionary_in_file(file_path, dictionary):
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()

        for word, replacement in dictionary.items():
            file_content = file_content.replace(word, replacement)

        with open(file_path, 'w') as file:
            file.write(file_content)
            
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def extract_keys_from_dict(dictionary):
    keys_only = [key.strip('<string></string>') for key in dictionary.keys() if key.startswith('<string>') and key.endswith('</string>')]

    return keys_only  # Return the list of keys instead of printing it

def translate_with_openai(keys, target_language):
    if target_language == "EN":
        return keys

    # Initialize the OpenAI API client
    key_file_path = join(dirname(abspath(__file__)), 'myKey.txt')
    openai.api_key = read_api_key_from_file(key_file_path)

    # Concatenate the keys into a single string
    input_text = "\n".join(keys)

    # Make a single API call to translate the entire input text to Spanish
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Translate the following English text to {target_language}, keep letter cases, complete incomplete words that are related an APP interface:\n{input_text}\n",
        max_tokens=450,  # Adjust the max_tokens as needed
        n=1,
        stop=None,
        temperature=0.7,
    )

    translated_text = response.choices[0].text.strip()
    translated_keys = translated_text.split('\n')

    return translated_keys

def update_file(dictionary, translations, output_file_path):
    updated_dict = {}
    
    for count, (key, value) in enumerate(dictionary.items()):
        if count < len(translations):
            updated_dict[key] = translations[count]
        else:
            updated_dict[key] = value
    
    # Write the updated dictionary to the output file
    with open(output_file_path, 'w') as output_file:
        for key, value in updated_dict.items():
            output_file.write(f"{key}: {value}\n")

    return updated_dict;

class TranslationApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Translation App')
        self.setGeometry(100, 100, 400, 200)

        self.label = QLabel('Enter Target Language:', self)
        self.label.move(20, 20)

        self.language_input = QLineEdit(self)
        self.language_input.setGeometry(20, 50, 200, 30)
        self.language_input.setMaxLength(15)

        self.translate_button = QPushButton('Translate', self)
        self.translate_button.setGeometry(20, 90, 150, 40)
        self.translate_button.clicked.connect(self.translate_and_replace)

    def translate_and_replace(self):
        target_language = self.language_input.text()
        if target_language:
            # Your translation and file replacement code here
            file_path = join(dirname(abspath(__file__)), 'content.txt')
            file_path_ui = join(dirname(abspath(__file__)), 'mainwindow.ui')
            file_path_ui_Original = join(dirname(abspath(__file__)), 'mainwindow_Original.ui')
            loaded_dict = load_dictionary_from_file(file_path)
            replace_file(file_path_ui_Original, file_path_ui)

            strings_EN = extract_keys_from_dict(loaded_dict)
            strings_translated = translate_with_openai(strings_EN, target_language)
            formatted_translation = list(map(lambda element: f'<string>{element}</string>', strings_translated))
            updated_dic = update_file(loaded_dict, formatted_translation, file_path)
            replace_dictionary_in_file(file_path_ui, updated_dic)
            print(f"Translation completed for {target_language}")
        else:
            print("Please enter a target language.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TranslationApp()
    window.show()
    sys.exit(app.exec_())
