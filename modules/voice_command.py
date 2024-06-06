class VoiceCommand(Enum):
    """
    Specific Voice Command moderate by 3 types: 
    - user input that trigger specific actions for the VUI.
    - content specific request for conversation
    - default agent speech 
    """
    Start = "Hi, Vrisper."
    Stop = "Stop."
    End = "Ok. Goodbye."
    Topic = "Option"
    Info = "Info."

    #basic response
    No = "No."
    Yes = "Yes."
    Idk = "I don't know."

    #Painting related content
    PaintingInfo = "Painting Info."
    PaintingArtifact = "Artifact."
    PaintingColor = "Color."
    PaintingStyle = "Style."
    PaintingStory = "Story."

    # Artifact related content
    ArtifactName= "Artifact name"
    ArtifactStory = "Story of artifact"

    #Default agent speech
    AgentGreeting = "Hi there! "
    AgentOk = "Ok."
    AgentGoodbye = "Goodbye!"
    AgentPainting = "I can help you with information about the painting or artifacts it have. Which painting would you like to know about?"
    AgentTopic = "Here are some topics you might interest: Painting Style, Painting Color, Story, or Artifacts of the painting. Are there anything you would like to know?"
    # AgentHelp = "I can help you with information about the painting or artifacts it have. Is there anything specific you would like to know?"
    AgentPaintingError = "I'm sorry, I couldn't find the information about this painting. Is that the correct name?"
    AgentTopicError = "I'm sorry, I don't have information about this topic. Would you like to discuss about another topic?"

#--------------------------------------------------