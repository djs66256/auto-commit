# Auto commit

Auto commit is a AI assistant that helps you to commit your changes to git.

Using Ollama to generate the commit message.

## Install

1. Install Ollama
2. `ollama pull qwen2.5-coder:7b`
3. `pip install -r requirements.txt`

## Customize

```
export AC_OLLAMA_URL='http://your.ollama.server.url'
export AC_OLLAMA_MODEL='your.ollama.model.name'
```
 
## Usage

```bash
python commit.py -a -m "Your additional commit message"
```
