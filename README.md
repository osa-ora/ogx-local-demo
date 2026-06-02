# ogx-local-demo
Demo OGX on your local machine with Ollama.

---

## Installing Ollama

Make sure you install Ollama on your machine
Download the models you need.
```
brew install ollama
ollama pull {models you need}
//for example ollama pull llama3.2:3b and ollama pull deepseek-r1:8b
ollama list
ollama serve
```
---
## Installing OGX 

```
uv tool install --force 'ogx[starter]' --python 3.13 --with "huggingface_hub<0.26.0" --with "sentence-transformers>=2.6.0"
export OLLAMA_URL=http://localhost:11434/v1
ogx stack run starter
```

Note: before you start it, take a backup of the file: dynamic_module_utils.py

```
cp /Users/{your-user}/.local/share/uv/tools/ogx/lib/python3.13/site-packages/transformers/dynamic_module_utils.py /Users/{your-user}/.local/share/uv/tools/ogx/lib/python3.13/site-packages/transformers/dynamic_module_utils_old.py
```

And replace the following function body: 
```
def resolve_trust_remote_code(trust_remote_code, model_name, has_local_code, has_remote_code):
... function content ...
...
```
With this code:
```
def resolve_trust_remote_code(trust_remote_code, model_name, has_local_code, has_remote_code):
    print("DEBUG: resolve_trust_remote_code called for", model_name)
    print("DEBUG: trust_remote_code", trust_remote_code)
    return True
```

---
## Install JupyterLab

```
brew install jupyterlab
jupyter lab 
```

Then Open the notebooks in this reposiotry and start to execute the simple-ogx-ollama but make sure the models referenced in that file already installed in ollama.
This will show you how to run different models available in ollama as abstracted by OGX.

<img width="1173" height="690" alt="Screenshot 2026-06-02 at 9 47 56 PM" src="https://github.com/user-attachments/assets/cfed99e5-b6c6-4e6d-b984-c0f38d7827b3" />


Then to test the RAG demo, first generate the files (if not already generated) and feel free to modify or to add any additional files.
This is using the notebook: sample-files-creation.

Once create go to the rag notebook named: simple-ogx-ollama and enjoy executing abstracted simple RAG architecture using OGX.

<img width="1445" height="699" alt="Screenshot 2026-06-02 at 9 46 40 PM" src="https://github.com/user-attachments/assets/d221dab3-6ece-4a55-b5cf-4222e9e9cc95" />

---

