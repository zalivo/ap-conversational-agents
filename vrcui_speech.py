import time
import os
import sys
import requests
import json

#import resource
# import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer,SpeechRecognizer, AudioConfig, AudioOutputConfig, ResultReason
from azure.cognitiveservices.speech.audio import AudioOutputConfig
from openai import AzureOpenAI

#dotenv
from dotenv import load_dotenv
load_dotenv()

# internal imports
from content_handling import ContentHandler
from knowledge_connection import PaintingKnowledge
#--------------------------------------------------
class VRisper:
    def __init__(self, prompt, knowledge_base):
        # Initialise Azure OpenAI
        self.client = AzureOpenAI(
            azure_endpoint=os.environ.get('GPT_ENDPOINT'),
            api_key=os.environ.get('GPT_KEY'),
        )
        #Speech Config
        self.speech_config = SpeechConfig(
            subscription=os.environ.get('SPEECH_KEY'), 
            region=os.environ.get('SPEECH_REGION'),
            speech_recognition_language="en-US",
        )
        self.speech_config.speech_synthesis_voice_name='en-US-JennyMultilingualNeural'
        #Audio Config
        self.audio_output_config = AudioOutputConfig(use_default_speaker=True)
        self.audio_config = AudioConfig(use_default_microphone=True)
 
        # speech Recognizer - STT
        self.speech_recognizer = SpeechRecognizer(
            speech_config=self.speech_config, 
            audio_config=self.audio_config
        )
        
        # Speech Synthesizer - TTS
        self.tts_sentence_end = [ ".", "!", "?", ";", "。", "！", "？", "；", "\n" ]
        self.speech_synthesizer = SpeechSynthesizer(
            speech_config=self.speech_config, 
            audio_config=self.audio_output_config)

        # prompt and conversation responsee
        self.system_prompt = prompt # prompt to GPT-4
        self.user_input = None
        self.voice_response = None

        # Neo4j database
        self.knowledge_db = PaintingsKnowledge(
            uri=os.environ.get('NEO4J_URI'), 
            user=os.environ.get('NEO4J_USER'), 
            password=os.environ.get('NEO4J_PASSWORD')
        )
        # self.knowledge_db = GraphDatabase.driver(
        #     uri=os.environ.get('NEO4J_URI'), 
        #     auth=(os.environ.get('NEO4J_USER'), os.environ.get('NEO4J_PASSWORD'))
        # )

    # Static properties to call out
    @property
    def openai_model(self):
        return self.client
    
    @property
    def synthesizer(self):
        return self.speech_synthesizer
    
    @property
    def recognizer(self):
        return self.speech_recognizer
    
    @property
    def knowledge(self):
        return self.knowledge_db

    @property
    def system_prompt(self):
        return self.system_prompt


    # FUNCTIONS OF THE VR-CUI-----------------------------------
    def send_voice_request(self, user_input):
        # Ask Azure OpenAI in streaming way
        response = self.client.chat.completions.create(
            model=deployment_id, 
            max_tokens=200, 
            stream=True, 
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_input} #user input - parsing by the stream conversation
            ]
        )
        collected_messages = []
        last_tts_request = None

        # iterate through the stream response stream
        for chunk in response:
            if len(chunk.choices) > 0:
                chunk_message = chunk.choices[0].delta.content  # extract the message
                if chunk_message is not None:
                    collected_messages.append(chunk_message)  # save the message
                    if chunk_message in self.tts_sentence_end: # sentence end found
                        text = ''.join(collected_messages).strip() # join the recieved message together to build a sentence
                        if text != '': # if sentence only have \n or space, we could skip
                            print(f"Speech synthesized to speaker for: {text}")
                            last_tts_request = self.speech_synthesizer.speak_text_async(text)
                            collected_messages.clear()
        if last_tts_request:
            last_tts_request.get() #send request to ask

    # Speech-to-Text Chat
    def stt_chat(self):
        while True:
            print("Listening...")
            try:
                # Get audio from the microphone and then send it to the TTS service.
                speech_recognition_result = self.speech_recognizer.recognize_once_async().get()

                # Speech was recognized, send the voice input
                if speech_recognition_result.reason == ResultReason.RecognizedSpeech:
                    # Case 1: Command: Vrisper - start the conversation #TODO: Change different name
                    if speech_recognition_result.text == "Hi, Vrisper.":
                       print("Conversation started.")
                    # Case 2: Command: STOP - end the conversation
                    elif speech_recognition_result.text == "Stop.": 
                        print("Conversation ended.")
                        break
                    # Case 3: Normal conversation
                    else:
                        #FIXME: Added different content handling
                        # list of pre-defined topics,painting knowledge, image processing
                        # user input match with each of these cases
                        continue
                        
                    conversation = speech_recognition_result.text
                    print("Recognized speech: {}".format(conversation))

                    # self.user_input = conversation #FIXME: remove or updated
                    self.send_voice_request(conversation)## TODO: from user input, adding to prompt

                # No speech was recognized
                elif speech_recognition_result.reason == ResultReason.NoMatch:
                    print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
                    # TODO: Adding the handling that Whisper responds with something else
                    break

                # cancel the voice
                elif speech_recognition_result.reason == ResultReason.Canceled:
                    cancellation_details = speech_recognition_result.cancellation_details
                    print("Speech Recognition canceled: {}".format(cancellation_details.reason))
                    if cancellation_details.reason == speechsdk.CancellationReason.Error:
                        print("Error details: {}".format(cancellation_details.error_details))
            except EOFError:
                break

    # Text-to-Speech Chat
    def tts_chat(self, text):
        """
        Convert conversation on-going and output to speaker.
        """	
        try:
            result = self.speech_synthesizer.speak_text_async(text).get()
            if result.reason == ResultReason.SynthesizingAudioCompleted:
                print("Text-to-speech conversion successful.")
                self.voice_response = result
                ## FIXME: any cases to handle?
                return True
            else:
                print(f"Error synthesizing audio: {result}")
                return False
        except Exception as ex:
            print(f"Error synthesizing audio: {ex}")
            return False






