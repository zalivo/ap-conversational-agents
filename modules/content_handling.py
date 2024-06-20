from modules.voice_command import VoiceCommand
from utils.functions import match_painting_name, match_topic

def ask_painting(agent, user_input):
    """
    Agent ask for the painting anme and handling user input
    This is the internal loop of the dialog, terminated when the painting name is found
    """
    found_painting = False
    painting_name = ""
    while not found_painting:
        # user_input = agent.speech_to_text()#painting name
        print(f"User input painting name:{user_input}")
        painting_name = match_painting_name(user_input.lower()) #match painting name
        
        if painting_name == "":
            agent.text_to_speech(VoiceCommand.AgentPaintingError.value)
            agent.text_to_speech(VoiceCommand.AgentPaintingAnother.value) #Can you repeated the painting name?
            found_painting = False
            continue
        else:
            print("Painting Name: ", painting_name)
            agent.text_to_speech(f"Great! Let's discuss about the painting: {painting_name}.")
            found_painting = True
            break
        user_input = agent.speech_to_text()#painting name
    return painting_name

def ask_topic(agent):
    """
    Agent ask for the topic and handling user input
    This is the internal loop of the dialog, terminated when the topic is found
    """
    found_topic = False
    topic = None
    while not found_topic:
        agent.text_to_speech(VoiceCommand.AgentTopic.value) #Can you repeated the painting name?
        user_input = agent.speech_to_text()#painting name
        print(f"User input topic:{user_input}")
        topic = match_topic(user_input.lower()) #match painting name

        if topic == None:
            agent.text_to_speech(VoiceCommand.AgentTopicError.value)
            continue #FIXME: conversation still going on, asking about other topic
        else:
            print("Topic: ", topic)
            # agent.text_to_speech(f"Great! Let's discuss about the painting: {topic}.")
            found_topic = True
    return topic

def ask_summary(agent):
    """
    Agent summary the conversation when user asking about the dialog summary
    """
    pass

def ask_artifact(agent):
    """
    Agent ask for the artifact name and handling user input
    This is the internal loop of the dialog, terminated when the artifact name is found
    """
    found_artifact = False
    artifact_name = ""
        # asking user about artifact
    while not found_artifact:
        agent.text_to_speech(VoiceCommand.AgentArtifact.value) #what artifact would you like to know?
        
        user_input = agent.speech_to_text().lower() #expected artifact name
        print("User input artifact name: ", user_input)

        artifact_name = match_artifact_name(user_input) #match artifact name

        if artifact_name == "":
            agent.text_to_speech(VoiceCommand.AgentTopicError.value)
            return
        else:
            print("Found Artifact Name: ", artifact_name)
            agent.text_to_speech(f"I found the artifact: {artifact_name}.Let's discuss about it.")
            found_artifact = True
    return artifact_name