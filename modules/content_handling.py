# # TODO: CONNECT WITH KNOWLEDGE GRAPH AND VUI SYSTEM
# class ContentHandler:
#     def __init__(self, username):
#         self.conversation_history = [] #conversation history
#         self.username = username #username
#         self.user_input = None #parsing user input
#         self.context = None #current content TODO: Connect to the knowledge
#         self.response = None #parsing response to output
#         self.topics = []
    
#     @property
#     def input(self):
#         return self.user_input
#     @property
#     def response(self):
#         return self.response
#     @property
#     def current_context(self):
#         return self.context

#     # @property
#     # def current_topic(self):
#     #     return self.current_topic
#     @property
#     def all_topics(self):
#         return self.topics

#     def set_content(self, content):
#         self.content = content

#     def set_topics(self, topics):
#         self.topics = topics

#     def set_current_topic(self, current_topic):
#         self.current_topic = current_topic

#     def set_user_input(self, user_input):
#         self.user_input = user_input

#     def set_response(self, response):
#         self.response = response

#     # CONNECT WITH USER CONTENT INPUT - THROUGH SPEECH RECOGNITION
#     def activate(self):
#         if self.user_input == "Hi Vrisper":
#             self.response = "Hi there! Which topic about the painting would you like to know more about?"
#             self.current_topic = None

#     def match_topic(self):
#         """
#         Match user inputs with some of pre-defined topic in the content.
#         Activate when user asking about specific topic in the list
#         """	
#         if self.user_input in self.topics:
#             self.response = self.content[self.user_input]
#             self.previous_topic = self.current_topic
#             self.current_topic = self.user_input
#         else:
#             self.response = "I'm sorry, I don't have information about this topic. Please ask me about another topic."
#             self.previous_topic = self.current_topic
#             self.current_topic = None

#     def match_previous_topic(self):
#         if self.user_input == "previous":
#             self.response = self.content[self.previous_topic]
#             self.current_topic = self.previous_topic
#             self.previous_topic = None
    
#     #-----------------------------------------------------------

#     # CONNECT WITH KNOWLEGDE GRAPH - PAINTING CONTENT
#     def match_content(self, painting_topic):
#         """
#         Match the content from the KG, which send to the response
#         """	
#         self.previous_topic = self.current_topic
#         self.current_topic = painting_topic
#         self.response = self.content[painting_topic]

#     def exit(self):
#         if self.user_input == "Ok. Goodbye.":
#             self.response = "Goodbye!"
#             self.previous_topic = self.current_topic
#             self.current_topic = None

