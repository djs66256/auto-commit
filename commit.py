import subprocess
import sys
import os
import argparse
import requests
from provider import get_provider, get_settings

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

def get_git_last_diff():
    # 获取 git diff HEAD HEAD~1 输出
    result = subprocess.run(['git', 'diff', 'HEAD~1', 'HEAD'], capture_output=True, text=True)
    return result.returncode, result.stdout

def git_add_all():
    result = subprocess.run(['git', 'add', '.'], capture_output=True, text=True)
    return result.returncode, result.stdout

def git_status():
    result = subprocess.run(['git', 'status', '--short'], capture_output=True, text=True)
    return result.returncode, result.stdout

def git_commit(message, *argv):
    result = subprocess.run(['git', 'commit', *argv, '-m', message], capture_output=True, text=True)
    return result.returncode, result.stdout

def system_prompt():
    prompt = f"""
    ## Role
    你是一位 Git 提交日志助手，用户会提供一个 git diff 的输出，你需要根据这个输出生成一个简洁明了的提交日志。

    ## Requirements
    提交日志应该满足以下要求：
    - 简洁明了，不要冗余，描述清楚功能修改及其目的，字数控制在 50 字以内
    - 始终使用中文
    - 使用现在时
    - 使用祈使语气
    - 使用特定的 commit 类型开头，保持提交信息头部简洁，不要带上任何文件名等其他信息
        - 使用 `feat:` 开头表示功能修改，大部分情况应该使用这个类型，除非明确的下面几种类型
        - 使用 `fix:` 开头表示 bug 等问题修复
        - 使用 `optimize:` 开头表示性能优化
        - 使用 `docs:` 开头表示文档相关

    ## Example
    ```
    feat: {{添加了某个功能}}
    fix: {{修复了某个 bug}}
    optimize: {{优化了某个性能}}
    docs: {{更新了某个文档}}
    ```

    ## Locale
    - zh-cn
    """
    return prompt


def regenerate_system_prompt():
    prompt = f"""
    ## Role
    你是一位 Git 提交日志助手，你需要根据用户输入的修改信息总结归纳生成一个简洁明了的提交日志，字数控制在 50 字以内。

    ## Requirements
    提交日志应该满足以下要求：
    - 简洁明了，不要冗余，描述清楚功能修改及其目的
    - 始终使用中文
    - 使用现在时
    - 使用祈使语气
    - 使用特定的 commit 类型开头，保持提交信息头部简洁，不要带上任何文件名等其他信息
        - 使用 `feat:` 开头表示功能修改，大部分情况应该使用这个类型，除非明确的下面几种类型
        - 使用 `fix:` 开头表示 bug 等问题修复
        - 使用 `optimize:` 开头表示性能优化
        - 使用 `docs:` 开头表示文档相关

    ## Example
    ```
    feat: {{添加了某个功能}}
    fix: {{修复了某个 bug}}
    optimize: {{优化了某个性能}}
    docs: {{更新了某个文档}}
    ```

    ## Locale
    - zh-cn
    """
    return prompt

def log(message, level=LogLevel.INFO):
    if level >= default_log_level:
        print(f"{message}")


class APIProvider:
    def generate_message(self, user_input: str, files: str, diff: str, last_diff: str) -> str:
        pass

    def summarize(self, user_input: str, files: str, diff: str, last_diff: str, long_message: str) -> str:
        pass

    def default_generate_prompt(self, user_input: str, files: str, diff: str, last_diff: str) -> str:
        return f'''
        User message:
        {user_input or ""}
        Files:
        {files}
        Diff:
        {diff or ""}
        {last_diff or ""}
        '''

class OllamaProvider(APIProvider):
    AC_OLLAMA_URL = os.getenv("AC_OLLAMA_URL", "http://localhost:11434")
    AC_OLLAMA_MODEL = os.getenv("AC_OLLAMA_MODEL", "qwen2.5-coder:7b")

    def generate_message(self, user_input: str, files: str, diff: str, last_diff: str) -> str:
        response = requests.post(f"{self.AC_OLLAMA_URL}/api/chat", json={
            "model": self.AC_OLLAMA_MODEL, 
            "messages": [
                {"role": "system", "content": system_prompt()},
                {"role": "user", "content": user_content}
            ],
            "stream": False
        })
        return response.json()["message"]["content"].replace("```", "")
    
    def summarize(self, user_input, files, diff, last_diff, long_message):
        response = requests.post(f"{self.AC_OLLAMA_URL}/api/chat", json={
            "model": self.AC_OLLAMA_MODEL, 
            "messages": [
                {"role": "system", "content": regenerate_system_prompt()},
                {"role": "user", "content": response_message}
            ],
            "stream": False
        })
        response_json = response.json()
        response_message = response_json["message"]["content"]
        response_message = response_message.replace("```", "")
        return response_message

class ChatGLMProvider(APIProvider):
    API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    API_TOKEN = os.getenv("AC_CHATGLM_API_TOKEN") 
    MODEL = os.getenv("AC_CHATGLM_MODEL", "glm-4-flash")

    def generate_message(self, user_input: str, files: str, diff: str, last_diff: str) -> str:
        print(f"{files} {diff} {last_diff}")
        user_content = self.default_generate_prompt(user_input, files, diff, last_diff)
        print(user_content)
        response = requests.post(
            self.API_URL, 
            headers={
                "Authorization": f"Bearer {self.API_TOKEN}"
            }, 
            json={
                "model": self.MODEL,
                "messages": [
                    {"role": "system", "content": system_prompt()},
                    {"role": "user", "content": user_content}
                ],
                "stream": False
            })
        print(response.json())
        return response.json()["message"]["content"].replace("```", "")

    def summarize(self, user_input, files, diff, last_diff, long_message):
        response = requests.post(
            self.API_URL, 
            headers={
                "Authorization": f"Bearer {self.API_TOKEN}"
            }, 
            json={
                "model": self.MODEL, 
                "messages": [
                    {"role": "system", "content": regenerate_system_prompt()},
                    {"role": "user", "content": response_message}
                ],
                "stream": False
            })
        return response.json()["message"]["content"].replace("```", "")


PROVIDERS = {
    "ollama": OllamaProvider(),
    "chatglm": ChatGLMProvider(),
}


# args: 
# -m commit: message
# -a add: add all files to git
# -v --verbose: log level, default is INFO
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI assistant for git commit")
    parser.add_argument("-p", "--provider", help="The chat api provider name")
    parser.add_argument("-m", "--message", required=False, help="The commit message")
    parser.add_argument("-a", "--add", action="store_true", help="Add all files to git")
    parser.add_argument("--amend", action="store_true", help="Amend the last commit")
    parser.add_argument("-v", "--verbose", action="store_true", help="Log level, default is INFO")
    args = parser.parse_args()

    if args.verbose:
        default_log_level = LogLevel.DEBUG
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
    
    if not args.amend:
        if files is None or len(files) == 0:
            log("No files to commit, we will exit now...", LogLevel.INFO)
            sys.exit(0)
      
    log(f"We will commit the following files: \n{files}", LogLevel.INFO)
    
    log("Now we will generate the diff messages...", LogLevel.INFO)
    return_code, diff_message = get_git_diff_staged()
    if return_code != 0:
        log("Failed to get git diff", LogLevel.ERROR)
        sys.exit(1)
    log(f"Diff message: {diff_message}", LogLevel.VERBOSE)
    log("Done!\n", LogLevel.INFO)

    last_diff_message = ""
    if args.amend:
        log("Now we will amend the last commit...", LogLevel.INFO)
        return_code, last_diff_message = get_git_last_diff()
        if return_code != 0:
            log("Failed to amend the last commit", LogLevel.ERROR)
            sys.exit(1)
        else:
            log(f"Last diff message: {last_diff_message}", LogLevel.DEBUG)

    settings = get_settings()
    provider_name = args.provider or settings.get("provider") or "ollama"
    provider = get_provider(provider_name)
    if provider is None:
        log(f"LLM provider {provider_name} not found", LogLevel.ERROR)
        sys.exit(1)

    log(f"Now we will generate the commit message using {provider_name}...", LogLevel.INFO)
    response_message = provider.generate_message(
        user_input = message,
        files = files, 
        diff = diff_message, 
        last_diff = last_diff_message)
    log(f"Response message: {response_message}", LogLevel.VERBOSE)
    if len(response_message) > 200:
        log("Message is too long, we will shorten it...", LogLevel.INFO)
        response_message = provider.summarize(
            user_input = message, 
            files = files, diff = diff_message, 
            last_diff = last_diff_message,
            long_message=response_message)
        log(f"Response message: {response_message}", LogLevel.VERBOSE)

    log("Done!\n", LogLevel.INFO)

    if message is not None and len(message) > 0:
        commit_message = message + "\n" + response_message
    else:
        commit_message = response_message
    commit_message = commit_message.strip()
    log(f"Commit message: \n{commit_message}\n", LogLevel.INFO)
    log("Now commit to git...", LogLevel.INFO)
    
    if args.amend:
        return_code, _ = git_commit(commit_message, '--amend')
    else:
        return_code, _ = git_commit(commit_message)
    if return_code != 0:
        log("Failed to commit", LogLevel.ERROR)
        sys.exit(1)
    log("Done!\n", LogLevel.INFO)
    log("Thank you for using AI assistant for git commit!", LogLevel.INFO)

