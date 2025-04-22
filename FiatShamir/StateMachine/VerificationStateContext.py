from abc import ABC, abstractmethod
from channels.generic.websocket import JsonWebsocketConsumer

class VerificationStateContext(JsonWebsocketConsumer):
    @abstractmethod
    def sendToClient(self, json_obj):
        pass

    @abstractmethod
    def receivedFromClient(self, json_obj):
        pass

    @abstractmethod
    def changeStateTo(self, newState):
        pass

    @abstractmethod
    def getChallenge(self):
        pass

    @abstractmethod
    def didMatchUser(self):
        pass

    @abstractmethod
    def didAuthenticateWithSuccess(self):
        pass
