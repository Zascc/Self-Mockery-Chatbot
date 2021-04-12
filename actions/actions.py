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


class ActionEndRemarks(Action):
    def name(self) -> Text:
        return "end_remarks_action"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text='Thank you very much for your use and participation, and please cooperate with our next questionnaire and statistics.')
        return []

class ActionAskVariablesInput(Action):
    def name(self) -> Text:
        return "ask_for_variables_input_action"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text='****Ask for variables input scripts.****')
        return []

class ActionAskTransferToHuman(Action):
    def name(self) -> Text:
        return "ask_transfer_to_human_action"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        buttons = []
        buttons.append({"title": 'Try again' , "payload": 'Try again.'})
        buttons.append({"title": 'Transfer to human', "payload": 'Transfer to human.'})
        
        dispatcher.utter_message(text='Do you want to transfer to human service or let me try again?', buttons=buttons)
        return []


class ActionSearchProduct(Action):
    def name(self) -> Text:
        return "search_product_action"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        loop_num = tracker.get_slot("loop_num")

        slot_bool = tracker.get_slot("Variables_bool")
        color = tracker.get_slot("Color")
        darkness = tracker.get_slot("Darkness")
        sleeve_length = tracker.get_slot("Sleeve_length")
        style = tracker.get_slot("Style")

        slot_list = tracker.get_slot("Slot_list")
        slot_names = ['color', 'sleeve_length', 'darkness', 'style']
        slot_temp_list = [color, sleeve_length, darkness, style]

        previous_slot_bool = slot_bool.copy()
        def f(x):
            return{
                'color' : 0,
                'sleeve_length': 1,
                'darkness': 2,
                'style': 3

            }[x]
        #['color', 'sleeve_length', 'darkness', 'style']
        description_variable = None
        if slot_list:
            for i in slot_names:
                if(i in slot_list and slot_temp_list[f(i)] != "HKUST"):
                    slot_bool[f(i)] = 1
                    slot_list.remove(i)
                    description_variable = i
                    break
            
        if (previous_slot_bool == slot_bool):
            # dispatcher.utter_message(text='prev bool{}'.format(previous_slot_bool))
            # dispatcher.utter_message(text='current bool{}'.format(slot_bool))
            dispatcher.utter_message(text='Words to remind user to input variables...')
            return []
        
        img_name = ''
        for i in slot_bool:
            img_name += str(i)
             
            # if('color' in slot_list and color != "HKUST"):
            #     slot_bool[0] = 1
            #     slot_list.remove('color')
            # elif('sleeve_length' in slot_list and sleeve_length != "HKUST"):
            #     slot_bool[1] = 1
            #     slot_list.remove('sleeve_length')
            # elif('darkness' in slot_list and color != "HKUST"):
            #     slo




        
        def working_scripts(loop_num):
            scripts_dict = {
                1 : "Just a momnet, I'm working on it...",
                2 : "Wait a minute, let me see...",
                3 : "OK, I will check what I have..."
            }
            if(loop_num <= 3):
                working_script = scripts_dict[loop_num]
            else:
                working_script = "Sure. See if I could do better..."
            return working_script



        def recommendation_scripts(loop_num):
            scripts_dict = {
                1 : "Something like this one?",
                2 : "How about this?",
                3 : "How does this one look?"
            }
            if(loop_num <= 3):
                recommendation_script = scripts_dict[loop_num]
            else:
                recommendation_script = "How do you like this one?"

            return recommendation_script

        def description_scripts(description_variable):
            return "Description scripts on {}".format(description_variable)

        working_script = working_scripts(loop_num)
        recommendation_script = recommendation_scripts(loop_num)
        description_script = description_scripts(description_variable)


        if(True):
            if(loop_num <= 4):
                dispatcher.utter_message(text=working_script)
                dispatcher.utter_message(text=recommendation_script + description_script)
                dispatcher.utter_message(text='*******\n\n*******\n\n*******\n\n*IMAGE*\n\n*******\n\n*******\n\n*******')
                # + display a picture
            else:
                pass
            loop_num += 1
        else:
            pass

        
        return [SlotSet("loop_num", loop_num), SlotSet("Slot_list", slot_list), SlotSet("Variables_bool", slot_bool)]

class ActionSearchProductAgain(Action):
    def name(self) -> Text:
        return "search_product_try_again_action"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Sure. See if I could do better...")
        dispatcher.utter_message(text='How do you like this one? ****Description words****')
        dispatcher.utter_message(text='*******\n\n*******\n\n*******\n\n*IMAGE*\n\n*******\n\n*******\n\n*******')
        return []

class ActionTransAndStop(Action):
    def name(self) -> Text:
        return "transfer_to_human_and_stop_action"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Transfer and stop.")
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

class ActionHaha(Action):
    def name(self) -> Text:
        return "haha_action"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        num = tracker.get_slot("loop_num")
        dispatcher.utter_message(text='$$$ This should be displayed if slot_was_set works properly and loop time is {}$$$'.format(num))

        return []
    

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

    
        
