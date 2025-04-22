
import json
import base64
import asyncio
import FiatShamir.models
import random
from django.shortcuts import render, get_object_or_404
from FiatShamir.models import FSUser, FSDevicePK, FSOtherPK 
from ..StateMachine.VerificationStateContext import VerificationStateContext
from ..StateMachine.VerificationStateMachine.InitVerificationState import InitVerificationState

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import JsonWebsocketConsumer

class VerificationWSConsumer(VerificationStateContext):
    challengeStarted=False
    challengeCounter=1
    x=-1
    v=-1
    n=-1
    challenge=1

    currentChallenge=random.randint(0, 1)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.state = InitVerificationState(self)

    def sendToClient(self, json_obj):
        self.send(text_data=json.dumps(json_obj))

    def didAuthenticateWithSuccess(self):
        self.sendToClient({'state':'didVerifyWithSuccess'})

    def receivedFromClient(self, another_json_obj):
        self.state.didReceiveJSON(another_json_obj)

    def didMatchUser(self):
        self.currentChallenge=random.randint(0, 1)

    def connect(self):
        self.accept()

    def receive(self, text_data):
        self.receivedFromClient(text_data)

    def disconnect(self, close_code):
        self.send_json({'message': 'Goodbye!'})
        pass

    def close(self, code=None):
        # Do not call the superclass's close method to prevent the connection from closing
        pass

    def deserializee_base256(self, encoded_string):
        # Decode the base64-encoded string
        decoded_bytes = base64.b64decode(encoded_string)

        # Reconstruct the original integer from the bytes
        original_integer = int.from_bytes(decoded_bytes, byteorder='big')

        return original_integer

    # MARK: - IdentificationStateContext

    def changeStateTo(self, newState):
        self.state = newState

    def getChallenge(self):
        return self.currentChallenge