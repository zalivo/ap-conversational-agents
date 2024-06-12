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

#KG information
paintings = kg.get_all_paintings()
artifacts = kg.get_all_artifacts()

painting_names = [p['p.name'] for p in paintings]
print("Painting Names: ", painting_names)

def conversation():
    """
    Entire Conversation, including multiple dialog from user and agent
    """
    activated = agent.activate() #activate "Hi Lisa."
    print("Activated: ", activated)
    ongoing_conversation = True

    if not activated:
        # not doing anything if not activated
        conversation()
        return
    
    # intialise conversation
    if VoiceCommand.AgentGuide.name not in command_history:
        agent_response = agent.text_to_speech(VoiceCommand.AgentGuide.value)
        #add command to history
        command_history.append(VoiceCommand.AgentGuide.name)

    # 1. Initial User input
    agent.text_to_speech(VoiceCommand.AgentBridge.value) #"What would you like to know?"
    user_input = agent.speech_to_text().lower() #user input, can be any topics

    if VoiceCommand.Stop.value in user_input or VoiceCommand.End.value in user_input:
        print("User saying goodbye")
        agent.text_to_speech(VoiceCommand.AgentGoodbye.value)
        ongoing_conversation = False
        return

    while ongoing_conversation:

        # Started: "Which painting would you like to know about?"
        agent.text_to_speech(VoiceCommand.AgentPainting.value) 
        
        user_input = agent.speech_to_text().lower() #Expected the painting name
        print(f"User input painting name:{user_input}")

        painting_name = ""

        found_painting = False
        while not found_painting:
            found_painting, painting_name = confirm_painting(user_input, painting_name)

        # check if any painting name in the list of painting names is in the user input
        # FIXME: Check by matching or checking subsequence instead of exact match
        # painting_name = ""
        # painting_name = "Head of a Boy in a Turban"
        for name in painting_names:
            if name in user_input:
                painting_name = name
                break
        print("Painting Name: ", painting_name)
        # wrong painting name, nothing will be explore
        if painting_name == "":
            agent.text_to_speech(VoiceCommand.AgentPaintingError.value)
            continue
        else:
            print("Painting Name: ", painting_name)
            agent.text_to_speech(f"Great! Let's discuss about the painting: {painting_name}. Is there anything specific topic you would like to know?")
            # 2. User input specific topic
            user_input = agent.speech_to_text() #user topic
            print("User input: ", user_input)
            handling_topic(user_input, painting_name) #handle user input based on topics
            ongoing = False
    conversation()
        

def dialog(context="", img_path="",user_input="", topic="story"):
    """
    Dialog between user and agent
    """
    ongoing_dialog = True
    while ongoing_dialog:
        user_input = agent.speech_to_text()
        if VoiceCommand.Stop.value in user_input:
            agent.text_to_speech(VoiceCommand.AgentGoodbye.value)
            ongoing_dialog = False
            return
        print("User: ", user_input)
        response = agent.get_oai_response(
            context=context,
            user_input=user_input,
            image_path=img_path,
            topic=topic,
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
    # dialog(user_input)

def handling_topic(user_input, painting_name):
    """
    Handling multiple user inputs content based on topics:
    - Painting Info
    - Painting Style
    - Painting Color
    - Painting Story
    - Painting Artifacts
    """
    current_topic = "" #TODO: Continuously keep track of the topic
    context = ""
    painting_info = kg.get_specific_painting(painting_name)[0]
    # artifacts = kg.get_artifacts_by_painting(painting_name) #list of artifacts

    #Painting information given by painting names
    print("Painting Info: ", painting_info)

    #Parse painting information to gpt
    name, description, style, artist, img_path, artifacts = painting_info['p.name'], painting_info['p.description'], painting_info['p.style'], painting_info['p.artist'], painting_info['p.img'], painting_info['p.artifacts']

    # context = f"Painting Name: {name}, Description: {description}, Style: {style}, Artist: {artist}, Artifacts: {artifacts}"
    command = user_input.lower()

    if VoiceCommand.PaintingInfo.value in command or VoiceCommand.PaintingStory.value in command:
        current_topic = "story"
        context = f"Painting Name: {name}, Description: {description}, Artist: {artist}"
    elif VoiceCommand.PaintingStyle.value in command:
        current_topic = "style"
        context = f"Painting Name: {name}, Style: {style}, Artist: {artist}"
    elif VoiceCommand.PaintingArtifact.value in command:
        current_topic = "artifact"
        context = f"Painting Name: {name}, Artifacts: {artifacts}"
    else:
        # any user input that doesn't match the above cases
        agent.text_to_speech(VoiceCommand.AgentBridge.value) # asking to discuss
        context = f"Painting Name: {name}, Description: {description}, Style: {style}, Artist: {artist}, Artifacts: {artifacts}"
    agent.text_to_speech(f"Great! Let's discuss about {current_topic}. What would you like to know about it?")
    
    dialog(
        context=context, 
        img_path=img_path, 
        user_input=user_input,
        topic = current_topic
    ) #FIXME: fix prompts, adjustable by  topics

def confirm_painting(user_input, painting_name=""):
    """
    Confirm the paintings in the list
    """
    # Agent confirm the painting name
    agent.text_to_speech(f"Got it! You want to know about the painting \"{user_input}\". Is that correct?")

    # User confirm the painting name
    user_input = agent.speech_to_text().lower()

    if VoiceCommand.No.value in user_input:
        agent.text_to_speech(VoiceCommand.AgentPaintingAnother.value)
        user_input = agent.speech_to_text().lower() #
        return False, painting_name
    elif VoiceCommand.Yes.value in user_input:
        
        # check if any painting name in the list of painting names is in the user input
        for name in painting_names:
            if name in user_input:
                agent.text_to_speech(f"Perfect! I found the painting name: {name}. Let's discuss about it.")
                return True, name
        return False, painting_name
    else:
        agent.text_to_speech(VoiceCommand.AgentPaintingError.value)
        continue
        
    # agent.text_to_speech("Here are the list of paintings: ")
    # for name in painting_names:
    #     agent.text_to_speech(name)
    # agent.text_to_speech("Which painting would you like to know about?")
    # user_input = agent.speech_to_text() #user input, can be any topics
    # print("User input: ", user_input)
    # handling_topic(user_input) #handle user input based on topics

if __name__ == "__main__":
    conversation()