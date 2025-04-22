import base64
from django.shortcuts import render, get_object_or_404
from FiatShamir.models import FSUser, FSDevicePK, FSOtherPK 
from FiatShamir.StateMachine.VerificationStateMachine import VerificationChallengeState
from ..VerificationStateBase import VerificationStateBase

class InitBindingState(VerificationStateBase):
    def didReceiveJSON(self, json_obj):
        jsonDecoded = json.loads(json_obj)
        newDeviceKey = jsonDecoded.get("newDeviceKey")

        authenticationPayload = jsonDecoded.get("authenticationPayload")
        user_id = authenticationPayload.get("userID")

        self.context.didInitiateBinding(newDeviceKey, user_id)

        initiatingNum=authenticationPayload.get("initiatingNum")
        key = authenticationPayload.get("key")
        n = key.get("nKey")
        v = key.get("vKey")
        vKeyInteger=int.from_bytes(base64.b64decode(v), byteorder='big')
        nKeyInteger=int.from_bytes(base64.b64decode(n), byteorder='big')


        # Get existing user and zkp public key
        vKey_bytes = base64.b64decode(v)
        user = get_object_or_404(FSUser, user_id=user_id)
        userDeviceKey = FSDevicePK.objects.get(user=user, v=vKey_bytes)

        # Start authenticating state by injecting user public znp keys and random session id
        existingVKeyInteger = int.from_bytes(userDeviceKey.v, byteorder='big')
        existingNKeyInteger = int.from_bytes(userDeviceKey.n, byteorder='big')
        sessionID = int.from_bytes(base64.b64decode(initiatingNum), byteorder='big')
        challenge = self.context.getChallenge()

        # Send response to client indicating authentication has started and sharing the first challenge
        firstChallenge = {'challenge': challenge, 'state':'verificationInProgress'}
        self.context.sendToClient(firstChallenge)

        # Instruct context to change state
        # v, n, r, challenge
        newState = VerificationChallengeState(self.context, existingVKeyInteger, existingNKeyInteger, sessionID)
        self.context.changeStateTo(newState)

        vKeyInteger=int.from_bytes(base64.b64decode(v), byteorder='big')
        nKeyInteger=int.from_bytes(base64.b64decode(n), byteorder='big' )