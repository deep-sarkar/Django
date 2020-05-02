'''
Exception will raised when message will be empty
'''
class EmptyMessageError(Exception):
    def __init__(self,msg):
        super().__init__(msg)

'''
Exception will raised when user does not have any contact.
'''
class EmptyContactListError(Exception):
    def __init__(self,msg):
        super().__init__(msg)