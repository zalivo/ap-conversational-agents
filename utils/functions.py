paintings_mapping = {
    "king": "King Caspar",
    "boy": "Head of a Boy in a Turban",
    "castro": "Portrait of Dom Miguel de Castro",
    "pedro": "Portrait of Pedro Sunda",
    "diego": "Portrait of Diego Bamba",
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

