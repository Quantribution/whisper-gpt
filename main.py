import os

import speech_recognition as sr
import openai
import whisper
from google.cloud import texttospeech

# Supress pygame import welcome message
import contextlib
with contextlib.redirect_stdout(None):
    import pygame

# Retrieve Google API credentials
os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Initialize OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

# Instantiates a client
client = texttospeech.TextToSpeechClient()

# Build the voice request
voice = texttospeech.VoiceSelectionParams(
    language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
)

# Initialize Whisper
model = whisper.load_model("base")

def transcribe_audio_to_text():
    try:
        return model.transcribe("input.wav")
    except:
        print("Transcription failed.")

def generate_response(prompt):
    response = openai.Completion.create(
        model="gpt-3.5-turbo",
        prompt=f"{prompt}",
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # Extract the generated text from the API response
    generated_text = response["choices"][0]["text"]
    
    return generated_text

def speak_text(text):
    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the type of audio file returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open("./output.wav", "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print('Audio content written to file "output.wav"')

    # Load the audio file and play it using Pygame
    pygame.mixer.init()
    pygame.mixer.music.load("output.wav")
    pygame.mixer.music.play()

def main():
    while True:
        # Activate Voice Assistant
        print(f"Say 'Whisper GPT' to start recording your question.")

        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)

            try:
                transcription = recognizer.recognize_whisper(audio, language="english").strip().rstrip(".")
                if transcription.lower() == "whisper gpt":
                    # Record audio
                    filename ="input.wav"
                    print("Ready for prompt!")

                    with sr.Microphone() as source:
                        recognizer = sr.Recognizer()
                        source.pause_threshold = 1
                        audio = recognizer.listen(source,phrase_time_limit=None,timeout=None)

                        with open(filename,"wb")as f:
                            f.write(audio.get_wav_data())
                            
                    # Transcript audio to text 
                    text = transcribe_audio_to_text()["text"]
                    if text:
                        print(f"You said: {text}")
                        
                        # Generate the response
                        response = generate_response(text)
                        print(f"Response: {response}")
                            
                        # Read the response using GPT3
                        speak_text(response)
                        
            except Exception as e:          
                print("An error ocurred: {}".format(e))
                
if __name__=="__main__":
    main()
