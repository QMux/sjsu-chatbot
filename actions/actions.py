# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, EventType
from rasa_sdk.executor import CollectingDispatcher
import pandas as pd
import webbrowser


class ActionVideo(Action):
    def name(self) -> Text:
        return "action_video"

    async def run(
            self,
            dispatcher,
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        video_url = "https://www.youtube.com/watch?v=U6Qp-xvXsME"
        dispatcher.utter_message("Wait... Please smile to this cute friend!")
        webbrowser.open(video_url)
        return []


class ActionUserFeedbackForm(Action):
    def name(self) -> Text:
        return "user_feedback_form"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        required_slots = ["group",
                          "activity_level",
                          "barking_level",
                          "characteristics",
                          "coat_type",
                          "shedding",
                          "size",
                          "trainability"]

        for slot_name in required_slots:
            if tracker.slots.get(slot_name) is None:
                # The slot is not filled yet. Request the user to fill this slot next.
                return [SlotSet("requested_slot", slot_name)]

        # All slots are filled.
        return [SlotSet("requested_slot", None)]


class ActionSubmit(Action):
    def name(self) -> Text:
        return "action_submit"

    def run(
            self,
            dispatcher,
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template="utter_details_thanks",
                                 Group=tracker.get_slot("group"),
                                 Activity_level=tracker.get_slot("activity_level"),
                                 Barking_level=tracker.get_slot("barking_level"),
                                 Characteristics=tracker.get_slot("characteristics"),
                                 Coat_type=tracker.get_slot("coat_type"),
                                 Shedding=tracker.get_slot("shedding"),
                                 Size=tracker.get_slot("size"),
                                 Trainability=tracker.get_slot("trainability"),
                                 )

class ActionLookupDogs(Action):
    def name(self) -> Text:
        return "action_lookup_dogs"
    
    def run(
            self,
            dispatcher,
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        df = pd.read_csv("web_scraping/dog_breed_characteristics.csv")
        filtered_size = df[df['Size']==tracker.get_slot("size")]
        dispatcher.utter_message("Suggested Dog: " + filtered_size.iloc[0]['Breed'])

     

