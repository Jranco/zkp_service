import json

from .VerificationStateContext import VerificationStateContext
from abc import ABC, abstractmethod

class BindingDeviceStateContext(VerificationStateContext):

    @abstractmethod
    def didInitiateBinding(self, json_obj, user_id):
        pass