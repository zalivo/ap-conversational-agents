import time
import os
import sys
import requests
import json

#import resource
# import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer,SpeechRecognizer, AudioConfig, ResultReason
from azure.cognitiveservices.speech.audio import AudioOutputConfig
from openai import AzureOpenAI

from promptflow.core import Prompty
from IPython.display import Image, display # for displaying images of paintings

#dotenv
from dotenv import load_dotenv
load_dotenv('.env')

# internal imports
# from content_handling import ContentHandler
from modules.knowledge import PaintingsKnowledge
from modules.voice_command import VoiceCommand
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

        self._user_input = None
        self.voice_response = None
        self._username = for_user
        self.context = ""
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
                    self._user_input = recog_result.text
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
            
            return result
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
    
    def get_oai_response(self, 
        context="", 
        user_input="", 
        prompt_path="prompts/basic.prompty", 
        image_path="", 
        # topic="", 
        conversation_history=[]):
        """
        Function that get the response from the OpenAI model.
        using the custom prompt. 
        Giving the context, question, image and conversation history.
        """
        print("Getting OpenAI response...")
        print(f"Prompt Path: {prompt_path} and Image Path: {image_path}")
        print(f"Context: {context}, User Input: {user_input}")
        print("-----------------------------------")
        try: 
            flow = Prompty.load(prompt_path) #"../prompts/basic.prompty"
            oai_response = flow(
                firstName = self._username,
                context = context,
                question = user_input,
                image = image_path,
                # topic = topic,
                conversation_history = conversation_history
            )
            # self.voice_response = oai_response
            print(f"OpenAI response: {oai_response}")
            return oai_response
        except Exception as ex:
            print(f"Error getting OpenAI response: {ex}")
            
    def activate(self):
        """
        Activate the VUI.
        """
        activate_input = self.speech_to_text()
        print(f"User Activate Input: {activate_input}")
        if VoiceCommand.Start.value in activate_input:
            self.text_to_speech(VoiceCommand.AgentGreeting.value)
            return True
        else:
            self.text_to_speech(VoiceCommand.AgentSorry.value)
            return False
    def deactivate(self):
        """
        Deactivate the VUI.
        """
        deactivate_input = self.speech_to_text()
        if VoiceCommand.End.value in deactivate_input:
            # self.text_to_speech(VoiceCommand.AgentGoodbye.value)
            return True
        else:
            return False
    def next_topic(self, next_input):
        """
        Next topic of the conversation.
        """
        # next_input = self.speech_to_text()
        if VoiceCommand.Next.value in next_input:
            return True
        else:
            return False
    
    def stop_topic(self, stop_input):
        """
        Stop the current topic of the dialog.
        """
        # stop_input = self.speech_to_text()
        if VoiceCommand.Stop.value in stop_input:
            return True
        else:
            return False




