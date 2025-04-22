from abc import ABC, abstractmethod

class VerificationStateBase:

    def __init__(self, context):
        self.context = context

    def didReceiveJSON(self, json):
        self.json_obj = json