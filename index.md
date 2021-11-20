# Autobot - An Auto Safety Chatbot built using RASA
Autobot is an intelligent chatbot that provides information about automotive safety complaints and recall campaigns in the United States. Autobot uses state-of-the-art NLU (Natural Language Understanding) based on a Transformer model using in RASA. [RASA](https://rasa.com/) is a popular open source framework for building chatbots. 

Autobot uses [NHTSA APIs](https://medium.com/@slkjain/exploring-public-apis-from-nhtsa-81cb7416e0fc) to query complaints and recall data based on Model Year, Make and Model entered by the user while conversing with the chatbot.

# Things you can ask the bot

The bot can provide information about a vehicle's complaints and recalls. You can ask it to:
1. Show complaints data
2. Describe NHTSA 

# Showing complaints data
Webchat interface of Autobot is part of 'index.html'. Open 'index.html' in a web-browser.

<img src="/img/Chatbot_Interface1.JPG" alt="Chatbot Initial Screen" width="600"/>

Click on the chat icon at the bottom-left corner of the screen. It will open the chat window.

<img src="/img/Chatbot_Interface2.JPG" alt="Chatbot Welcome Screen" width="600"/>

The initial chat window shows possible chatbot services. The user can either directly click on an option or type their question as English text. If the text is typed, then it need not exactly match with the option text. The RASA NLU engine can map the user-typed text to an appropriate service of the chatbot. For example, if the user asks, "show me some vehicle complaints" then the NLU engine will map the user intent to "Show complaints data".

<img src="/img/Show_Complaints1.JPG" alt="Show me some vehicle complaints" width="200"/>

Based on this intent, Autobot will ask for relevant information such as model year to retrieve the complaints data.

<img src="/img/Ask_MY1.JPG" alt="Provide model year" width="200"/>

Say the user types the Model Year as 2018 then Autobot will present the list of all the Makes available in the NHTSA database for the model year 2018. 

<img src="/img/Ask_Make1.JPG" alt="Provide make" width="200"/>

The user can either select a make option from the presented makes or the user can type it as well. Here, the user typed 'nissan'.

<img src="/img/Ask_Model1.JPG" alt="Provide model" width="200"/>

Again, the user can either select an option or type manually. Selecting model as 'Altima' here shows following details -

<img src="/img/Show_Summary1.JPG" alt="Show summary" width="200"/>

For 2018 Nissan Altima, there exist 139 complaints and 2 recalls in NHTSA database. All of these details are queried at run time using [NHTSA Public APIs](https://medium.com/@slkjain/exploring-public-apis-from-nhtsa-81cb7416e0fc).

At this stage if the user wants to see more details, they can select YES. Once the user opts for more details, complaint counts related to crash and fire are shown. Total number of injuries and fatalities are also shown. The Autobot then lists top three components responsible for these complaints. A sample crash related and a fire related complaint text is shown. Additionally, a sample recall campaign is also listed.

> 8 complaint(s) were related to crash.

> There were no fire related complaints.

> Total injuries reported: 6

> No fatalities reported.

> Component SERVICE BRAKES reported 46 time(s) in the complaints.

> Component UNKNOWN OR OTHER reported 45 time(s) in the complaints.

> Component ELECTRICAL SYSTEM reported 26 time(s) in the complaints.

>+ Following is a sample crash related complaint *

> WHILE DRIVING HOME AND JUST ENTERING MY NEIGHBORHOOD, I NOTICED A LOW TIRE WARNING ON MY DASHBOARD. I LOOKED AT THE PRESSURE AND THERE WAS APPROXIMATELY 26 POUNDS STILL IN THE TIRE AND THE CLOSEST PLACE TO FILL UP WAS AT MY HOUSE. WHILE APPROACHING A RIGHT TURN IN THE NEIGHBORHOOD AND BECAUSE OF THE WINTER WEATHER CONDITIONS OF SNOW AND ICE ON THE ROAD, I SLOWED DOWN TO A CRAWL AND APPLIED MY BRAKE PRIOR TO AND WHILE TURNING. WHILE IN THE BEGINNING OF MY TURN, I INSTANTLY REALIZED THAT I HAD NO CONTROL OF MY CAR AND I SLID INTO A SNOW BANK ON THE SIDE OF THE ROAD...

>+ Following is a sample recall campaign *

> Recall Campaign Number 19V654000 issued for BACK OVER PREVENTION: SENSING SYSTEM: CAMERA -

> Recall Summary: Nissan North America, Inc. (Nissan) is recalling certain 2018-2019 Nissan Altima, Armada, Frontier, Kicks, Leaf, Maxima, Murano, NV, NV200, Pathfinder, Rogue, Rogue Sport, Sentra, Titan, Titan Diesel, Versa Note and Versa Sedan vehicles, as well as Infiniti Q50, Q60, QX30 and QX80 vehicles. Additionally included are 2019 Nissan GT-R and Taxi and Infiniti QX50, QX60, Q70, Q70L vehicles. The back-up camera and display settings can be adjusted such that the rear view image is no longer visible and the system will retain that setting the next time the vehicle is placed in reverse. As such, these vehicles fail to comply with the requirements of Federal Motor Vehicle Safety Standard (FMVSS) number 111, "Rear Visibility."

> Recall Consequence: The lack of an image in the back-up camera display increases the risk of a crash.

At the juncture, once the user thanks Autobot, it goes back to presenting initial options again. 

<img src="/img/Show_NoProblem1.JPG" alt="Acknowledge" width="200"/>

Here is a recorded session with Autobot -

<img src="/img/autobot1.gif" alt="Recorded session with Autobot" width="200"/>

Additionally, Autobot is capable of responding to weird "out-of-scope" questions thrown at it as well. The code for building Autobot is available in [Autobot Github Repository](https://github.com/slkjain/autobot).
