import re
import os

def execute(args):
    lines = []
    
    if len(args) < 2:
        lines.append({"text": "❌ שגיאה: יש לספק תבנית חיפוש ונתיב לקובץ(ים).", "type": "error"})
        lines.append({"text": "דוגמה: חפש_בטקסט "מחרוזת" my_file.txt", "type": "sys-out"})
        lines.append({"text": "דוגמה: חפש_בטקסט -i "מחרוזת" *.log", "type": "sys-out"})
        return {"lines": lines}

    pattern_arg = args[0]
    file_paths = args[1:]
    case_sensitive = True
    
    # Check for -i (case-insensitive) argument
    if pattern_arg == "-i" and len(args) >= 3:
        case_sensitive = False
        pattern_arg = args[1]
        file_paths = args[2:]
    elif pattern_arg.startswith("-") and pattern_arg != "-i":
        lines.append({"text": f"❌ שגיאה: ארגומנט לא ידוע: {pattern_arg}", "type": "error"})
        lines.append({"text": "הארגומנטים הנתמכים כרגע הם -i (לא תלוי רישיות).", "type": "sys-out"})
        return {"lines": lines}

    try:
        flags = re.IGNORECASE if not case_sensitive else 0
        search_pattern = re.compile(pattern_arg, flags)
    except re.error as re_err:
        lines.append({"text": f"❌ שגיאה בתבנית ביטוי רגולרי: {re_err}", "type": "error"})
        return {"lines": lines}

    found_matches = False
    for file_path in file_paths:
        if not os.path.exists(file_path):
            lines.append({"text": f"⚠️ הקובץ '{file_path}' לא נמצא. מדלג.", "type": "sys-out"})
            continue
        if not os.path.isfile(file_path):
            lines.append({"text": f"⚠️ '{file_path}' אינו קובץ. מדלג.", "type": "sys-out"})
            continue

        lines.append({"text": f"🔎 מחפש ב-'{file_path}' עבור '{pattern_arg}'...", "type": "sys-out"})
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    if search_pattern.search(line):
                        lines.append({"text": f"  {file_path}:{line_num}: {line.strip()}", "type": ""})
                        found_matches = True
        except PermissionError:
            lines.append({"text": f"❌ אין הרשאה לקרוא את הקובץ '{file_path}'.", "type": "error"})
        except Exception as e:
            lines.append({"text": f"❌ שגיאה בקריאת הקובץ '{file_path}': {e}", "type": "error"})
    
    if not found_matches:
        lines.append({"text": "ℹ️ לא נמצאו התאמות.", "type": "sys-out"})
    else:
        lines.append({"text": "✅ חיפוש הסתיים.", "type": "success"})

    return {"lines": lines}
