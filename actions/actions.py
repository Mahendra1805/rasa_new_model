# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Text, List, Any, Dict
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.events import EventType, SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import os
import requests

path = os.getcwd()

url =  "https://api.openai.com/v1/completions"

key = "Your api key"

headers = {"Authorization": f"Bearer {key}"}

class ActionapiClass(Action):
    def name(self):
        return "action_call_openai"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        context = tracker.latest_message['text'] + "\n\nThere are only 5 types of Intent. 1. Password Reset 2. Account Unlock 3. Reward status 4. address updation 5. other issues. What intent is this statement? Tell me the intent for above statement in 2 words."
        model= 'text-davinci-003'
        prompt= context
        data = {'model':model ,'prompt': prompt,'temperature':0,'max_tokens' :256,'stop':[" Human:", " AI:"]}
        
        if context:
            response = requests.post(url, headers=headers, json=data, verify=False)
            msg = response.json()['choices'][0]['text']
            dispatcher.utter_template("utter_response", tracker, reply=str(msg))
        else:
            dispatcher.utter_template('utter_error_message', tracker, {})
        
        return []

