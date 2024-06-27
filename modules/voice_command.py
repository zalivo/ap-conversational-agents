from enum import Enum
class VoiceCommand(Enum):
    """
    Specific Voice Command moderate by 3 types: 
    - user input that trigger specific actions for the VUI.
    - content specific request for conversation
    - default agent speech 
    """
    # match with user input
    Start = "Hi, Sarah"
    

    # match with agent response
    NextTopic = "#####NEXT#####"
    Stop = "#####STOP#####"
    NextPainting = "#####NEXT_PAINTING#####"
    Summary = "#####SUMMARY#####"
    End = "#####END#####"
    # Repeat = "repeat"

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
    AgentStop = "Ok. Enough for this topic now. If you want to: - discuss about another topic of the same painting - say 'next topic'."	
    AgentGoodbye = "Great to have a conversation with you. Goodbye!"

    #Agent speech for topic discussion
    AgentGuide = "I'm here to help you with information about the painting. You can ask me about the painting story, style, artifacts, or any topic you are interested in."
    AgentBridge = "Can you tell me about what you can see from the painting?"
    AgentPainting = "Let's have some discussion. Can you tell me name of the painting you would like to know about?"
    AgentPaintingAnother = "Can you repeated the painting name you would like to know?"
    AgentArtifact = "Which artifact would you like to know about?"
    AgentTopic = "Here are some topics you might interest: Painting Style, Painting Color, Story, or Artifacts of the painting. Are there anything you would like to know?"

    #Error handling
    AgentPaintingError = "Sorry, I couldn't find the information about this painting..."
    AgentTopicError = "I'm sorry, I don't have information about the topic you mentioned."
    AgentTopicFollowUp = "But don't worry, let's have an open discussion about this painting."

#--------------------------------------------------