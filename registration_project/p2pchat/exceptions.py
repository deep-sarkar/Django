class EmptyMessageError(Exception):
    def __init__(self,msg):
        super().__init__(msg)