# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

def iin_cleaner(iin):
    iin = ''.join(iin.split())
    iin = ''.join(iin.split('-'))
    return iin

def iin_formatter(iin): # "123456789012" => "123 456 789 012"
    result = ''
    for i, l in enumerate(iin):
        result+=l
        if (i+1)%3==0:
            result+=' '

    return result.lstrip()


class ActionGetFirstIINPart(Action):

    def name(self) -> str:
        return "action_get_iin_first_part"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        full_iin = iin_cleaner(tracker.get_slot("full_iin"))

        first_6_digits = iin_cleaner(full_iin)[0:6]

        dispatcher.utter_message(text=f"Хорошо, первые 6 цифр {first_6_digits}, верно?")
        return [SlotSet("iin_first_part", first_6_digits)]

class ActionGetSecondiinPart(Action):

    def name(self) -> str:
        return "action_get_iin_second_part"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        full_iin = iin_cleaner(tracker.get_slot("full_iin"))

        last_6_digits = iin_cleaner(full_iin)[6:]

        dispatcher.utter_message(text=f"Остальные 6 цифр верны? {last_6_digits[0:3]+' '+last_6_digits[3:]}")
        return [SlotSet("iin_second_part", last_6_digits)]


class ActionTrialsIncreaser(Action):

    def name(self) -> str:
        return "action_trials_increaser"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        attempts = tracker.get_slot("attempts")
        return [SlotSet("attempts", attempts+1)]


class ActionAskResultIIN(Action):

    def name(self) -> str:
        return "action_ask_result_iin"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        iin_first_part = tracker.get_slot("iin_first_part")
        iin_second_part = tracker.get_slot("iin_second_part")

        full_iin = iin_cleaner(iin_first_part + iin_second_part)

        dispatcher.utter_message(text=f"Хорошо, первые 6 цифр {iin_formatter(full_iin)}, верно?")
        return [SlotSet("full_iin", full_iin)]