paintings_mapping = {
    "king": "King Caspar",
    "boy": "Head of a Boy in a Turban",
    "dom": "Portrait of Dona Isabel de Porcel",
    "pedro": "Portrait of Pedro de Alvarado",
}
artifacts_mapping = {
    "pot": "Incense Pot",
    "golden": "Golden Accessories",
    "doublet": "The Doublet",
    "turban": "The Turban",
    "white": "The white orstrich feather",
    "blue garment": "The blue garment",
    "red": "The red ostrich feather",
    "hat": "The cavalier hat",
    "gilt garment": "The gilt garment",
    "ivory": "The ivory tusk"
}
topic_mapping = {
    "style": "style",
    "story": "story",
    "artifact": "artifact"
}

def match_painting_name(user_input):
    """
    Match the user input with the list of key in the painting name mapping.
    """
    print("Painting name to match: ", user_input)
    for name in paintings_mapping.keys():
        if name in user_input:
            return paintings_mapping[name] # return the full name
    return ""

def match_artifact_name(user_input):
    """
    Match the user input with the list of key in the artifact name mapping.
    """
    for name in artifacts_mapping.keys():
        if name in user_input:
            return artifacts_mapping[name] # return the full name
    return ""

def match_topic(user_input):
    """
    Match the user input with the list of key in the topic mapping.
    """
    for topic in topic_mapping.keys():
        if topic in user_input:
            return topic_mapping[topic] # return the full name
    return ""

# def confirm_painting(agent, user_input, painting_name=""):
#     """
#     Confirm the paintings in the list
#     """
#     # Agent confirm the painting name
#     agent.text_to_speech(f"Got it! You want to know about the painting \"{user_input}\". Is that correct?")

#     # User confirm the painting name
#     user_input = agent.speech_to_text().lower()

#     if VoiceCommand.No.value in user_input:
#         agent.text_to_speech(VoiceCommand.AgentPaintingAnother.value)
#         user_input = agent.speech_to_text().lower() #
#         return False, painting_name
#     elif VoiceCommand.Yes.value in user_input:
        
#         # check if any painting name in the list of painting names is in the user input
#         for name in painting_names:
#             if name in user_input:
#                 agent.text_to_speech(f"Perfect! I found the painting name: {name}. Let's discuss about it.")
#                 return True, name
#         return False, painting_name
#     else:
#         agent.text_to_speech(VoiceCommand.AgentPaintingError.value)
#         continue


