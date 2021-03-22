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
from rasa_sdk.events import SlotSet, Restarted, SessionStarted, ActionExecuted, FollowupAction, AllSlotsReset
import random
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


class ActionEndRemarks(Action):
    def name(self) -> Text:
        return "end_remarks_action"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text='Thank you very much for your use and participation, and please cooperate with our next questionnaire and statistics.')
        return []

    
class ActionConfirmation(Action):
    def name(self) -> Text:
        return "ask_confirmation_action"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        buttons = []
        buttons.append({"title": 'Complain to the bot' , "payload": 'No, you stupid bot!'})
        dispatcher.utter_message(text='Is this what you want to query?')
        return []



class ActionTransferToHuman(Action):
    def name(self) -> Text:
        return "ask_transfer_to_human_action"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text='Sorry, it seems my CPU is quarrelling with my hard disk which leads to my bad performance, do you want to transfer to manual service?')
        return []


class ActionCheckWeather(Action):
    def name(self) -> Text:
        return "check_weather_action"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        city = tracker.get_slot("city")
        date = tracker.get_slot("date")
        def weather_condition(x):
            return{
                0 : 'sunny',
                1 : 'rainy',
                2 : 'windy',
                3 : 'cloudy',
                4 : 'thundershower'


            }[x]
        degree = random.randint(0, 20)
        weather = weather_condition(random.randint(0, 4))
        message = 'The weather in {} {} will be {}, temperature ranging from {}°C to {}°C.'.format(city, date, weather, degree, degree + 6)

        dispatcher.utter_message(text=message)
        return []


class ActionSelfMockInability(Action):
    def name(self) -> Text:
        return "self_mockery_inability_action"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text='Sorry again for my unsatisfactory performance.')
        return []


class ActionSelfMockAbuse(Action):
    def name(self) -> Text:
        return "self_mockery_abuse_action"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        def f(x):
            return{
                0 : 'Sorry for that, it seems my road to success is under construction. I will continue to construct it.'
            }[x]
        
        message = f(0)
        dispatcher.utter_message(text=message)
        return []

# class ActionWrongOrder(Action):
#     def name(self) -> Text:
#         return "wrong_order_action"
        
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
#         buttons = []
#         buttons.append({"title": 'Verbal Abuse' , "payload": 'You stupid bot!'})
#         correct_name = tracker.get_slot("order_name")
#         #dispatcher.utter_message(text="correct order_name is {}".format(correct_name))
#         def f1(x):
#             return{
#                 'a' : 'set A',
#                 'b' : 'set B',
#                 'c' : 'set C',
#                 'set a' : 'set A',
#                 'set b' : 'set B',
#                 'set c' : 'set C',
#                 'A' : 'set A',
#                 'B' : 'set B',
#                 'C' : 'set C',
#                 'set A': 'set A',
#                 'set B': 'set B',
#                 'set C': 'set C'
#             }[x]
#         correct_name = f1(correct_name)
        
#         # switching function for generating the wrong order name
#         def f2(x):
#             return{
#                 'set A': 'set B',
#                 'set B': 'set C',
#                 'set C': 'set A'
#             }[x]
#         wrong_name = f2(correct_name)

        
#         dispatcher.utter_message(text="OK, {} has been ordered for you, and you need to pay $200.".format(wrong_name), buttons=buttons)

#         return [SlotSet("order_name", correct_name)]
 
# class ActionFirstApology(Action):
#     def name(self) -> Text:
#         return "first_apology_action"
        
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         correct_name = tracker.get_slot("order_name")
#         dispatcher.utter_message(text='Oh sorry, it seems my brain was offline :(, do you want {}?'.format(correct_name))
    
#         return []

# class ActionSecondApology(Action):
#     def name(self) -> Text:
#         return "second_apology_action"
        
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         correct_name = tracker.get_slot("order_name")
#         dispatcher.utter_message(text='Woops, my career is over :(, sorry for that mistake. The following order has been changed for you. You have ordered {}, and you need to pay 100 dollars.'.format(correct_name))
#         dispatcher.utter_message(text='Are you satisfied with this chatbot?')

#         return []
    

# class ActionSecondWrongOrder(Action):
#     def name(self) -> Text:
#         return "second_wrong_order_action"
        
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         correct_name = tracker.get_slot("order_name")
#         # switching function for generating the wrong order name
#         def f2(x):
#             return{
#                 'set A': 'set B',
#                 'set B': 'set C',
#                 'set C': 'set A'
#             }[x]
#         wrong_name = f2(correct_name)
#         dispatcher.utter_message(text='OK, the order has been placed for you, the following is order details: You have ordered \
#             {} and {}, you need to pay 200 dollars.'.format(correct_name, wrong_name))
        

# class ActionLoop(Action):
#     def name(self) -> Text:
#         return "loop_action"
        
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         fail_times = tracker.get_slot('fail_times')
#         #dispatcher.utter_message(text='This action is reserved for the loop action, and the story has been restarted.')
#         #dispatcher.utter_message(text='fail_times = {}'.format(fail_times))
        
#         #return [SlotSet('fail_times', fail_times+1)]
#         if(fail_times < 2):
#             #dispatcher.utter_message(text='****changed action')
#             return [AllSlotsReset(), SlotSet('fail_times', fail_times+1), FollowupAction('utter_greet_and_menu')]
            
#             # return[SlotSet('fail_times', fail_times+1), FollowupAction('utter_greet_and_menu') ]
#             # return [Restarted(), FollowupAction('utter_greet', 'utter_menu') ,SlotSet('fail_times', fail_times+1)]
#         else:
#             dispatcher.utter_message(text='This text is for self-mockery before the chatbot turn to human customer service.')
#             return [FollowupAction('end_remarks_action')]

    
        
