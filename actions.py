from typing import Any, Text, Dict, List, Union, Optional

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.events import AllSlotsReset
from rasa_sdk.events import SlotSet

import requests
import json
import os

#global variables
MAX_ERROR_ALLOWED = 3

input_error_count = 0
complaint_count = 0
crash_count = 0
fire_count = 0

recall_count = 0

list_summary_crash = []
list_summary_fire = []        
response = None
recall_response = None

class ValidateNhtsaForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_nhtsa_form"

    async def validate_ModelYear(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        global input_error_count
        if value:
            response = requests.get("https://api.nhtsa.gov/products/vehicle/modelYears?issueType=c" )
            if response.status_code == 200:
                results = response.json()['results']
                suggestedMY = ""
                for result in results:
                    data = result["modelYear"]
                    if data == value:
                        #model year is good... Let's present a list of makes or brands
                        responseNxt = requests.get(f"https://api.nhtsa.gov/products/vehicle/makes?modelYear={data}&issueType=c" )
                        if responseNxt.status_code == 200:
                            buttons =[]
                            resultsNxt = responseNxt.json()['results']
                            for resultNxt in resultsNxt:
                                mkNxt = resultNxt["make"]
                                buttons.append({"title": mkNxt, "payload": mkNxt})
                            dispatcher.utter_message(text="Please select the MAKE/BRAND:", buttons=buttons)
                        else:
                            dispatcher.utter_message("What is the Make or Brand name of the vehicle?")
                        return {"ModelYear": value}
                    else:
                        if suggestedMY == "":
                            suggestedMY += data    
                        else:                          
                            suggestedMY += (", " + data)     
                dispatcher.utter_message(f"Sorry. Model Year *{value}* could not be validated.")
                input_error_count += 1
                if input_error_count > MAX_ERROR_ALLOWED:
                    dispatcher.utter_message(f"Input errors exceeded {MAX_ERROR_ALLOWED}. Resetting all inputs.")
                    input_error_count = 0
                    return {"Model": None, "ModelYear": None, "Make": None}
                if suggestedMY != "":
                    dispatcher.utter_message(f"Possible values - {suggestedMY}.")
                return {"ModelYear": None}
            else:            
                dispatcher.utter_message(f"Sorry. It seems NHTSA APIs are not working.")
                return {"ModelYear": None}
        else:
            return {"ModelYear": None }


        
    async def validate_Make(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        global input_error_count
        if value:
            modelyear = tracker.get_slot("ModelYear")
            response = requests.get(f"https://api.nhtsa.gov/products/vehicle/makes?modelYear={modelyear}&issueType=c" )
            if response.status_code == 200:
                results = response.json()['results']
                suggestedMake = ""
                for result in results:
                    data = result["make"]
                    if data.upper() == value.strip().upper():
                        #make is good... Let's present a list of models
                        responseNxt = requests.get(f"https://api.nhtsa.gov/products/vehicle/models?modelYear={modelyear}&make={data}&issueType=c")
                        if responseNxt.status_code == 200:
                            buttons =[]
                            resultsNxt = responseNxt.json()['results']
                            for resultNxt in resultsNxt:
                                mdNxt = resultNxt["model"]
                                buttons.append({"title": mdNxt, "payload": mdNxt})
                            dispatcher.utter_message(text="Please select the MODEL:", buttons=buttons)
                        else:
                            dispatcher.utter_message("What is the Model of the vehicle?")
                        return {"Make": data.upper()}
                    else:
                        if suggestedMake == "":
                            suggestedMake += data    
                        else:                          
                            suggestedMake += (", " + data)    
                dispatcher.utter_message(f"Sorry. Make *{value}* could not be validated for {modelyear}.")
                input_error_count += 1
                if input_error_count > MAX_ERROR_ALLOWED:
                    dispatcher.utter_message(f"Input errors exceeded {MAX_ERROR_ALLOWED}. Resetting all inputs.")
                    input_error_count = 0
                    return {"Model": None, "ModelYear": None, "Make": None}
                if suggestedMake != "":
                    dispatcher.utter_message(f"Possible values - {suggestedMake}.")
                return {"Make": None}
            else:            
                dispatcher.utter_message(f"Sorry. It seems NHTSA APIs are not working.")
                return {"Make": None}
        else:
            return {"Make": None }

    async def validate_Model(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        global input_error_count
        if value:
            modelyear = tracker.get_slot("ModelYear")
            make = tracker.get_slot("Make")
            response = requests.get(f"https://api.nhtsa.gov/products/vehicle/models?modelYear={modelyear}&make={make}&issueType=c" )
            if response.status_code == 200:
                results = response.json()['results']
                suggestedModel = ""
                for result in results:
                    data = result["model"]
                    if data.upper() == value.strip().upper():
                        return {"Model": data.upper()}
                    else:
                        if suggestedModel == "":
                            suggestedModel += data    
                        else:                          
                            suggestedModel += (", " + data)    
                dispatcher.utter_message(f"Sorry. Model *{value}* could not be validated for {modelyear} {make}.")
                input_error_count += 1
                if input_error_count > MAX_ERROR_ALLOWED:
                    dispatcher.utter_message(f"Input errors exceeded {MAX_ERROR_ALLOWED}. Resetting all inputs.")
                    input_error_count = 0
                    return {"Model": None, "ModelYear": None, "Make": None}
                if suggestedModel != "":
                    dispatcher.utter_message(f"Possible values - {suggestedModel}.")
                return {"Model": None}
            else:            
                dispatcher.utter_message(f"Sorry. It seems NHTSA APIs are not working.")
                return {"Model": None}
        else:
            return {"Model": None }

class ActionSubmitResults(Action):
    def name(self) -> Text:
        return "action_submit_results"
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        infoType = tracker.get_slot("InfoType")
        make = tracker.get_slot("Make")
        modelyear = tracker.get_slot("ModelYear")
        model = tracker.get_slot("Model")

        if modelyear == None:
            modelyear = "2019"
        
        if make == None:
            dispatcher.utter_message(f"Please re-state your query by specifying make. I can not provide info without knowing make and model.")
            return [AllSlotsReset()]

        if model == None:
            dispatcher.utter_message(f"Please re-state your query by specifying model. I can not provide info without knowing make and model.")
            return [AllSlotsReset()]

        model_year = modelyear.strip() 

        if (infoType == "complaints"):
            global complaint_count
            global crash_count
            global fire_count
            global response
            global input_error_count

            input_error_count = 0 #reset all input errors if you have reached till here
            complaint_count = 0
            crash_count = 0
            fire_count = 0
            response = None

            global list_summary_crash
            global list_summary_fire
            list_summary_crash = []
            list_summary_fire = []        

            parameters = {
                "modelYear": model_year,
                "make": make,
                "model" :model
            }
            response = requests.get("https://api.nhtsa.gov/complaints/complaintsByVehicle", params=parameters )
            if response.status_code == 200:
                results = response.json()['results']
                for result in results:
                    complaint_count += 1
                    summary = result["summary"]
                    if result["crash"]:
                        crash_count += 1
                        list_summary_crash.append(summary)
                    if result["fire"]:
                        fire_count += 1
                        list_summary_fire.append(summary)

            dispatcher.utter_message(f"There are {complaint_count} complaint(s) in NHTSA database for {modelyear} {make} {model}.")

        if (infoType == "recalls"):
            global recall_count
            global recall_response
            recall_count = 0
            recall_response = None

            recall_response = requests.get(f"https://one.nhtsa.gov/webapi/api/Recalls/vehicle/modelyear/{model_year}/make/{make}/model/{model}?format=json")
            if recall_response.status_code == 200:
                results_recall = recall_response.json()['Results']
                for result in results_recall:
                    recall_count += 1

            dispatcher.utter_message(f"There are {recall_count} recall(s) in NHTSA database for {modelyear} {make} {model}.")

        if (infoType == "ratings"):
            rating_response = requests.get(f"https://api.nhtsa.gov/SafetyRatings/modelyear/{model_year}/make/{make}/model/{model}")
            if rating_response.status_code == 200:
                results_rating = rating_response.json()['Results']
                if len(results_rating) != 0: 
                    for result in results_rating:
                        vehicleDesc = result["VehicleDescription"]
                        vehicleId = result["VehicleId"]
                        rating_response_for_id = requests.get(f"https://api.nhtsa.gov/SafetyRatings/VehicleId/{vehicleId}")
                        if rating_response_for_id.status_code == 200:
                            if (len(rating_response_for_id.json()['Results']) != 0):
                                results_rating_for_id = rating_response_for_id.json()['Results'][0]
                                dispatcher.utter_message(f"* Following are the ratings for {vehicleDesc}")
                                dispatcher.utter_message(f"- OverallRating = {results_rating_for_id['OverallRating']}")
                                dispatcher.utter_message(f"- OverallFrontCrashRating = {results_rating_for_id['OverallFrontCrashRating']}")
                                dispatcher.utter_message(f"- FrontCrashDriversideRating = {results_rating_for_id['FrontCrashDriversideRating']}")
                                dispatcher.utter_message(f"- FrontCrashPassengersideRating = {results_rating_for_id['FrontCrashPassengersideRating']}")
                                dispatcher.utter_message(f"- OverallSideCrashRating = {results_rating_for_id['OverallSideCrashRating']}")
                                dispatcher.utter_message(f"- SideCrashDriversideRating = {results_rating_for_id['SideCrashDriversideRating']}")
                                dispatcher.utter_message(f"- SideCrashPassengersideRating = {results_rating_for_id['SideCrashPassengersideRating']}")
                                dispatcher.utter_message(f"- RolloverRating = {results_rating_for_id['RolloverRating']}")
                                dispatcher.utter_message(f"- RolloverPossibility = {results_rating_for_id['RolloverPossibility']}")
                                dispatcher.utter_message(f"- RolloverRating2 = {results_rating_for_id['RolloverRating2']}")
                                dispatcher.utter_message(f"- RolloverPossibility2 = {results_rating_for_id['RolloverPossibility2']}")
                                dispatcher.utter_message(f"- SidePoleCrashRating = {results_rating_for_id['SidePoleCrashRating']}")
                                dispatcher.utter_message("---")
                            else:
                                dispatcher.utter_message(f"Sorry. No ratings are available for {model_year} {make} {model}")
                else:
                    dispatcher.utter_message(f"Sorry. No ratings are available for {model_year} {make} {model}")

        if (infoType == "complaints" and complaint_count> 0) or (infoType == "recalls" and recall_count> 0):
            return [SlotSet("MoreDataAvailable", True)]
        else:
            return [SlotSet("MoreDataAvailable", False)]

class ActionMoreResults(Action):
    def name(self) -> Text:
        return "action_more_results"
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        infoType = tracker.get_slot("InfoType")
        if (infoType == "complaints"):
            if (crash_count > 0):
                dispatcher.utter_message(f"{crash_count} complaint(s) were related to crash.")
            else:
                dispatcher.utter_message("There were no crash related complaints.")
            
            if (fire_count > 0):
                dispatcher.utter_message(f"{fire_count} complaint(s) were related to fire.")
            else:
                dispatcher.utter_message("There were no fire related complaints.")

            results = response.json()['results']
            totalInjuries = 0
            for result in results:
                totalInjuries += result["numberOfInjuries"]
            
            if totalInjuries > 0 :
                dispatcher.utter_message(f"Total injuries reported: {totalInjuries}")
            else:
                dispatcher.utter_message(f"No injuries reported.")

            totalDeaths = 0
            for result in results:
                totalDeaths += result["numberOfDeaths"]
            
            if totalDeaths > 0:
                dispatcher.utter_message(f"Total fatalities(s) reported: {totalDeaths}")
            else:
                dispatcher.utter_message(f"No fatalities reported.")

            componentDict = {}
            for result in results:
                components = result["components"]
                component_list = components.split(",")
                for cmp in component_list:
                    if cmp.strip() in componentDict:
                        componentDict[cmp.strip()] += 1
                    else:
                        componentDict[cmp.strip()] = 1
            
            if (len(componentDict) > 0):
                max_key = max(componentDict, key=componentDict.get)
                max_value = max(componentDict.values())
                dispatcher.utter_message (f"Component {max_key} reported {max_value} time(s) in the complaints.")
                componentDict.pop(max_key, None)
            
            if (len(componentDict) > 0):
                max_key = max(componentDict, key=componentDict.get)
                max_value = max(componentDict.values())
                dispatcher.utter_message (f"Component {max_key} reported {max_value} time(s) in the complaints.")
                componentDict.pop(max_key, None)
            
            if (len(componentDict) > 0):
                max_key = max(componentDict, key=componentDict.get)
                max_value = max(componentDict.values())
                dispatcher.utter_message (f"Component {max_key} reported {max_value} time(s) in the complaints.")
                componentDict.pop(max_key, None)

            if crash_count>0:
                dispatcher.utter_message("---")
                dispatcher.utter_message("* Following is a sample crash related complaint *")
                dispatcher.utter_message(list_summary_crash[0])

            if fire_count>0:
                dispatcher.utter_message("---")
                dispatcher.utter_message("* Following is a sample fire related complaint *")
                dispatcher.utter_message(list_summary_fire[0])

            dispatcher.utter_message("---")

        if (infoType == "recalls" and recall_count > 0):
            dispatcher.utter_message("* Following is a sample recall campaign *")
            results_recall = recall_response.json()['Results']
            result = results_recall[0] #checking only the first recall campaign
            recall_num = result["NHTSACampaignNumber"]
            recall_cmp = result["Component"]
            recall_summary = result["Summary"]
            recall_consequence = result["Conequence"]
            dispatcher.utter_message(f"Recall Campaign Number {recall_num} issued for {recall_cmp} - ")
            dispatcher.utter_message(f"Recall Summary: {recall_summary}")     
            dispatcher.utter_message(f"Recall Consequence: {recall_consequence}")
            dispatcher.utter_message("---")  
        
        if (infoType == "ratings" or infoType == "vin"):
            dispatcher.utter_message(f"No more results available for ratings or vin.")

        return [AllSlotsReset()]

class ResetAllSlots(Action):
    def name(self) -> Text:
        return "action_reset_allslots"
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        return [AllSlotsReset()]

class SetInfoTypeComplaints(Action):
    def name(self) -> Text:
        return "action_set_infotype_complaints"
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        dispatcher.utter_message(f"OK. Let me get complaints data for you.")
        return [SlotSet("InfoType", "complaints")]

class SetInfoTypeRecalls(Action):
    def name(self) -> Text:
        return "action_set_infotype_recalls"
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        dispatcher.utter_message(f"OK. Let me get recall info for you.")
        return [SlotSet("InfoType", "recalls")]

class SetInfoTypeRatings(Action):
    def name(self) -> Text:
        return "action_set_infotype_ratings"
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        dispatcher.utter_message(f"OK. Let me get safety ratings for you.")
        return [SlotSet("InfoType", "ratings")]        

class SetInfoTypeVIN(Action):
    def name(self) -> Text:
        return "action_set_infotype_vin"
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        dispatcher.utter_message(f"OK. Let me get VIN details for you.")
        return [SlotSet("InfoType", "vin")]      

class ValidateVinForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_vin_form"

    async def validate_VIN(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        #Currently no validations are performed for VIN value
        return {"VIN": value} 

class ActionVINResults(Action):
    def name(self) -> Text:
        return "action_vin_results"
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        vin = tracker.get_slot("VIN")

        if vin == None:
            dispatcher.utter_message(f"Please provide a valid VIN.")
            return [AllSlotsReset()]

        vin = vin.strip() 
        vin_response = requests.get(f"https://vpic.nhtsa.dot.gov/api/vehicles/decodevin/{vin}?format=json" )
        if vin_response.status_code == 200:
            results = vin_response.json()['Results']
            for result in results:
                if (result["Value"] != "" and result["Value"] != None and result["Value"] != "Not Applicable"):
                    dispatcher.utter_message(f"{result['Variable']} = {result['Value']}")

        return [AllSlotsReset()]
