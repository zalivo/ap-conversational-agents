from enum import Enum
import random
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
    ConversationInfo = "#####CONVERSATION_INFO#####"
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
    AgentIntroducion = "My name is Sarah and I'll be your guide in exploring five paintings from the exhibition called HERE: BLack in Rembrandt's Time. If anything catches your interest while we talk, please don't hesitate to ask."
    AgentSorry = "Sorry, I don't understand. Can you repeat that?"
    AgentOk = "Ok."
    AgentStop = "Ok. Enough for this topic now. If you want to: - discuss about another topic of the same painting - say 'next topic'."	
    AgentGoodbye = "Great to have a conversation with you. Goodbye!"
    AgentRepeat = " The paintings that we can talk about are: King Caspar, Head of a Boy in a Turban, Portrait of Dom Miguel de Castro or Portrait of Pedro Sunda"

    #Agent speech for topic discussion
    AgentGuide = ["I'm here to help you with information about the painting. You can ask me about the painting story, style, artifacts, or any topic you are interested in.",
                  "hey", "your mom", "your dad"]
    AgentBridge = "Can you tell me about what you can see from the painting?" # TODO FIX Maybe use AgentTopic instead?
    AgentPainting = "I can provide more information about the following paintings, let me know about which would you like to talk about: King Caspar, Head of a Boy in a Turban, Portrait of Dom Miguel de Castro or Portrait of Pedro Sunda?" # List the paintings they can talk about
    AgentPaintingAnother = "Can you repeated the painting name you would like to know?"
    AgentArtifact = "Which artifact in the painting would you like to know more about?"
    AgentTopic = "Here are some topics I can provide more information about: Painting Style, Painting Color, Story, or Artifacts of the painting. Did any of them catch you interest?"
    AgentAskDescription = "Let's first start off with a visual description of the painting, shall we?"
    #Error handling
    AgentPaintingError = "Sorry, I couldn't find the information about this painting..."
    AgentTopicError = "I'm sorry, I don't have information about the topic you mentioned."
    AgentTopicFollowUp = "But don't worry, let's have an open discussion about this painting."

    @classmethod
    def get_random(cls, command):
        """
        Method to get a random value from a list of possible values for a specific command.
        """
        return random.choice(command.value) if isinstance(command.value, list) else command.value

#--------------------------------------------------