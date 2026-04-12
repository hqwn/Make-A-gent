# How to set up the voice assistant framework/UI for you AI Agent

This is a super quick tutorial on how to set up the voice assistant/ UI framework for your AI Agent. If you want to set up the UI, you will also have to set up the voice assistant framework. Here's how you do it for Voice Assistant or/and the UI:

## Youtube Tutorial

If at any time something is confusing to you, or you want a quick YouTube tutorial on how to set this up, you can watch: https://youtu.be/mCsRr_MMr7w

---

### Install the requirements for the voice assistant/UI framework:

install all of the dependencies needed with pip using this command:

```bash
pip install -r requirements2.txt
```

### That's it for the voice assistant/UI framework setup! Here's how to use it:

If you want to just talk to your new AI Agent with the terminal, write **run_jarvis()** in the bottom of the Talk.py file and run it, but if you want the UI (which you should do in my opinion), Make sure it doesnt say run_jarvis() in the bottom of the Talk.py file, then just run the UI.py and visit http://127.0.0.1:7860 in your browser to use the UI, and thats it! Enjoy! You can change the wake word if you want, refer to https://github.com/dscripka/openWakeWord for more info on how to do that. Put your new model (if you want one) in the models folder and change the model name in the `Voice_assistant.py` file.

### How to use the voice assistant:
You will have to say Jarvis, then it will print/(for UI)say in the textbox, heard Jarvis when it hears the wake word. After that say your question, which it will also print out/write in the textbox, then it will print out the AI Agent's response, and also say it out loud!
