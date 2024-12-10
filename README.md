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

Add to bashrc is recommended.

```
echo 'export AC_OLLAMA_URL=http://your.ollama.server.url' >> ~/.bashrc
source ~/.bashrc
```

> In macos, it maybe .bash_profile or .zshrc, depend on your terminal.
 
## Usage

```bash
python commit.py -a -m "Your additional commit message"
```

If you don't like the message, you can re-generate by:

```bash
python commit.py -a --amend
```