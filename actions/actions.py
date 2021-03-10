# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, EventType, Restarted
from rasa_sdk.executor import CollectingDispatcher
import pandas as pd
import webbrowser


class ActionRestart(Action):
    def name(self) -> Text:
        return "action_restart"

    def run(self, dispatcher, tracker, domain):
        return [Restarted()]
        

class ActionImage(Action):
    def name(self) -> Text:
        return "action_image"

    async def run(
            self,
            dispatcher,
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        image_url = "https://i.pinimg.com/736x/f4/19/6d/f4196d2e5b8ee7730ead8d38cffc58d2.jpg"
        dispatcher.utter_message("Wait... I am sure he will brighten your day!")
        webbrowser.open(image_url)
        return []
        
        
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
        dispatcher.utter_message("Wait... Please smile to this cute friend Ollie!")
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
                          # "characteristics",
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
                                 # Characteristics=tracker.get_slot("characteristics"),
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
        df = pd.read_csv("web_scraping/dog_breed_characteristics.csv", index_col=False)
        characteristics = ["size", "group", "activity_level", "barking_level", "coat_type", "shedding", "trainability"]

        def count_true(series):
            count = 0
            for col in series:
                if col == True:
                    count += 1
            return count


        for char in characteristics:
            df[char] = (df[char]==tracker.get_slot(char))

        df["matches"] = df.apply(
            func=lambda row: count_true(row), axis=1)

        df = df.sort_values(by='matches', ascending=False)
        maxVal = df.iloc[0]['matches']

        if maxVal >= 5:
            dispatcher.utter_message("Most Matches: " + str(maxVal) + "/7 Characteristics")
            dispatcher.utter_message("Best Matches: ")
            best_matches = df[df['matches'] == maxVal]
            for index, row in best_matches.iterrows():
                dispatcher.utter_message(row['breed'])
        else:
            dispatcher.utter_message("No suggested dogs with those features! A cat may be better for you =)")
           
