\# AutoStream AI Agent



\## How to run

1\. Clone this repository

2\. Run: pip install -r requirements.txt

3\. Create a .env file and add: ANTHROPIC\_API\_KEY=your-key-here

4\. Run: python agent.py



\## Architecture

This agent is built using LangChain and Claude Haiku. A simple state 

dictionary manages memory across conversation turns, tracking whether 

the user is in the lead collection flow and which fields have been 

collected. Intent detection uses the LLM to classify each message as 

GREETING, PRODUCT\_QUERY, or HIGH\_INTENT. RAG works by loading a local 

knowledge\_base.json file and passing it as context to the LLM. The 

mock\_lead\_capture tool only fires after all three fields are confirmed.



\## WhatsApp Deployment

To deploy on WhatsApp, I would use the WhatsApp Business API with a 

webhook. A Flask server would receive POST requests from WhatsApp, 

pass the message to agent\_respond(), and send the reply back via the 

API. State would move from an in-memory dictionary to a database like 

Redis, keyed by phone number so each user has their own conversation.

