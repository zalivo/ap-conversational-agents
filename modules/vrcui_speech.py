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

from promptflow.core import Prompty
from IPython.display import Image, display # for displaying images of paintings

#dotenv
from dotenv import load_dotenv
load_dotenv('.env')

# internal imports
# from content_handling import ContentHandler
from knowledge_connection import PaintingsKnowledge
from voice_command import VoiceCommand
#--------------------------------------------------
class VRisper:
    def __init__(self, for_user):
        # Initialise Azure OpenAI
        self.client = AzureOpenAI(
            azure_endpoint=os.getenv('GPT_ENDPOINT'),
            api_key=os.getenv('GPT_KEY'),
            api_version="2024-02-01"
        )
        #Speech Config
        self.speech_config = SpeechConfig(
            subscription=os.getenv('SPEECH_KEY'), 
            region=os.getenv('SPEECH_REGION'),
            speech_recognition_language="en-US",
        )
        self.speech_config.speech_synthesis_voice_name='en-US-JennyMultilingualNeural' #"en-GB-RyanNeural"
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

        # Neo4j database
        # self.knowledge_db = PaintingsKnowledge(
        #     uri=os.getenv('NEO4J_URI'), 
        #     user=os.getenv('NEO4J_USER'), 
        #     password=os.getenv('NEO4J_PASSWORD')
        # )

        self.user_input = None
        self.voice_response = None
        self.username = for_user
        self.context = ""
        self.topics = []

    # Properties of the model
    @property
    def openai_model(self):
        return self.client
    
    @property
    def synthesizer(self):
        return self.speech_synthesizer
    
    @property
    def recognizer(self):
        return self.speech_recognizer
    
    # @property
    # def knowledge_graph(self):
    #     return self.knowledge_db

    @property
    def username(self):
        return self.username
    
    @property
    def user_input(self):
        return self.user_input

    @property
    def context(self):
        return self.context
    #SETTERS
    def set_context(self, context):
        self.context = context
    
    def set_topics(self, topics):
        self.topics = topics

    def set_user_input(self, user_input):
        self.user_input = user_input
    
    # FUNCTIONS OF THE VR-CUI-----------------------------------

    # Speech-to-Text - User Input to VUIs
    def speech_to_text(self):
        while True:
            print("Listening...")
            try:
                # Recognition result from input
                recog_result = self.speech_recognizer.recognize_once_async().get()

                # Speech was recognized
                if recog_result.reason == ResultReason.RecognizedSpeech:
                    print("User: {}".format(recog_result.text))
                    self.user_input = recog_result.text
                    return recog_result.text
                # No speech was recognized
                elif recog_result.reason == ResultReason.NoMatch:
                    print("No speech could be recognized: {}".format(recog_result.no_match_details))
                    return False
                # cancel the voice
                elif recog_result.reason == ResultReason.Canceled:
                    cancellation_details = recog_result.cancellation_details
                    print("Speech Recognition canceled: {}".format(cancellation_details.reason))
                    if cancellation_details.reason == speechsdk.CancellationReason.Error:
                        print("Error details: {}".format(cancellation_details.error_details))
                    return False
            except EOFError:
                break
    # Text-to-Speech - VUI Response
    def text_to_speech(self, text):
        """
        Convert conversation on-going and output to default speaker.
        """	
        try:
            result = self.speech_synthesizer.speak_text_async(text).get() #outputing the text to speaker
            
            # Case 1: Audio ready to outputted
            if result.reason == ResultReason.SynthesizingAudioCompleted:
                print("Speech synthesized for text [{}]".format(text))
                self.voice_response = result
            else:
                print(f"Error synthesizing audio: {result}")
        except Exception as ex:
            print(f"Error synthesizing audio: {ex}")
    
    def display_image(self, image_path):
        """
        Display image of the painting.
        """
        try:
            print(f"Displaying image: {image_path}")
            image = Image(url=image_path)
            display(image)
        except Exception as err:
            print(f"Error displaying image: {err}")
    
    def get_oai_response(self, context=context, user_input="", prompt_path="../prompts/basic.prompty", image_path=image_path, conversation_history=[]):
        """
        Function that get the response from the OpenAI model.
        using the custom prompt. 
        Giving the context, question, image and conversation history.
        """
        
        flow = Prompty.load(prompt_path) #"../prompts/basic.prompty"
        oai_response = flow(
            firstName = self.username,
            context = context,
            question = user_input,
            image = image_path,
            conversation_history = conversation_history
        )
        # self.voice_response = oai_response
        print(f"OpenAI response: {oai_response}")
        return oai_response

    def activate(self):
        """
        Activate the VUI.
        """
        activate_input = self.speech_to_text()
        if activate_input == VoiceCommand.Start:
            # self.text_to_speech(VoiceCommand.AgentGreeting)
            return True
        else:
            return False
    def deactivate(self):
        """
        Deactivate the VUI.
        """
        deactivate_input = self.speech_to_text()
        if deactivate_input == VoiceCommand.Stop:
            # self.text_to_speech(VoiceCommand.AgentGoodbye)
            return False
        else:
            return True




