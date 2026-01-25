# Assistant
Don' think I will do everything for you, but I can chat and generate images for you. Parental advice: be nice so you don't get hunted when AI takes over...

We use ollama to access any llm for chatting, easy setup is the main reason for choose ollama. For image generation, we use stable diffusion v1.5 which will be downloaded from the diffusers package, you dont need to bother about it. If you want to change the image generation model, change it in line 4 in [sd.py](backend/sd.py), do this only if you have enough GPU vram.

### Before starting the app:
1. install ollama from `https://ollama.com/download` according to your platform and install it 
    #### or 
    run this command `curl -fsSL https://ollama.com/install.sh | sh` in terminal/cmd/whatever you use
2. check if installed successfuly by `ollama --version` 
3. if version is displayed, then it means success, your parents are proud, fn
4. next pull the llm model you want to use like this: `ollama pull gemma3:1b`. I'm pulling gemma3:1b model because thats the only one my 8yrs old laptop can handle now, if you are rich pull any bigger models that you like. 
5. run the model now: `ollama run gemma3:1b`, this starts the chat in terminal, go ahead ask it a question. Also ollama exposes them to `http://localhost:11434/api/generate` which is used in the app for communication to the model. Dont bother going to this url in the browser, you are blocked already, lol
6. if you pulled any other model, then you should update the line 5 in [chat.py](backend/chat.py). Papa's money, huh?

### To start the project:
1. Activate python: `source fastapi-env/bin/activate`
2. change directory to backend and run: `uvicorn main:app --reload`
3. go to `localhost:8000/docs`


    ```PS: DON'T get offended by the sarcasm used here, its just for fun or my mood at the time of writing this. I am using my laptop of 8yrs with i7 7th gen, Nvidia GTX 1050 Ti 4GB and 16GB RAM, so I had to use the smallest working models to get this working, if you have a better pc, good for you, try out other bigger models and let me know how it feels to be high up in cloud 9!!!```