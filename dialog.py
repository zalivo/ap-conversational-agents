from modules.voice_command import VoiceCommand 
from modules.vrcui_speech import VRisper
from modules.content_handling import get_all_info, painting_handler, ask_painting

agent = VRisper(for_user="Thomas")
# kg = PaintingsKnowledge(
#     uri=os.getenv('NEO4J_URI'), 
#     user=os.getenv('NEO4J_USER'), 
#     password=os.getenv('NEO4J_PASSWORD')
# )

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

    if not ongoing_conversation:
        print("User ended the conversation from dialog function...")
        return
    
    while ongoing_conversation:

        if current_painting == "":
            agent.text_to_speech(VoiceCommand.AgentPainting.value)
        else:
            agent.text_to_speech(f"We are discussing about the painting: {current_painting}. Do you want to continue? If not, say 'goodbye'.")
            ongoing_conversation = agent.deactivate() #deactivate the conversation

        # if not ongoing_conversation:
        #     # ongoing_conversation = False
        #     conversation_history = [] #clear the conversation history
        #     agent.text_to_speech(VoiceCommand.AgentGoodbye.value)
        #     return
        
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
            conversation_enabled = ongoing_conversation,
            current_painting=current_painting,
            context=context, 
            img_path=img_path, 
            user_input=user_input,
            # topic = topic,
            dialog_history=conversation_history
        )

        # ongoing = False
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
        if VoiceCommand.Summary.value in response:
            print("<----Summary the current topic---->")
            ongoing_dialog = True
            continue
        elif VoiceCommand.NextTopic.value in response:
            print("<----Next topic---->")
            ongoing_dialog = False
            return
        elif VoiceCommand.Stop.value in response:
            print("<----Stop the current conversation---->")
            ongoing_dialog = False
            return
        elif VoiceCommand.NextPainting.value in response:
            print("<----Next painting---->")
            dialog_history = [] #clear the conversation history
            current_painting = ""
            return
        elif VoiceCommand.End.value in response:
            print("<----Ending the conversation---->")
            conversation_enabled = False
            return


    # dialog(user_input)

#----------------------------------Main-----------------------------------

if __name__ == "__main__":
    conversation()