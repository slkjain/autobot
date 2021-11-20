# Autobot - An Auto Safety Chatbot built using RASA and NHTSA APIs
Autobot is an intelligent chatbot that provides information about automotive safety complaints and recall campaigns in the United States. Autobot code is compatible with Rasa Open Source version 2.8.0. Rasa is a popular open source framework for building chatbots. 
Autobot uses [NHTSA APIs](https://medium.com/@slkjain/exploring-public-apis-from-nhtsa-81cb7416e0fc) to query complaints and recall data based on Model Year, Make and Model. 

# Building and Running Autobot
Following are the build instructions for Windows. The process should be similar in other environments. 

1. Create a directory names 'Autobot'.

2. Create a virtual environment and install Rasa Open Source in the 'Autobot' directory. The documentation on how to install Rasa is be checked at [Rasa Docs](https://rasa.com/docs/rasa/installation/) . Please note that you do not need to do "rasa init" if you are directly downloading files from this git repository. Rasa X is also not required for building or testing this chatbot.

3. Open two command prompts (or Powershell terminals)

4. Navigate to the 'Autobot' directory

5. In one of the terminal window (command prompt), run following command:

``rasa train``

This will build the source and create a model in 'models' sub-folder under 'Autobot'.

6. Open the second terminal window and start the action server:

``rasa run actions``

7. Return to the first terminal window and start the Rasa server

``rasa run -m models --enable-api --cors "*"``

(Note: if you want to user Rasa shell then do not start a Rasa server using the above command. Instead use ``rasa shell`` and skip the next step.)

8. Open 'index.html' using a web browser (Chrome, Firefox or Safari). The webpage shall show a chat icon at the right-bottom corner. Click on the chat icon to start chatting with Autobot.

# Webchat Interface of Autobot
Webchat interface of Autobot is part of 'index.html' and it is based on [Rasa Webchat](https://github.com/botfront/rasa-webchat)

# Overview of the files

`data/nlu.yml` - contains NLU training data

`data/rules.yml` - contains rules training data

`data/stories.yml` - contains stories training data

`actions.py` - contains custom action/api code

`domain.yml` - the domain file, including bot response templates

`config.yml` - training configurations for the NLU pipeline and policy ensemble

`credentials.yml` - contains the credentials for the voice & chat platforms 

`endpoints.yml` - contains the different endpoints the bot can use

`index.html` - Webchat interface of Autobot
