# from modules.content_handling import ContentHandling
from modules.voice_command import VoiceCommand 
from modules.vrcui_speech import VRisper
from modules.knowledge import PaintingsKnowledge

import os
from dotenv import load_dotenv
load_dotenv('.env')


agent = VRisper(for_user="John")
kg = PaintingsKnowledge(
    uri=os.getenv('NEO4J_URI'), 
    user=os.getenv('NEO4J_USER'), 
    password=os.getenv('NEO4J_PASSWORD')
)

command_history = [] #command history
conversation_history = [] #dialog history
topics = [] #conversation topics

#KG information
paintings = kg.get_all_paintings()
artifacts = kg.get_all_artifacts()

painting_names = [p['p.name'].lower() for p in paintings]
print("Painting Names: ", painting_names)

def conversation():
    """
    Entire Conversation, including multiple dialog from user and agent
    """
    activated = agent.activate() #activate "Hi Lisa."
    print("Activated: ", activated)

    # Only activate after Hi, Lisa.
    while activated:

        # intialise conversation, check if the command already exist
        if VoiceCommand.AgentGuide.name not in command_history:
            agent_response = agent.text_to_speech(VoiceCommand.AgentGuide.value)

            #add command to history
            command_history.append(VoiceCommand.AgentGuide.name)

        user_input = agent.speech_to_text() #get user input from microphone
        
        if user_input == VoiceCommand.Stop.value or user_input == VoiceCommand.End.value:
            agent.text_to_speech(VoiceCommand.AgentGoodbye.value)
            return

        #FIXME: Handling multiple user inputs content
        # if user_input == VoiceCommand.Topic.value:
        #     # agent.text_to_speech(VoiceCommand.AgentTopic.value)
        #     # user_input = agent.speech_to_text()
        #     continue
        # elif user_input == VoiceCommand.PaintingInfo.value:

        agent.text_to_speech(VoiceCommand.AgentPainting.value) # Asking about painting name
        
        #1. User giving painting name
        painting_name = agent.speech_to_text() #user input painting name
        print("User input painting name: ", painting_name)

        if painting_name.lower() not in painting_names:
            agent.text_to_speech(VoiceCommand.AgentPaintingError.value)
            continue

        painting_info = kg.get_specific_painting(painting_name)[0]
        print("Painting Info: ", painting_info)

        #Parse painting information to gpt
        name, description, style, artist, img_path, artifacts = painting_info['p.name'], painting_info['p.description'], painting_info['p.style'], painting_info['p.artist'], painting_info['p.img'], painting_info['p.artifacts']
        
        # TODO: Adjusting context correspoding to each use cases
        context = f"Painting Name: {name}, Description: {description}, Style: {style}, Artist: {artist}, Artifacts: {artifacts}"

        #2. Agent asking about specific topic
        agent.text_to_speech(VoiceCommand.AgentTopic.value)

        #3. User giving input (either related to topic or not)
        user_input = agent.speech_to_text()
        
        dialog(
            context=context,
            img_path=img_path,
            user_input=user_input
            )
        activated = agent.deactivate() #deactivate "Stop."
    conversation()
        

def dialog(context="", img_path="",user_input=""):
    """
    Dialog between user and agent
    """
    # user_input = agent.speech_to_text() #get user input from microphone
    print("User: ", user_input)
    response = agent.get_oai_response(
        context=context,
        user_input=user_input,
        image_path=img_path,
        conversation_history=conversation_history
    )
    print("Agent: ", response)
    #FIXME: Is this the dialog history or whole conversation history?
    conversation_history.append(
        f'''
        User: {user_input}
        Assistant: {response}
        '''
    )
    agent.text_to_speech(response)

    if user_input == VoiceCommand.Stop.value:
        agent.text_to_speech(VoiceCommand.AgentGoodbye.value)
        return
    dialog(user_input)

if __name__ == "__main__":
    conversation()