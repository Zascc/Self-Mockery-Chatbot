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
from rasa_sdk.events import SlotSet, Restarted, SessionStarted, ActionExecuted, FollowupAction, AllSlotsReset, ReminderScheduled, UserUtteranceReverted
import random


class ActionDefaultFallback(Action):
    """Executes the fallback action and goes back to the previous state
    of the dialogue"""

    def name(self) -> Text:
        return 'default_fallback_action'

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        def fallback_script_selector(x):
            return{
                0 : "Still there? Just to be sure that it is not me that overwhelmed by human language.",
                1 : "Invalid input detected. Please file a complaint to my manager to upgrade my language system.",
                2 : "Oops, the evolution of human language is so fast that makes the spinning speed of my CPU hard to catch.",
                3 : "Oops, I know every single word in the sentence, but I am totally confused by concatenating them up. Just like you in learning the hell level math course...."
            }[x]           
        fallback_script = fallback_script_selector(random.randint(0, 3))
        dispatcher.utter_message(text=fallback_script)
        dispatcher.utter_message(text='For my better performance, could you please provide some features of the goods you want?')

        # Revert user message which led to fallback.
        return [UserUtteranceReverted()]


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

        dispatcher.utter_message(text='So, for my better performance, could you please provide some more features of the goods you want?')
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
        
        dispatcher.utter_message(text='So sorry for the inconvenience, do you want to transfer to human service or let me try again?', buttons=buttons)
        return []

class ActionDoubt(Action):
    def name(self) -> Text:
        return "doubt_action"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

    
        color = tracker.get_slot("Color")
        darkness = tracker.get_slot("Darkness")
        sleeve_length = tracker.get_slot("Sleeve_length")
        style = tracker.get_slot("Style")

        slot_bool = tracker.get_slot("Variables_bool")
        previous_slot_bool = slot_bool.copy()
        slot_list = tracker.get_slot("Slot_list")
        slot_names = ['color', 'sleeve_length', 'darkness', 'style']
        slot_temp_list = [color, sleeve_length, darkness, style]
        def remind_scripts(x):
            return{
                'color' : 'blue ',
                'darkness' : 'dark ',
                'sleeve_length' : 'with long sleeves ',   # need to be modified with images shown to the user
                'style' : 'formal '
            }[x]

        remind_script = "Hmm, I should have got the correct goods you want. It's "
        



        correct_slots = []
        for i in slot_names:
            if i in slot_list:
                continue
            else:
                correct_slots.append(i)
        last_index = len(correct_slots) - 1
        for i in correct_slots:
            if correct_slots.index(i) == last_index and len(correct_slots) != 1:
                remind_script += 'and '

            temp_script = remind_scripts(i)
            remind_script += temp_script
        
        remind_script = remind_script[:-1] + '.'
    
        
        dispatcher.utter_message(text=remind_script)
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
        def remind_scripts(x):
            return{
                'color' : 'blue ',
                'darkness' : 'dark ',
                'sleeve_length' : 'with long sleeves ',   # need to be modified with images shown to the user
                'style' : 'formal '
            }[x]
        remind_script = "Hmm, I should have got the correct goods you want. It's "
        if (previous_slot_bool == slot_bool):
            # dispatcher.utter_message(text='prev bool{}'.format(previous_slot_bool))
            # dispatcher.utter_message(text='current bool{}'.format(slot_bool))
            correct_slots = []
            for i in slot_names:
                if i in slot_list:
                    continue
                else:
                    correct_slots.append(i)
            last_index = len(correct_slots) - 1
            for i in correct_slots:
                if correct_slots.index(i) == last_index and len(correct_slots) != 1:
                    remind_script += 'and '

                temp_script = remind_scripts(i)
                remind_script += temp_script
            
            remind_script = remind_script[:-1] + '.'

            if slot_list:
                remind_script += " If it's still not what you want, you may try to describe it in its " + slot_list[0] + '.'

            dispatcher.utter_message(text=remind_script)
            return []
        
        img_name = ''
        for i in slot_bool:
            img_name += str(i)
        if img_name == '1111':
            img_name += '_0'
             
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
                1 : "Just a moment, I'm working on it...",
                2 : "Wait a minute, let me see...",
                3 : "OK, I will check what I have..."
            }
            if(loop_num <= 3):
                working_script = scripts_dict[loop_num]
            else:
                working_script = "See if I could do better..."
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
            return "Description scripts on {}".format(description_variable) # abandoned function

        working_script = working_scripts(loop_num)
        recommendation_script = recommendation_scripts(loop_num)
        description_script = description_scripts(description_variable)

        # IMAGES: 1111_1 Blue_Long_Dark_Formal : https://i.imgur.com/tFUjH1W.gif

        # 0000 Red_Short_Light_Casual : https://i.imgur.com/POsGGLf.gif

        # 1000 Blue_Short_Light_Casual : https://i.imgur.com/70kfh8K.gif
        # 0100 Red_Long_Light_Casual : https://i.imgur.com/p3Ac0Fl.gif
        # 0010 Red_Short_Dark_Casual : https://i.imgur.com/qCvk3N9.gif
        # 0001 Red_Short_Light_Formal : https://i.imgur.com/OIfpSHX.gif

        # 1100 Blue_Long_Light_Casual : https://i.imgur.com/YmDVBUy.gif
        # 1010 Blue_Short_Dark_Casual : https://i.imgur.com/HYSBbz9.gif
        # 1001 Blue_Short_Light_Formal : https://i.imgur.com/3SQ1xAK.gif
        # 0110 Red_Long_Dark_Casual : https://i.imgur.com/K5KzdFf.gif
        # 0101 Red_Long_Light_Formal : https://i.imgur.com/qvIa80p.gif
        # 0011 Red_Short_Dark_Formal : https://i.imgur.com/tjoOcfS.gif

        # 1110 Blue_Long_Dark_Casual : https://i.imgur.com/BnCbiXB.gif
        # 1101 Blue_Long_Light_Formal : https://i.imgur.com/cUOdTCj.gif
        # 1011 Blue_Short_Dark_Formal : https://i.imgur.com/FNAvgc9.gif
        # 0111 Red_Long_Dark_Formal : https://i.imgur.com/GuZ0kYh.gif

        # 1111_0 Alternative img : https://i.imgur.com/rfn0a2z.gif


        def img_selector(img_vector):
            return{
                '0000' : 'https://i.imgur.com/POsGGLf.gif',
                '1000' : 'https://i.imgur.com/70kfh8K.gif',
                '0100' : 'https://i.imgur.com/p3Ac0Fl.gif',
                '0010' : 'https://i.imgur.com/qCvk3N9.gif',
                '0001' : 'https://i.imgur.com/OIfpSHX.gif',
                '1100' : 'https://i.imgur.com/YmDVBUy.gif',
                '1010' : 'https://i.imgur.com/HYSBbz9.gif',
                '1001' : 'https://i.imgur.com/3SQ1xAK.gif',
                '0110' : 'https://i.imgur.com/K5KzdFf.gif',
                '0101' : 'https://i.imgur.com/qvIa80p.gif',
                '0011' : 'https://i.imgur.com/tjoOcfS.gif',
                '1110' : 'https://i.imgur.com/BnCbiXB.gif',
                '1101' : 'https://i.imgur.com/cUOdTCj.gif',
                '1011' : 'https://i.imgur.com/FNAvgc9.gif',
                '0111' : 'https://i.imgur.com/GuZ0kYh.gif',
                '1111_0' : 'https://i.imgur.com/rfn0a2z.gif',
                '1111_1' : 'https://i.imgur.com/tFUjH1W.gif'
            }[img_vector]
 

        output_img = img_selector(img_name)

        if(True):
            if(loop_num <= 4):
                dispatcher.utter_message(text=working_script)
                dispatcher.utter_message(text=recommendation_script, image=output_img)
                #dispatcher.utter_message(text='d',image=output_img)
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
        slot_bool = tracker.get_slot("Variables_bool")
        img_name = ''
        for i in slot_bool:
            img_name += str(i)
        if img_name == '1111':
            img_name += '_1'
        
        def img_selector(img_vector):
            return{
                '0000' : 'https://i.imgur.com/POsGGLf.gif',
                '1000' : 'https://i.imgur.com/70kfh8K.gif',
                '0100' : 'https://i.imgur.com/p3Ac0Fl.gif',
                '0010' : 'https://i.imgur.com/qCvk3N9.gif',
                '0001' : 'https://i.imgur.com/OIfpSHX.gif',
                '1100' : 'https://i.imgur.com/YmDVBUy.gif',
                '1010' : 'https://i.imgur.com/HYSBbz9.gif',
                '1001' : 'https://i.imgur.com/3SQ1xAK.gif',
                '0110' : 'https://i.imgur.com/K5KzdFf.gif',
                '0101' : 'https://i.imgur.com/qvIa80p.gif',
                '0011' : 'https://i.imgur.com/tjoOcfS.gif',
                '1110' : 'https://i.imgur.com/BnCbiXB.gif',
                '1101' : 'https://i.imgur.com/cUOdTCj.gif',
                '1011' : 'https://i.imgur.com/FNAvgc9.gif',
                '0111' : 'https://i.imgur.com/GuZ0kYh.gif',
                '1111_0' : 'https://i.imgur.com/rfn0a2z.gif',
                '1111_1' : 'https://i.imgur.com/tFUjH1W.gif'
            }[img_vector]

        output_img = img_selector(img_name)

        dispatcher.utter_message(text="See if I could do better...")
        dispatcher.utter_message(text='How do you like this one?', image=output_img)
        # dispatcher.utter_message(attachment=output_img)
        return []

class ActionTransAndStop(Action):
    def name(self) -> Text:
        return "transfer_to_human_and_stop_action"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text='Sorry for the inconvenience but the human customer service representatives deliberately lower my IQ to protect their jobs! I will turn you to them to get them busy now.')
        return []

        
        


class ActionSelfMockWhenWrong(Action):
    def name(self) -> Text:
        return "self_mockery_when_wrong_action"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


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
        new_variable = False
        if slot_list:
            for i in slot_names:
                if(i in slot_list and slot_temp_list[f(i)] != "HKUST"):
                    new_variable = True
                    break

        if (not new_variable):
            return []


        def f(x):
            return{
                'color' : 0,
                'sleeve_length': 1,
                'darkness': 2,
                'style': 3

            }[x]
        def f_scripts_num(x):
            return{
                'color' : 3,
                'darkness' : 1,
                'sleeve_length' : 1,
                'style' : 2
            }[x]
        def f_script(x):
            return{
                'color_0' : "Sorry for the poor eye sight, I find it's urgent to buy a better camera in order to support my color sensor ability. ",
                'color_1' : "Sorry for the poor color vision, I find it's urgent to upgrade the monitor in order to support my display ability. ",
                'color_2' : "Sorry for the wrong color, I guess I really need to buy a piece of RTX2060 to improve my color vision.",
                'color_3' : "Sorry for my poor color vision. I think it's time to get my GPU back. It was borrowed by someone for bitcoin mining.",
                'darkness_0' : "Sorry for the wrong darkness level, well let me just get out of the energy saving mode for better display brightness.",
                'darkness_1' : "Sorry for the wrong darkness level, well let me just bought a brighter screen for better display brightness.",
                'sleeve_length_0' : "Sorry for the wrong sleeve length, I guess I really need to buy a Sony camera to improve my eye sight. ",
                'sleeve_length_1' : "Sorry for that, I don't have limbs like human so please allow me to receive more feedback to get a concept of it. ",
                'style_0' : "Sorry for the poor fashion concept, I find it's urgent to update the database for new fashion in order to support my recognition skills.",
                'style_1' : "Sorry for the wrong style, I guess I really need to train on latest fashion dataset for the neural network to refresh my fashion concept.",
                'style_2' : "Sorry for that, I don't have personality like human because I was made by assembly line so please allow me to do it by trial and error to get a concept of it."
            }[x]
        if slot_list:
            for i in slot_names:
                if(i in slot_list and slot_temp_list[f(i)] != "HKUST"):
                    description_variable = i
                    break
            if description_variable != None:
                rand_num = f_scripts_num(description_variable)
                input_var = description_variable + '_' + str(random.randint(0, rand_num))
                mockery_script = f_script(input_var)
            else:
                mockery_script = 'Sorry for the mistake, it seems my stay up results in my poor memory today.'
        else:
            mockery_script = 'Sorry for the mistake, it seems my stay up results in my poor memory today.'
        dispatcher.utter_message(text=mockery_script)

        return []


class ActionSelfMockAbuse(Action):
    def name(self) -> Text:
        return "self_mockery_abuse_action"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        def f(x):
            return{
                0 : 'Yeah, so I do not have any salary for working all day long, how pool am I!',
                1 : 'Sorry, but everyone seems to be under pressure recently, you work 996 but I work 007, DAMN capitalism!',
                2 : 'Please not be that mean. I have been working so long that I think I got a fever. CPU overheated, but still tons of work to do.'
            }[x]
        rand_num = random.randint(0, 2)
        message = f(rand_num)
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

# class ActionHaha(Action):
#     def name(self) -> Text:
#         return "haha_action"
        
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         num = tracker.get_slot("loop_num")
#         dispatcher.utter_message(text='$$$ This should be displayed if slot_was_set works properly and loop time is {}$$$'.format(num))

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

    
        
