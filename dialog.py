from modules.voice_command import VoiceCommand 
from modules.vrcui_speech import VRisper
from modules.knowledge import PaintingsKnowledge
from modules.content_handling import painting_handler, ask_painting
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
        print(f"ONGOING CONVERSATION... {ongoing_conversation}")
        if current_painting == "":
            agent.text_to_speech(VoiceCommand.AgentPainting.value)
        # else:
        #     agent.text_to_speech(f"We are discussing about the painting: {current_painting}.")


        
        # Started: "Which painting would you like to know about?"
        user_input = agent.speech_to_text()
        print("User input conversation: ", user_input)

        painting_name = ask_painting(agent, user_input=user_input) #handle painting name
        current_painting = painting_name #assign the current painting with current painting name
        print("Current Painting: ", painting_name)
    

        #FIXME: Directly get the painting information
        painting_info = get_all_info(painting_name)
        print("Painting Info: ", painting_info)

        # get the context and image for model
        context, img_path = painting_handler(painting_info)

        current_painting, conversation_continue = dialog(
            conversation_enabled = ongoing_conversation,
            current_painting=painting_name,
            context=context, 
            img_path=img_path, 
            user_input=user_input,
            # topic = topic,
            dialog_history=conversation_history
        )

        print("Current Painting: ", current_painting)
        print("Conversation Continue?  ", conversation_continue)

        if current_painting == "goodbye" and not conversation_continue:
            print("----END OF CONVERSATION - GOODBYE----")
            ongoing_conversation = False
            return
        else:
            current_painting = ""
            conversation_history = []
            continue

    # conversation()

def dialog(
    conversation_enabled=True,
    current_painting="", 
    context="", 
    img_path="",
    user_input="", 
    dialog_history=[]):
    """
    Dialog between user and agent
    """
    print("Start new dialog...")

    ongoing_dialog = True  
    conversation_continue = True

    agent.text_to_speech(VoiceCommand.AgentBridge.value) # asking to discuss

    while ongoing_dialog:
        user_input = agent.speech_to_text()
        print("[User]: ", user_input)

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
        # print("[Sarah]: ", response)

        if VoiceCommand.Summary.value in response:
            print("<----Summary the current topic---->")
            response = response.replace(VoiceCommand.Summary.value, "")
            agent.text_to_speech(response)
            ongoing_dialog = True
            continue

        elif VoiceCommand.ConversationInfo.value in response:
            print("<----Conversation Info---->")
            response = response.replace(VoiceCommand.ConversationInfo.value, "")
            agent.text_to_speech(response)
            ongoing_dialog = True
            continue

        elif VoiceCommand.Stop.value in response:
            print("<----Stop the current conversation---->")
            response = response.replace(VoiceCommand.Stop.value, "")
            agent.text_to_speech(response)
            ongoing_dialog = False
            break

        elif VoiceCommand.NextPainting.value in response:
            print("<----Next painting---->")
            response = response.replace(VoiceCommand.NextPainting.value, "")
            agent.text_to_speech(response)
            dialog_history = [] #clear the conversation history
            current_painting = ""
            conversation_continue = True
            return current_painting, conversation_continue
        
        elif VoiceCommand.End.value in response:
            print("<----Ending the conversation---->")
            response = response.replace(VoiceCommand.End.value, "")
            agent.text_to_speech(response)
            current_painting = "goodbye"
            conversation_continue= False
            return current_painting, conversation_continue

        else:
            agent.text_to_speech(response)


    # dialog(user_input)
def get_all_info(painting_name):
    """
    Get all information about the painting including the full information of the artifacts
    by getting each artifact information by artifact name
    """
    all_info = {}
    painting_info = kg.get_specific_painting(painting_name)[0]
    # print("Painting Info: ", painting_info)
    for key, value in painting_info.items():
        all_info[key] = value
        if key == "p.artifacts":
            # all_info['p.artifacts'] = {
            #     "artifact1_name": "artifact1_description",
            #     "artifact2_name": "artifact2_description",
            #     ...
            # }
            all_info['p.artifacts'] = {}

            for artifact_name in value:
                artifact_info = kg.get_specific_artifact(artifact_name)[0]
                print("Artifact Info: ", artifact_info)
                all_info['p.artifacts'][artifact_info['a.name']] = artifact_info['a.description'] 

    # print(f"All Info of the painting {painting_name}: {all_info}")

    return all_info

#----------------------------------Main-----------------------------------

if __name__ == "__main__":
    conversation()