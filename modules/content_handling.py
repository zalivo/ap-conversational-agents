from modules.voice_command import VoiceCommand
from utils.functions import match_painting_name, match_topic
from modules.knowledge import PaintingsKnowledge
import os
from dotenv import load_dotenv

load_dotenv('.env')

kg = PaintingsKnowledge(
    uri=os.getenv('NEO4J_URI'), 
    user=os.getenv('NEO4J_USER'), 
    password=os.getenv('NEO4J_PASSWORD')
)

# def get_all_info(painting_name):
#     """
#     Get all information about the painting including the full information of the artifacts
#     by getting each artifact information by artifact name
#     """
#     all_info = {}
#     painting_info = kg.get_specific_painting(painting_name)[0]
    
#     for key, value in painting_info.items():
#         all_info[key] = value
#         if key == "p.artifacts":
#             #list of artifacts name
#             # all_info['p.artifacts'] = {
#             #     "artifact1_name": "artifact1_description",
#             #     "artifact2_name": "artifact2_description",
#             #     ...
#             # }
#             for artifact_name in value:
#                 artifact_info = kg.get_specific_artifact(artifact_name)[0]
#                 print("Artifact Info: ", artifact_info)
#                 # restructuring the artifacts information
#                 all_info['p.artifacts'][artifact_info['a.name']] = artifact_info['a.description'] 

#     print(f"All Info of the painting {painting_name}: {all_info}")

#     return all_info

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

def response_handler(agent, response):
    """
    Handle the special response token from the agent
    so it can trigger the agent to do the specific action
    """
    action_enabled = False

    if VoiceCommand.Stop.value in response:
        
        return 

def ask_painting(agent, user_input):
    """
    Agent ask for the painting anme and handling user input
    This is the internal loop of the dialog, terminated when the painting name is found
    """
    found_painting = False
    painting_name = ""
    while not found_painting:
        # user_input = agent.speech_to_text()#painting name
        print(f"[User]:{user_input}")
        painting_name = match_painting_name(user_input.lower()) #match painting name
        
        if painting_name == "":
            agent.text_to_speech(VoiceCommand.AgentPaintingError.value)
            agent.text_to_speech(VoiceCommand.AgentPaintingAnother.value) #Can you repeated the painting name?
            found_painting = False
            
            user_input = agent.speech_to_text()#painting name
            continue
        else:
            # print("Painting Name: ", painting_name)
            agent.text_to_speech(f"Great! Let's discuss about the painting: {painting_name}.")
            found_painting = True
            break
        
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