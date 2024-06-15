# from modules.content_handling import ContentHandling
from modules.voice_command import VoiceCommand 
from modules.vrcui_speech import VRisper
from modules.knowledge import PaintingsKnowledge
from utils.functions import match_painting_name, match_artifact_name, match_topic
import os
from dotenv import load_dotenv
load_dotenv('.env')


agent = VRisper(for_user="Thomas")
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

# painting_names = [p['p.name'] for p in paintings]
# print("Painting Names: ", painting_names)

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
        agent.text_to_speech(VoiceCommand.AgentGuide.value)
        #add command to history
        command_history.append(VoiceCommand.AgentGuide.name)

    # 1. Initial User input
    agent.text_to_speech(VoiceCommand.AgentBridge.value) #"What would you like to know?"
    user_input = agent.speech_to_text().lower() #user input, can be any topics

    # STOP conversation: "End" or "Goodbye"	
    if VoiceCommand.End.value in user_input:
        print("User saying goodbye")
        agent.text_to_speech(VoiceCommand.AgentGoodbye.value)
        ongoing_conversation = False
        return

    current_topic = match_topic(user_input) #match topic
    print("Current Topic by user: ", current_topic)

    while ongoing_conversation:

        # Started: "Which painting would you like to know about?"
        agent.text_to_speech(VoiceCommand.AgentPainting.value) 
        
        user_input = agent.speech_to_text().lower() #Expected the painting name
        print(f"User input painting name:{user_input}")

        painting_name = match_painting_name(user_input) #match painting name

        if painting_name == "":
            agent.text_to_speech(VoiceCommand.AgentPaintingError.value)
            # continue
            ongoing_conversation = False
            return #FIXME: conversation still going on without interruption
        else:
            print("Painting Name: ", painting_name)
            agent.text_to_speech(f"Great! Let's discuss about the painting: {painting_name}.")
            if current_topic == "":
                agent.text_to_speech(VoiceCommand.AgentBridge.value) #"What would you like to know?"
            else:
                agent.text_to_speech(f"Any specific things relate to the topic {current_topic} you want to know about?")

        # 2. User input specific topic
        user_input = agent.speech_to_text() #user topic
        print("User input: ", user_input)

        context, img_path, user_input, topic = topic_handler(user_input, painting_name, current_topic) #handle user input based on topics
        dialog(
            context=context, 
            img_path=img_path, 
            user_input=user_input,
            topic = topic
        )
        # ongoing = False
    # conversation()

def dialog(context="", img_path="",user_input="", topic="story"):
    """
    Dialog between user and agent
    """
    ongoing_dialog = True
    while ongoing_dialog:
        user_input = agent.speech_to_text()
        if VoiceCommand.Stop.value in user_input or VoiceCommand.End.value in user_input:
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
        conversation_history.append(
            f'''
            User: {user_input}
            Assistant: {response}
            '''
        )
        agent.text_to_speech(response)
    # dialog(user_input)

def topic_handler(user_input, painting_name, current_topic=""):
    """
    Handling multiple user inputs content based on topics:
    - Painting Style
    - Painting Story
    - Painting Artifacts
    """
    context = ""
    painting_info = kg.get_specific_painting(painting_name)[0]
    # artifacts = kg.get_artifacts_by_painting(painting_name) #list of artifacts

    #Painting information given by painting names
    print("Painting Info: ", painting_info)

    #Parse painting information to gpt
    name, description, style, artist, img_path, artifacts = painting_info['p.name'], painting_info['p.description'], painting_info['p.style'], painting_info['p.artist'], painting_info['p.img'], painting_info['p.artifacts']

    command = user_input.lower()
    print("User requested topic: ", command)

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
    agent.text_to_speech(f"I'm intrigued, what do you see from the painting. Are there any special thing about its {current_topic} interest you?")

    # TODO: Add the handling cases for specific artifacts in the case topic = "artifact"
    
    # dialog(
    #     context=context, 
    #     img_path=img_path, 
    #     user_input=user_input,
    #     topic = current_topic
    # )
    return context, img_path, user_input, current_topic

def artifact_handler(user_input, painting_name, artifacts):
    pass



if __name__ == "__main__":
    conversation()