from enum import Enum
class VoiceCommand(Enum):
    """
    Specific Voice Command moderate by 3 types: 
    - user input that trigger specific actions for the VUI.
    - content specific request for conversation
    - default agent speech 
    """
    Start = "Hi, Lisa."
    Stop = "stop"
    End = "goodbye"
    Topic = "option"
    Info = "info"

    #basic response
    No = "No."
    Yes = "Yes."
    Idk = "I don't know."

    #Painting related content
    PaintingInfo = "information"
    PaintingArtifact = "artifact"
    PaintingColor = "color"
    PaintingStyle = "style"
    PaintingStory = "story"

    # Artifact related content
    ArtifactName= "artifact name"
    ArtifactInfo = "artifact information"

    #Default agent speech
    AgentGreeting = "Hi there! "
    AgentSorry = "Sorry, I don't understand. Can you repeat that?"
    AgentOk = "Ok."
    AgentGoodbye = "Great to talk to you. Goodbye!"
    AgentGuide = "I can help you with information about the painting or artifacts it have. These are something you can ask: \n- Painting story \n- Painting style \n - or Artifacts in the painting."
    AgentBridge = "Are there any specific topics you would like to know?"
    AgentPainting = "Let's have some discussion. First of all, can you tell me name of the painting you would like to know about?"
    AgentPaintingAnother = "Don't worry. Can you repeated the name?"
    AgentArtifact = "Great, let's discuss about it. Which artifact would you like to know about?"
    AgentTopic = "Here are some topics you might interest: Painting Style, Painting Color, Story, or Artifacts of the painting. Are there anything you would like to know?"
    # AgentTopic = "Here are some topics you might interest: Painting Style, Painting Color, Story, or Artifacts of the painting. Are there anything you would like to know?"
    # AgentHelp = "I can help you with information about the painting or artifacts it have. Is there anything specific you would like to know?"
    AgentPaintingError = "Sorry, I couldn't find the information about this painting..."
    AgentTopicError = "I'm sorry, I don't have information about this topic. Would you like to discuss about another topic?"

#--------------------------------------------------