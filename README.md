# About

Things that I would like to have in an interface for LLMs:

- the ability to use speech to text on the desktop along with easy linking/loading of local files
- the ability to quickly direct bots to websites to provide context for questions (low priority)
- maintain multiple bots along with histories of their prompts.
    - If I experiment with a tweak to a prompt, I want to be able to quickly restore to a previous version if that prompt doesn't seem to be working well
- maintain multiple contexts that I can curate
    - I want to be able to select one or more contexts to inject into a given conversation
 
- automated summaries of ongoing conversations with the ability to purge older messages and replace with high level summaries
- storage of all chat history for searching /modification/training in the future
- checks on speech-to-text that can autoformat (via dedicated bots) to maintain clarity of conversation even if my engagement is more conversational.
- interface for multiple models
- tracking of current active context length with presentation of approximate costs per message as conversation expands...

- have a project directory view for a given conversation and check/uncheck boxes to include them in the context of the conversation.


Some other notes about intended direction....

The open router keys are the only ones being used for interfacing with ChatBots

The OpenAI key is planned to be used for Whisper speech-to-text integration...

# License

This package is licensed under the permissive MIT license. Have at it if you like. Please note that it is uses--though does not modify--PySide6 which is licensed under [LGPL](https://www.gnu.org/licenses/lgpl-3.0.en.html). 
