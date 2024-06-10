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

painting_names = [p['p.name'].lower() for p in paintings]
print("Painting Names: ", painting_names)

def conversation():
    """
    Entire Conversation, including multiple dialog from user and agent
    """
    activated = agent.activate() #activate "Hi Lisa."
    print("Activated: ", activated)
    ongoing = True

    if not activated:
        # not doing anything if not activated
        conversation()
        return
    # Only activate after Hi, Lisa.
    while ongoing:

        # intialise conversation, check if the command already exist
        if VoiceCommand.AgentGuide.name not in command_history:
            agent_response = agent.text_to_speech(VoiceCommand.AgentGuide.value)
            print(f"Initial Agent Guide: {agent_response}")
            #add command to history
            command_history.append(VoiceCommand.AgentGuide.name)

        # Started: "Which painting would you like to know about?"
        agent.text_to_speech(VoiceCommand.AgentPainting.value) 
        
        user_input = agent.speech_to_text().lower() #Expected the paiting name
        print(f"First user input in loop:{user_input}")
        if VoiceCommand.Stop.value in user_input or VoiceCommand.End.value in user_input:
            agent.text_to_speech(VoiceCommand.AgentGoodbye.value)
            # deactivating the agent
            ongoing = False
            return

        # #TODO: user input painting name
        # painting_name = agent.speech_to_text() 
        # print("User input painting name: ", painting_name)
        

        # check if any painting name in the list of painting names is in the user input
        # FIXME: Check by matching or checking subsequence instead of exact match
        painting_name = ""
        painting_name = "head of a boy in a turban"
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
            agent.text_to_speech(f"Great! Let's discuss about the painting {painting_name}. Is there anything specific topic you would like to know?")
            # 2. User input specific topic
            user_input = agent.speech_to_text() #user topic
            print("User input: ", user_input)
            context, img_path, topic = handling_topic(user_input, painting_name) #handle user input based on topics

            agent.text_to_speech(f"Great! Let's discuss about {topic}")

            dialog(
                context=context,
                img_path=img_path,
                # user_input=user_input #FIXME: included or not?
            )
    conversation()
        

def dialog(context="", img_path="",user_input=""):
    """
    Dialog between user and agent
    """
    user_input = agent.speech_to_text()
    print("User: ", user_input)
    response = agent.get_oai_response(
        context=context,
        user_input=user_input,
        image_path=img_path,
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

    if VoiceCommand.Stop.value in user_input:
        agent.text_to_speech(VoiceCommand.AgentGoodbye.value)
        return
    dialog(user_input)

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

    if VoiceCommand.PaintingInfo.value in user_input:
        current_topic = VoiceCommand.PaintingInfo.value
        context = f"Painting Name: {name}, Description: {description}, Artist: {artist}"
        pass
    elif VoiceCommand.PaintingStyle.value in user_input:
        current_topic = VoiceCommand.PaintingStyle.value
        context = f"Painting Name: {name}, Style: {style}"
        pass
    elif VoiceCommand.PaintingColor.value in user_input:
        current_topic = VoiceCommand.PaintingColor.value
        context = f"Style: {style}, Artist: {artist}"
        #FIXME: Added additional prompt?
        pass
    elif VoiceCommand.PaintingStory.value in user_input:
        current_topic = VoiceCommand.PaintingStory.value
        context = f"Painting Name: {name}, Description: {description}"
        pass
    elif VoiceCommand.PaintingArtifact.value in user_input:
        current_topic = VoiceCommand.PaintingArtifact.value
        context = f"Painting Name: {name}, Description: {description}, Artifacts: {artifacts}"
        pass
    else:
        # any user input that doesn't match the above cases
        agent.text_to_speech(VoiceCommand.AgentPainting.value) # asking to discuss
        context = f"Painting Name: {name}, Description: {description}, Style: {style}, Artist: {artist}, Artifacts: {artifacts}"
    return context, img_path, current_topic
if __name__ == "__main__":
    conversation()