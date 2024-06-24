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
        user_input = agent.speech_to_text()
        print("User input conversation: ", user_input)

        painting_name = ask_painting(agent, user_input=user_input) #handle painting name
        current_painting = painting_name
        print("Current Painting: ", current_painting)

        #FIXME: Directly get the painting information
        painting_info = get_all_info(painting_name)
        print("Painting Info: ", painting_info)

        # get the context and image for model
        context, img_path = painting_handler(painting_info)

        dialog(
            context=context, 
            img_path=img_path, 
            user_input=user_input,
            # topic = topic,
            dialog_history=conversation_history
        )

        # ongoing = False
    # conversation()

def dialog(context="", img_path="",user_input="", dialog_history=[]):
    """
    Dialog between user and agent
    """
    print("Start new dialog...")
    ongoing_dialog = True   
    # current_topic = topic
    
    # agent.text_to_speech(f"We are discussing about the {current_topic} of the painting.")
    agent.text_to_speech(VoiceCommand.AgentBridge.value) # asking to discuss

    while ongoing_dialog:
        # #FIXME: OR HERE?
        user_input = agent.speech_to_text()
        print("[User input to discuss]: ", user_input)

        response = agent.get_oai_response(
            context=context,
            user_input=user_input,
            image_path=img_path,
            # topic=topic,
            conversation_history=dialog_history
        )
        dialog_history.append(
            f'''
            User: {user_input}
            Assistant: {response}
            '''
        )
        agent.text_to_speech(response)
        if VoiceCommand.End.value in user_input:
            ongoing_dialog = False
            return
    # dialog(user_input)

# -----------------------------------------------------Specific Handlers for user voice input -----------------------------------
def painting_handler(painting_info):
    """
    Handle the painting information.
    Convert the information from KG into context and image path
    """

    context = f'''
    The painting is called "{painting_info['p.name']}". 
    It was created by {painting_info['p.artist']} in {painting_info['p.year']}.
    The painting style is {painting_info['p.style']}.
    The painting story is {painting_info['p.description']}. 
    And in the painting, it contains the following artifacts: {painting_info['p.artifacts']}
    '''
    img_path = painting_info['p.img']
    return context, img_path

def get_all_info(painting_name):
    """
    Get all information about the painting including the full information of the artifacts
    by getting each artifact information by artifact name
    """
    all_info = {}
    painting_info = kg.get_specific_painting(painting_name)[0]
    
    for key, value in painting_info.items():
        all_info[key] = value
        if key == "p.artifacts":
            #list of artifacts name
            # all_info['p.artifacts'] = {
            #     "artifact1_name": "artifact1_description",
            #     "artifact2_name": "artifact2_description",
            #     ...
            # }
            for artifact_name in value:
                artifact_info = kg.get_specific_artifact(artifact_name)[0]
                print("Artifact Info: ", artifact_info)
                # restructuring the artifacts information
                all_info['p.artifacts'][artifact_info['a.name']] = artifact_info['a.description'] 

    print(f"All Info of the painting {painting_name}: {all_info}")

    return all_info


#----------------------------------Main-----------------------------------

if __name__ == "__main__":
    conversation()