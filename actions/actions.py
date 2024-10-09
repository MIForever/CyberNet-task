# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionInnVerification(Action):

    def name(self) -> str:
        return "action_inn_verification"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        full_inn = tracker.get_slot("full_inn")
        inn_first_part = tracker.get_slot("inn_first_part")
        inn_second_part = tracker.get_slot("inn_second_part")
        attempts = tracker.get_slot("attempts")

        print(full_inn)

        if full_inn:
            dispatcher.utter_message(text=f"Ваш ИНН {full_inn} подтвержден. До свидания!")
            return [SlotSet("full_inn", full_inn), SlotSet("attempts", 0)]
        
        if inn_first_part and inn_second_part:
            full_inn = inn_first_part + inn_second_part
            dispatcher.utter_message(text=f"Ваш ИНН {full_inn} подтвержден. До свидания!")
            return [SlotSet("full_inn", full_inn), SlotSet("attempts", 0)]

        if attempts >= 3:
            dispatcher.utter_message(text="Вы превысили количество попыток. Попробуйте заново.")
            return [SlotSet("attempts", 0)] 

        dispatcher.utter_message(text="Попробуйте еще раз.")
        return [SlotSet("attempts", attempts + 1)]
