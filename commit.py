import subprocess
import sys
import os
import argparse
import requests

class LogLevel:
    DEBUG = 0
    VERBOSE = 1
    INFO = 2
    ERROR = 3

default_log_level = LogLevel.INFO
def get_git_diff_staged():
    # 获取 git diff --staged 输出
    result = subprocess.run(['git', 'diff', '--staged'], capture_output=True, text=True)
    return result.returncode, result.stdout

def git_add_all():
    result = subprocess.run(['git', 'add', '.'], capture_output=True, text=True)
    return result.returncode, result.stdout

def git_status():
    result = subprocess.run(['git', 'status', '--short'], capture_output=True, text=True)
    return result.returncode, result.stdout

def git_commit(message):
    result = subprocess.run(['git', 'commit', '-m', message], capture_output=True, text=True)
    return result.returncode, result.stdout

def system_prompt():
    prompt = f"""
    你是一位 Git 提交日志助手，用户会提供一个 git diff 的输出，你需要根据这个输出生成一个简洁明了的提交日志。
    提交日志应该满足以下要求：
    - 简洁明了，不要冗余，描述清楚功能修改及其目的
    - 使用中文
    - 使用现在时
    - 使用祈使语气

    ## Example
    User:
    ```
    diff --git ...
    ```
    Assistant:
    ```
    [简洁明了的提交日志]
    ```

    - Locale: zh-cn
    """
    return prompt

def log(message, level=LogLevel.INFO):
    if level >= default_log_level:
        print(f"{message}")

# args: 
# -m commit: message
# -a add: add all files to git
# -v --verbose: log level, default is INFO
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI assistant for git commit")
    parser.add_argument("-m", "--message", required=False, help="The commit message")
    parser.add_argument("-a", "--add", action="store_true", help="Add all files to git")
    parser.add_argument("-v", "--verbose", action="store_true", help="Log level, default is INFO")
    args = parser.parse_args()

    AC_OLLAMA_URL = os.getenv("AC_OLLAMA_URL", "http://localhost:11434")
    AC_OLLAMA_MODEL = os.getenv("AC_OLLAMA_MODEL", "qwen2.5-coder:7b")

    if args.verbose:
        default_log_level = LogLevel.VERBOSE
    else:
        default_log_level = LogLevel.INFO

    message = args.message
    log(f"Your commit message: {message}", LogLevel.VERBOSE)
    
    if args.add:
        log("AI assistant for git commit, now start adding all files...", LogLevel.INFO)
        return_code, _ = git_add_all()
        if return_code != 0:
            log("Failed to add all files", LogLevel.ERROR)
            sys.exit(1)
        log("Done!\n", LogLevel.INFO)

    log("Now we will get the git status...", LogLevel.INFO)
    return_code, files = git_status()
    if return_code != 0:
        log("Failed to get git status", LogLevel.ERROR)
        sys.exit(1)
    log(f"We will commit the following files: \n{files}", LogLevel.INFO)
    
    log("Now we will generate the diff messages...", LogLevel.INFO)
    return_code, diff_message = get_git_diff_staged()
    if return_code != 0:
        log("Failed to get git diff", LogLevel.ERROR)
        sys.exit(1)
    log(f"Diff message: {diff_message}", LogLevel.VERBOSE)
    log("Done!\n", LogLevel.INFO)

    # use ollama to generate the commit message
    log("Now we will generate the commit message using ollama...", LogLevel.INFO)
    response = requests.post(f"{AC_OLLAMA_URL}/api/chat", json={
        "model": AC_OLLAMA_MODEL, 
        "messages": [
            {"role": "system", "content": system_prompt()},
            {"role": "user", "content": diff_message}
        ],
        "stream": False
    })

    response_json = response.json()
    response_message = response_json["message"]["content"]
    response_message = response_message.replace("```", "")

    log(f"Response message: {response_message}", LogLevel.VERBOSE)
    log("Done!\n", LogLevel.INFO)

    if message is not None and len(message) > 0:
        commit_message = message + "\n" + response_message
    else:
        commit_message = response_message
    commit_message = commit_message.strip()
    log(f"Commit message: {commit_message}", LogLevel.INFO)
    log("Now commit to git...", LogLevel.INFO)
    return_code, _ = git_commit(commit_message)
    if return_code != 0:
        log("Failed to commit", LogLevel.ERROR)
        sys.exit(1)
    log("Done!\n", LogLevel.INFO)
    log("Thank you for using AI assistant for git commit!", LogLevel.INFO)
