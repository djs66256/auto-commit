# Auto commit

Auto commit is a AI assistant that helps you to commit your changes to git.

Using LLM to generate the commit message.
 
## Usage

You can check the usage by:
```
python commit.py -h
```
```bash
usage: commit.py [-h] [-p PROVIDER] [-m MESSAGE] [-a] [--amend] [-v]

AI assistant for git commit

options:
  -h, --help            show this help message and exit
  -p PROVIDER, --provider PROVIDER
                        The chat api provider name
  -m MESSAGE, --message MESSAGE
                        The commit message
  -a, --add             Add all files to git
  --amend               Amend the last commit
  -v, --verbose         Log level, default is INFO
```

### Examples

Add all files and comit with all files:

```bash
python commit.py -a
```

If you don't like the message, you can re-generate by:

```bash
python commit.py -a --amend
```
## Install

You can check the usage of install.sh by:
```
sh install.sh -h 
```

```bash
Usage:  [-p provider] [-t token] -s -h
  -p provider: llm provider name, ollama/chatglm/deepseek
  -t token: api_key, you need an api_key to access the provider
  -s add alias 'gca=python commit.py -a' to bashrc
  -h help
```

`sh install.sh` will use Ollama as the default provider.

Or just simple:

```bash
# use local ollama
bash <(curl https://raw.githubusercontent.com/djs66256/auto-commit/refs/heads/master/install.sh) -s
```
```bash
# use api service of chatglm
bash <(curl https://raw.githubusercontent.com/djs66256/auto-commit/refs/heads/master/install.sh) -p chatglm -t {your_api_key} -s
```

### Alias

Recommend to add alias to your bashrc file. Or add alias to your gitconfig file.

```bash
You can add alias to bashrc:
  echo "alias gca=python3 /Users/daniel/auto-commit/commit.py -a" >> ~.bashrc
  source ~/.bashrc
```

## Customize

You can customize by editing the file at `~/.auto_commit/config.yaml`

### Prompt and language

You can modify the prompt and language by editing the file at `~/.auto_commit/config.yaml`, default language is Chinese.

```yml
base:
    generate_prompt: {prompt to generate commit message}
    summarize_prompt: {when the result of generate_prompt is too long for some reason, summarize it by this prompt}
```