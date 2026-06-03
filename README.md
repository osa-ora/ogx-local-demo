# OGX Demo on Your Local Environment
---

Llama Stack has evolved into **OGX**: https://github.com/ogx-ai/ogx

As described in the official documentation, OGX is much more than simple inference routing. It composes inference, storage, moderation, and orchestration into a single process—whether you run it as a server or import it as a library. Your agent can search a vector store, call a tool, apply moderation checks, and stream the response without requiring glue code or sidecar services (see: https://ogx-ai.github.io/).

In this tutorial, we will demonstrate how to spin up OGX on your local machine using Ollama to execute two foundational scenarios: simple model selection and a basic RAG pipeline.

---

## 1) Installing Ollama

1. Install Ollama on your machine.
2. Download the local LLM models you want to interact with.

```bash
brew install ollama

# Pull the models you want to use for the demo
ollama pull llama3.2:3b
ollama pull deepseek-r1:8b

# Verify your local inventory and start the engine
ollama list
ollama serve

```

You can validate that the Ollama service endpoint is alive using:

```bash
curl http://localhost:11434/api/tags | jq .

```

---

## 2) Installing OGX

Set up your Python runtime and package management tooling:

```bash
brew install python@3.13
brew install uv
```

Install openai and all necessary libraries, for example:
```
python3 -m pip install openai --break-system-packages
```

Install the OGX starter stack profile. We will bind it to your local Ollama instance:

```bash
uv tool install --force 'ogx[starter]' --python 3.13 --with "huggingface_hub<0.26.0" --with "sentence-transformers>=2.6.0"

export OLLAMA_URL=http://localhost:11434/v1
ogx stack run starter

```

> ⚠️ **Sanity Check:** Ensure the OGX gateway started successfully by querying its model routing index on port `8321`:
> ```bash
> curl http://localhost:8321/v1/models | jq .
> 
> ```

Also, once the OGX server is up and running, you can check the endpoints documentation by opening the following URL in your browser:

```
http://localhost:8321/docs
```


### 🛠️ Important Hugging Face Patch

To ensure local text embeddings route properly without remote execution safety flags blocking your scripts, apply this quick override to the `transformers` library utility file.

Take a backup of the target file first:

```bash
cp /Users/{your-user}/.local/share/uv/tools/ogx/lib/python3.13/site-packages/transformers/dynamic_module_utils.py /Users/{your-user}/.local/share/uv/tools/ogx/lib/python3.13/site-packages/transformers/dynamic_module_utils_old.py

```

Open `dynamic_module_utils.py` and replace the default body of `resolve_trust_remote_code` with a forced approval wrapper:

```python
def resolve_trust_remote_code(trust_remote_code, model_name, has_local_code, has_remote_code):
    print("DEBUG: resolve_trust_remote_code called for", model_name)
    print("DEBUG: trust_remote_code", trust_remote_code)
    return True

```

---

## 3) Install JupyterLab

Launch your local development workspace:

```bash
brew install jupyterlab
jupyter lab 

```

---

## 4) Run the Demo Notebooks

### Scenario A: Simple Model Selection

Open the `simple-ogx-ollama.ipynb` notebook. Ensure that the model strings referenced inside match the models you pulled during Step 1. This sequence demonstrates how seamlessly OGX abstracts model inference calls using standard API constructs.

<img width="1173" height="690" alt="Screenshot 2026-06-02 at 9 47 56 PM" src="https://github.com/user-attachments/assets/cfed99e5-b6c6-4e6d-b984-c0f38d7827b3" />

### Scenario B: Abstracted RAG Pipeline

*Note: This default starter setup utilizes the inline flat-file FAISS/Memory provider for lightweight, zero-configuration local file searching.*

1. Run the `sample-files-creation.ipynb` notebook first to generate your local reference `.txt` files. Feel free to edit or add your own content here!
2. Open the main RAG notebook `simple-rag-ogx-openai.ipynb` for OpenAI SDK or `simple-rag-ogx.ipynb` for REST APIs, execute the cells, and watch OGX automatically ingest, chunk, attach, and contextually search across your documents natively.

<img width="1483" height="728" alt="Screenshot 2026-06-03 at 10 04 44 AM" src="https://github.com/user-attachments/assets/cc4e9930-9dd5-4e6a-b6a9-559bb792f98a" />


This concludes our tutorial for local OGX installation.
