from modules.voice_command import VoiceCommand 
from modules.vrcui_speech import VRisper
from modules.knowledge import PaintingsKnowledge
from modules.content_handling import ask_painting, ask_topic, ask_summary, ask_artifact
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


    current_painting = ""
    conversation_history = [] #conversation history

    
    while ongoing_conversation:

        if current_painting == "":
            agent.text_to_speech(VoiceCommand.AgentPainting.value)
        else:
            agent.text_to_speech(f"We are discussing about the painting: {current_painting}. Do you want to continue? If not, say 'goodbye'.")
            ongoing_conversation = agent.deactivate() #deactivate the conversation

        if not ongoing_conversation:
            # ongoing_conversation = False
            conversation_history = [] #clear the conversation history
            agent.text_to_speech(VoiceCommand.AgentGoodbye.value)
            return
        
        # Started: "Which painting would you like to know about?"
        # Ask painting success -> continue to dialog
        # Ask painting failed -> repeat the question
        user_input = agent.speech_to_text()
        print("User input conversation: ", user_input)

        # agent.text_to_speech(VoiceCommand.AgentPainting.value)

        painting_name = ask_painting(agent, user_input=user_input) #handle painting name
        current_painting = painting_name
        print("Current Painting: ", current_painting)

        discussed_topic = ask_topic(agent) #find the topic
        current_topic = discussed_topic
        print("Current Topic: ", current_topic)

        
        context, img_path, user_input, topic, artifacts = topic_handler(user_input, painting_name, current_topic) #handle user input based on topics

        print(f"Topic: {topic}, Normal Context: [{context}]")

        if topic == "artifact":
            print("Handling Artifact in conversation...")

            print(f"List of Artifacts from the painting: {artifacts}")

            artifact_context = artifact_handler(painting_name=current_painting,painting_artifacts=artifacts)
            if artifact_context == None:
                break
            else:
                print(f"Artifact Context: [{artifact_context}]")
                context = context + artifact_context
                continue
        print(f"Final Context: [{context}]")
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
    print("Start new dialog...")
    ongoing_dialog = True   
    current_topic = topic
    
    agent.text_to_speech(f"We are discussing about the {current_topic} of the painting.")
    agent.text_to_speech(VoiceCommand.AgentBridge.value) # asking to discuss
    
    # FIXME: WHERE TO ADD THE USER INPUT - HERE?

    while ongoing_dialog:
        #FIXME: OR HERE?
        user_input = agent.speech_to_text()
        print("[User input specific info relate to topic]: ", user_input)
        
        is_next_topic = agent.next_topic(user_input) #next topic
        is_stop = agent.stop_topic(user_input) #stop the conversation

        if is_next_topic:
            agent.text_to_speech(VoiceCommand.AgentTopic.value)
            new_topic = ask_topic()
            context, img_path, user_input, topic = topic_handler(user_input, current_painting, new_topic)
            dialog_history = [] # clear the dialog history
            dialog(context, img_path, user_input, topic, dialog_history)
            return
        elif is_stop:
            agent.text_to_speech(VoiceCommand.AgentStop.value)
            ongoing_dialog = False
            current_topic = ""
            return

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

# -----------------------------------------------------Specific Handlers for user voice input -----------------------------------
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

    # command = user_input.lower()
    # print("User requested topic: ", command)

    if current_topic == "story":
        print("Handling Painting Story in topic handler...")
        # current_topic = "story"
        context = f"Painting Name: {name}, Description: {description}, Artist: {artist}"
    elif current_topic == "style":
        print("Handling Painting Style in topic handler...")
        # current_topic = "style"
        context = f"Painting Name: {name}, Style: {style}, Artist: {artist}"
    elif current_topic == "artifact":
        print("Handling Painting Artifacts in topic handler...")
        # current_topic = "artifact"
        context = f"Painting Name: {name}, Artifacts: {artifacts}"

    else:
        # any user input that doesn't match the above cases
        print("Handling other topic in topic handler...")
        agent.text_to_speech(VoiceCommand.AgentTopicError.value)
        agent.text_to_speech(VoiceCommand.AgentTopicFollowUp.value)
        context = f"Painting Name: {name}, Description: {description}, Style: {style}, Artist: {artist}, Artifacts: {artifacts}"

    return context, img_path, user_input, current_topic, artifacts

def artifact_handler(painting_name, painting_artifacts):
    """
    Handling user input for artifacts
    """
    if len(painting_artifacts) == 0:
        agent.text_to_speech(f"Sorry, I couldn't find any artifacts from this painting: {painting_name}.")
        return
    else: 
        agent.text_to_speech(f"Here are the artifacts I found from the painting: \"{painting_name}\"")
        for artifact in painting_artifacts:
            agent.text_to_speech(f"Artifact: {artifact['a.name']}")

    artifact_name = ask_artifact(agent) #ask user about artifact
    
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
    - Start, 
    - Stop, 
    - End, 
    - Next
    - Repeat,
    - Summary
    """
    if VoiceCommand.End.value in user_input:
        print("----User saying goodbye----")
        return "goodbye"
    
    elif VoiceCommand.Stop.value in user_input:
        print("----User stop the conversation----")
        return "stop"
    
    elif VoiceCommand.Topic.value in user_input:
        print("----User want to discuss another topic----")
        return "next"
    
    elif VoiceCommand.Repeat.value in user_input:
        return "repeat"

    elif VoiceCommand.Summary.value in user_input:
        return "summary"

    else:
        return ""



#----------------------------------Main-----------------------------------

if __name__ == "__main__":
    conversation()