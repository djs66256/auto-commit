import subprocess
import sys
import argparse

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
def log(message, level=LogLevel.INFO):
    if level >= default_log_level:
        print(f"{message}")

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
    parser.add_argument("-c", "--config", required=False, help="The external config. 'en'")
    parser.add_argument("-d", "--dry", action="store_true", help="Dry run, only print the commit message")
    parser.add_argument("-v", "--verbose", action="store_true", help="Log level, default is INFO")
    args = parser.parse_args()

    if args.verbose:
        default_log_level = LogLevel.DEBUG
    else:
        default_log_level = LogLevel.INFO

    ex_config = args.config

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
    provider = get_provider(provider_name, ex_config)
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
    
    if not args.dry:
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

