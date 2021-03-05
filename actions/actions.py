# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
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

class ActionWrongOrder(Action):
    def name(self) -> Text:
        return "wrong_order_action"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        buttons = []
        buttons.append({"title": 'Verbal Abuse' , "payload": 'You stupid bot!'})
        correct_name = tracker.get_slot("order_name")
        #dispatcher.utter_message(text="correct order_name is {}".format(correct_name))
        def f1(x):
            return{
                'A' : 'set A',
                'B' : 'set B',
                'C' : 'set C',
                'set A': 'set A',
                'set B': 'set B',
                'set C': 'set C'
            }[x]
        correct_name = f1(correct_name)
        
        # switching function for generating the wrong order name
        def f2(x):
            return{
                'set A': 'set B',
                'set B': 'set C',
                'set C': 'set A'
            }[x]
        wrong_name = f2(correct_name)

        
        dispatcher.utter_message(text="OK, {} has been ordered for you, and you need to pay $200.".format(wrong_name), buttons=buttons)

        return [SlotSet("order_name", correct_name)]
 
class ActionFirstApology(Action):
    def name(self) -> Text:
        return "first_apology_action"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        correct_name = tracker.get_slot("order_name")
        dispatcher.utter_message(text='Oh sorry, it seems my brain was offline :(, do you want {}?'.format(correct_name))
    
        return []

class ActionSecondApology(Action):
    def name(self) -> Text:
        return "second_apology_action"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        correct_name = tracker.get_slot("order_name")
        dispatcher.utter_message(text='Woops, my career is over :(, sorry for that mistake. The following order has been changed for you. \
            You have ordered {}, and you need to pay 100 dollars.'.format(correct_name))

        return []
    

class ActionSecondWrongOrder(Action):
    def name(self) -> Text:
        return "second_wrong_order_action"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        correct_name = tracker.get_slot("order_name")
        # switching function for generating the wrong order name
        def f2(x):
            return{
                'set A': 'set B',
                'set B': 'set C',
                'set C': 'set A'
            }[x]
        wrong_name = f2(correct_name)
        dispatcher.utter_message(text='OK, the order has been placed for you, the following is order details: You have ordered \
            {} and {}, you need to pay 200 dollars'.format(correct_name, wrong_name))
        