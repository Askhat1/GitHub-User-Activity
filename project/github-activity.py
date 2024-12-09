import subprocess
import json
import argparse

def is_gh_installed():
    try:
        subprocess.run(["gh", "--version"], capture_output=True, text=True, check=True)
        return True
    except FileNotFoundError:
        print("Ошибка: GitHub CLI не установлена. Установите её перед использованием скрипта")
        return False
def fetch_user_events(username, event_type=None):
    try:
        result = subprocess.run(
            ["gh", "api", f"users/{username}/events"],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print("Ошибка: ", result.stderr)
            return None
        
        events = json.loads(result.stdout)

        if event_type:
            events = [event for event in events if event['type'] == event_type]

        return events
    except Exception as e:
        print(f"Ошибка: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Получить активность пользователя GitHub.")
    parser.add_argument("username", help="Имя пользователя GitHub")
    parser.add_argument("-t", "--type", help="Фильтр по типу события (например, PushEvent, IssuesEvent, WatchEvent)")
    parser.add_argument("-n", "--number", type=int, default=5, help="Количество выводимых событий (по умолчанию 5)")
    args = parser.parse_args()

    events = fetch_user_events(args.username, args.type)
    
    if events:
        output = []  
        for event in events[:args.number]:
            if event['type'] == 'PushEvent':
                commits_count = len(event['payload']['commits']) if 'payload' in event and 'commits' in event['payload'] else 0
                output.append(f"Pushed {commits_count} commit(s) to {event['repo']['name']}")
            elif event['type'] == 'IssuesEvent':
                output.append(f"Opened a new issue in {event['repo']['name']}")
            elif event['type'] == 'WatchEvent':
                output.append(f"Starred {event['repo']['name']}")
            else:
                output.append(f"Performed {event['type']} in {event['repo']['name']}")

        print("\n".join(output))
    else:
        print("Не удалось получить данные.")

if __name__ == "__main__":
    main()
