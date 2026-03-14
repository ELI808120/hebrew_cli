import os

def execute(args):
    lines = []
    
    if not args:
        lines.append({"text": "❌ שגיאה: יש לספק נתיב לקובץ יומן.", "type": "error"})
        lines.append({"text": "דוגמה: קרא_יומן my_log.txt", "type": "sys-out"})
        lines.append({"text": "דוגמה: קרא_יומן -n 10 my_log.txt", "type": "sys-out"})
        return {"lines": lines}

    num_lines = 10 # Default to last 10 lines
    file_path = None

    # Parse arguments for -n <num_lines>
    if len(args) >= 3 and args[0] == "-n":
        try:
            num_lines = int(args[1])
            file_path = args[2]
        except ValueError:
            lines.append({"text": "❌ שגיאה: הארגומנט אחרי '-n' חייב להיות מספר שלם.", "type": "error"})
            return {"lines": lines}
    elif len(args) == 1:
        file_path = args[0]
    else:
        lines.append({"text": "❌ שגיאה: ארגומנטים לא חוקיים.", "type": "error"})
        lines.append({"text": "דוגמה: קרא_יומן my_log.txt", "type": "sys-out"})
        lines.append({"text": "דוגמה: קרא_יומן -n 10 my_log.txt", "type": "sys-out"})
        return {"lines": lines}

    if not os.path.exists(file_path):
        lines.append({"text": f"❌ שגיאה: הקובץ '{file_path}' לא נמצא.", "type": "error"})
        return {"lines": lines}
    if not os.path.isfile(file_path):
        lines.append({"text": f"❌ שגיאה: '{file_path}' אינו קובץ.", "type": "error"})
        return {"lines": lines}

    lines.append({"text": f"📜 מציג את {num_lines} השורות האחרונות מ-'{file_path}'...", "type": "sys-out"})

    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            # Read all lines and then take the last N
            all_lines = f.readlines()
            
            for line in all_lines[-num_lines:]:
                lines.append({"text": line.strip(), "type": ""})
        
        lines.append({"text": "✅ הצגת יומן הושלמה.", "type": "success"})

    except PermissionError:
        lines.append({"text": f"❌ אין הרשאה לקרוא את הקובץ '{file_path}'.", "type": "error"})
    except Exception as e:
        lines.append({"text": f"❌ שגיאה בקריאת הקובץ '{file_path}': {e}", "type": "error"})
    
    return {"lines": lines}
