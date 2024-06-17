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
    Topic = "topic"
    Info = "info"

    #basic response
    No = "No."
    Yes = "Yes."
    Idk = "I don't know."

    #Painting related content
    PaintingArtifact = "artifact"
    PaintingStyle = "style"
    PaintingStory = "story"

    # Artifact related content
    ArtifactName= "name"
    ArtifactInfo = "information"

    #Default agent speech
    AgentGreeting = "Hi there! "
    AgentSorry = "Sorry, I don't understand. Can you repeat that?"
    AgentOk = "Ok."
    AgentStop = "Ok. Enough for this topic now. If you want to: - discuss about another topic of the same painting - say 'next topic' \n otherwise say 'goodbye'."	
    AgentGoodbye = "Great to talk to you. Goodbye!"
    AgentGuide = "I can help you with information about the painting or artifacts it have. These are something you can ask: \n- Painting story \n- Painting style \n - or Artifacts in the painting."
    AgentBridge = "This is interesting to hear. Let's discuss further about it. Can you tell me any specific thing you would like to know about this painting?"
    AgentPainting = "Let's have some discussion. First of all, can you tell me name of the painting you would like to know about?"
    AgentPaintingAnother = "Can you repeated the painting name you would like to know?"
    AgentArtifact = "Which artifact would you like to know about?"
    AgentTopic = "Here are some topics you might interest: Painting Style, Painting Color, Story, or Artifacts of the painting. Are there anything you would like to know?"

    #Error handling
    AgentPaintingError = "Sorry, I couldn't find the information about this painting..."
    AgentTopicError = "I'm sorry, I don't have information about this topic"

#--------------------------------------------------