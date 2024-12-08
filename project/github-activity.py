import subprocess
import json
import argparse

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
    args = parser.parse_args()

    events = fetch_user_events(args.username, args.type)
    
    if events:
        for event in events[:5]:  
            print(f"\nТип события: {event['type']}")
            print(f"Репозиторий: {event['repo']['name']}")
            print(f"Дата события: {event['created_at']}")
            if 'payload' in event and 'commits' in event['payload']:
                print(f"Количество коммитов: {len(event['payload']['commits'])}")
            print('-' * 40)
    else:
        print("Не удалось получить данные.")

if __name__ == "__main__":
    main()
