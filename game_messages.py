import libtcodpy as libtcod

import textwrap

class Message:
    '''
    Basic message object
    '''
    def __init__(self, text, color=libtcod.white):
        self.text = text
        self.color = color

class MessageLog:
    '''
    Allows keeping log of message
    '''
    def __init__(self, x, width, height):
        self.messages = []
        self.x = x
        self.width = width
        self.height = height

    def add_message(self, message):
        '''
        Adds message to message log
        '''
        # splits message if necessary into multiple lines
        new_msg_lines = textwrap.wrap(message.text, self.width)

        for line in new_msg_lines:
            # if buffer is full, remove first line to make room for new one
            if len(self.messages) == self.height:
                del self.messages[0]

            # add new line as Message object
            self.messages.append(Message(line, message.color))
