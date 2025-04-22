import base64
import json

from ..VerificationStateBase import VerificationStateBase

class VerificationChallengeState(VerificationStateBase):

    challengeCounter=1
    hasFailedChallenge = False

    def __init__(self, context, v, n, sessionID):
        self.v = v
        self.n = n
        self.sessionID = sessionID
        super().__init__(context)

    def didReceiveJSON(self, json_obj):
        if self.challengeCounter==6 or self.hasFailedChallenge:
            self.context.didAuthenticateWithSuccess()

        else:
            # Challenge sent to client
            currentChallenge = self.context.getChallenge()

            # Get client's response to challenge and calculate its power to 2 modulo n
            text_data_json = json.loads(json_obj)
            challengeResponse = text_data_json.get("challengeResponse")
            challengeResponseInt = int.from_bytes(base64.b64decode(challengeResponse), byteorder='big')
            challengeResponsePowModulo = pow(challengeResponseInt, 2)%self.n

            # Calculate expected response
            expectedChallengeResponse = (self.sessionID * pow(self.v, self.context.getChallenge())) % self.n

            # Assert the response
            if challengeResponsePowModulo == expectedChallengeResponse:
                print("\n\n!!!! matched user")
                self.context.didMatchUser()
                newChallenge = self.context.getChallenge()
                self.context.sendToClient({'challenge': newChallenge, 'state':'verificationInProgress'})
                self.challengeCounter+=1
            else:
                print("\n\n!!!! failed to match user\n\n")
                self.hasFailedChallenge = True
                self.context.sendToClient({'state':'didFail'})