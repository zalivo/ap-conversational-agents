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

#KG information
paintings = kg.get_all_paintings()
artifacts = kg.get_all_artifacts()

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
    # agent.text_to_speech(VoiceCommand.AgentBridge.value) #"What would you like to know?"
    # user_input = agent.speech_to_text().lower() #user input, can be any topics

    # # # STOP conversation: "End" or "Goodbye"	
    # # if VoiceCommand.End.value in user_input:
    # #     print("User saying goodbye")
    # #     agent.text_to_speech(VoiceCommand.AgentGoodbye.value)
    # #     ongoing_conversation = False
    # #     return

    # current_topic = match_topic(user_input) #match topic
    # print("Current Topic by user: ", current_topic)

    current_painting = ""

    while ongoing_conversation:

        conversation_history = [] #conversation history
        
        if command_handler(user_input) == "goodbye":
            ongoing_conversation = False
            conversation_history = []
            return
        
        # Started: "Which painting would you like to know about?"
        agent.text_to_speech(VoiceCommand.AgentPainting.value)

        painting_name = ask_painting() #handle painting name
        current_painting = painting_name
        print("Current Painting: ", current_painting)

        discussed_topic = ask_topic() #find the topic
        current_topic = discussed_topic
        print("Current Topic: ", current_topic)


        context, img_path, user_input, topic = topic_handler(user_input, painting_name, current_topic) #handle user input based on topics
        
        if topic == "artifact":
            artifact_context = artifact_handler(painting_name)
            context = context + artifact_context
            continue

        dialog(
            context=context, 
            img_path=img_path, 
            user_input=user_input,
            topic = topic,
            dialog_history=conversation_history
        )
        # ongoing = False
    # conversation()

def dialog(context="", img_path="",user_input="", topic="", dialog_history=[]):
    """
    Dialog between user and agent
    """
    current_topic = topic
    ongoing_dialog = True
    while ongoing_dialog:
        user_input = agent.speech_to_text()
        print("User input: ", user_input)

        if command_handler(user_input) == "stop":
            ongoing_dialog = False
            current_topic = ""
            return
        
        if command_handler(user_input) == "next":
            new_topic = ask_topic()
            context, img_path, user_input, topic = topic_handler(user_input, current_painting, new_topic)
            dialog_history = [] # clear the dialog history

        response = agent.get_oai_response(
            context=context,
            user_input=user_input,
            image_path=img_path,
            topic=topic,
            conversation_history=dialog_history
        )
        dialog_history.append(
            f'''
            User: {user_input}
            Assistant: {response}
            '''
        )
        agent.text_to_speech(response)
    # dialog(user_input)

# Specific Handlers for user voice input -----------------------------------
def ask_painting():
    """
    Agent ask for the painting anme and handling user input
    This is the internal loop of the dialog, terminated when the painting name is found
    """
    found_painting = False
    painting_name = ""
    while not found_painting:
        agent.text_to_speech(VoiceCommand.AgentPaintingAnother.value) #Can you repeated the painting name?
        user_input = agent.speech_to_text().lower() #painting name
        print(f"User input painting name:{user_input}")
        painting_name = match_painting_name(user_input) #match painting name
        
        if painting_name == "":
            agent.text_to_speech(VoiceCommand.AgentPaintingError.value)
            continue #FIXME: conversation still going on without interruption
        else:
            print("Painting Name: ", painting_name)
            agent.text_to_speech(f"Great! Let's discuss about the painting: {painting_name}.")
            found_painting = True
    return painting_name

def ask_topic():
    """
    Agent ask for the topic and handling user input
    This is the internal loop of the dialog, terminated when the topic is found
    """
    found_topic = False
    topic = None
    while not found_topic:
        agent.text_to_speech(VoiceCommand.AgentTopic.value) #Can you repeated the painting name?
        user_input = agent.speech_to_text().lower() #painting name
        print(f"User input topic:{user_input}")
        topic = match_topic(user_input) #match painting name

        if topic == None:
            agent.text_to_speech(VoiceCommand.AgentTopicError.value)
            continue #FIXME: conversation still going on without interruption
        else:
            print("Topic: ", topic)
            # agent.text_to_speech(f"Great! Let's discuss about the painting: {topic}.")
            found_topic = True
    return topic

def topic_handler(user_input, painting_name, current_topic=""):
    """
    Handling multiple user inputs content based on topics:
    - Painting Style
    - Painting Story
    - Painting Artifacts
    """
    context = ""
    painting_info = kg.get_specific_painting(painting_name)[0]

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

    return context, img_path, user_input, current_topic

def artifact_handler(painting_name):
    """
    Handling user input for artifacts
    """
    # Agent LIST all artifacts from the painting
    painting_artifacts = kg.get_artifacts_by_painting(painting_name)
    print("Painting Artifacts from graph: ", painting_artifacts)
    
    agent.text_to_speech(f"Here are the artifacts I found from the painting: {painting_name}")

    for artifact in painting_artifacts:
        agent.text_to_speech(f"Artifact: {artifact['a.name']}")
    
    # asking user about artifact
    agent.text_to_speech(VoiceCommand.AgentArtifact.value) #what artifact would you like to know?
    
    user_input = agent.speech_to_text().lower() #expected artifact name
    print("User input artifact name: ", user_input)

    artifact_name = match_artifact_name(user_input) #match artifact name

    if artifact_name == "":
        agent.text_to_speech(VoiceCommand.AgentTopicError.value)
        return
    else:
        print("Found Artifact Name: ", artifact_name)
        artifact_info = kg.get_specific_artifact(artifact_name)[0]

        if artifact_info == "":
            agent.text_to_speech(f"Sorry, I couldn't find the information about this artifact: {artifact_name}.")
            return
    
    agent.text_to_speech(f"Great! I found the information about the artifact: {artifact_name} of this painting. Let's discuss about it.")
    agent.text_to_speech(f"What is your interest about this {artifact_name} artifact? Any thing from this artifact intrigued you? ")
    
    artifact_context = f"Artifact Name: {artifact_info['a.name']}, Description: {artifact_info['a.description']}"

    return artifact_context

def command_handler(user_input):
    """
    Command handler for user input - Using for handling specific user command:
    - Start, Stop, End, Next
    """
    if VoiceCommand.End.value in user_input:
        print("User saying goodbye")
        agent.text_to_speech(VoiceCommand.AgentGoodbye.value)
        return "goodbye"
    
    elif VoiceCommand.Stop.value in user_input:
        print("User stop the conversation")
        agent.text_to_speech(VoiceCommand.AgentStop.value)
        return "stop"
    
    elif VoiceCommand.Topic.value in user_input:
        print("User want to discuss another topic")
        agent.text_to_speech(VoiceCommand.AgentTopic.value)
        return "next"
    else:
        return ""



#----------------------------------Main-----------------------------------

if __name__ == "__main__":
    conversation()