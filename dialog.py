# from modules.content_handling import ContentHandling
from modules.voice_command import VoiceCommand 
from modules.vrcui_speech import VRisper
from modules.knowledge_connection import PaintingsKnowledge

import os
from dotenv import load_dotenv
load_dotenv('.env')


agent = VRisper(for_user="John")
kg = PaintingsKnowledge(
    uri=os.getenv('NEO4J_URI'), 
    user=os.getenv('NEO4J_USER'), 
    password=os.getenv('NEO4J_PASSWORD')
)

conversation_history = [] #conversation history
topics = [] #conversation topics
paintings = kg.get_all_paintings()
artifacts = kg.get_all_artifacts()

painting_names = [p['name'] for p in paintings]

def conversation():
    """
    Entire Conversation, including multiple dialog from user and agent
    """


    activated = agent.activate() #activate "Hi Vrisper"
    while activated:
        agent.text_to_speech(VoiceCommand.AgentGreeting) #"Hi there!"

        agent.text_to_speech(VoiceCommand.AgentPainting) # Asking about painting name
        
        #1. User giving painting name
        painting_name = agent.speech_to_text() #get user input from microphone
        print("User input painting name: ", painting_name)
        if painting_name not in kg.get_all_paintings():
            agent.text_to_speech(VoiceCommand.AgentPaintingError)
            continue
        painting_info = kg.get_specific_painting(painting_name)[0]
        print("Painting Info: ", painting_info)

        #Parse painting information to gpt
        name, description, style, artist, img, artifacts = painting_info['name'], painting_info['description'], painting_info['style'], painting_info['artist'], painting_info['img'], painting_info['artifacts']
        context = f"Painting Name: {name}, Description: {description}, Style: {style}, Artist: {artist}, Artifacts: {artifacts}"
        #Set content and topics
        agent.set_context(context)
        agent.set_topics(["Painting Style", "Painting Color", "Story", "Artifacts"])
        agent.set_user_input(painting_name)

        #2. Agent asking about specific topic
        agent.text_to_speech(VoiceCommand.AgentTopic)

        #3. User giving input (either related to topic or not)
        user_input = agent.speech_to_text()
        dialog(user_input)

        if user_input == VoiceCommand.End:
            agent.text_to_speech(VoiceCommand.AgentGoodbye)
            break

def dialog(user_input):
    """
    Dialog between user and agent
    """
    user_input = agent.speech_to_text() #get user input from microphone
    print("User: ", user_input)
    response = agent.get_oai_response(
        context=agent.context,
        user_input=user_input,
        conversation_history=conversation_history
    )
    print("Agent: ", response)
    conversation_history.append(
        f'''
        User: {user_input}
        Assistant: {response}
        '''
    )
    agent.text_to_speech(response)

    if user_input == VoiceCommand.Stop:
        agent.text_to_speech(VoiceCommand.AgentOk)
        return
    dialog(user_input)