# whisper-gpt

whisper-gpt is a Python script that utilizes OpenAI's GPT-3.5 language model, Whisper speech-to-text engine, and Google Cloud's Text-to-Speech API, and to create a basic voice assistant that can transcribe speech, generate responses using GPT-3.5, and synthesize speech from the generated responses. 

## Installation
1. Clone this repository using `git clone https://github.com/quantribution/whisper-gpt.git`
2. Install the required Python libraries using `pip install -r requirements.txt`
3. Set up an OpenAI API key and add it to your environment variables as `OPENAI_API_KEY`. 
4. Set up a Google Cloud Service Account and add the key path to your environment variables as `GOOGLE_APPLICATION_CREDENTIALS`. 

## Usage
1. Run the program by typing `python main.py` in your terminal.
2. When prompted, say "Whisper GPT" to activate the voice assistant and start recording your question.
3. Wait for the voice assistant to generate and read the response.

Note: Ensure that your microphone is connected and working properly before running the program.

## Contributions
If you would like to contribute to this project, feel free to open a pull request with your changes.
