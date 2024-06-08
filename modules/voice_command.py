from enum import Enum
class VoiceCommand(Enum):
    """
    Specific Voice Command moderate by 3 types: 
    - user input that trigger specific actions for the VUI.
    - content specific request for conversation
    - default agent speech 
    """
    Start = "Hi, Lisa."
    Stop = "Stop."
    End = "Ok. Goodbye."
    Topic = "Option"
    Info = "Info."

    #basic response
    No = "No."
    Yes = "Yes."
    Idk = "I don't know."

    #Painting related content
    PaintingInfo = "Painting info."
    PaintingArtifact = "Artifact."
    PaintingColor = "Color."
    PaintingStyle = "Style."
    PaintingStory = "Story."

    # Artifact related content
    ArtifactName= "Artifact name"
    ArtifactStory = "Story of artifact"

    #Default agent speech
    AgentGreeting = "Hi there! "
    AgentSorry = "Sorry, I don't understand. Can you repeat that?"
    AgentOk = "Ok."
    AgentGoodbye = "Goodbye!"
    AgentGuide = "I can help you with information about the painting or artifacts it have. These are something you can ask: \n- Painting Style \n- Painting Color \n- Story \n- Artifacts. \nWhat would you like to know?" 
    AgentPainting = "Great, let's discuss about it. Which painting would you like to know about?"
    # AgentTopic = "Here are some topics you might interest: Painting Style, Painting Color, Story, or Artifacts of the painting. Are there anything you would like to know?"
    # AgentHelp = "I can help you with information about the painting or artifacts it have. Is there anything specific you would like to know?"
    AgentPaintingError = "I'm sorry, I couldn't find the information about this painting. Is that the correct name?"
    AgentTopicError = "I'm sorry, I don't have information about this topic. Would you like to discuss about another topic?"

#--------------------------------------------------