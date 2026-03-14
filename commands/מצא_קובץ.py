import os
import re

def execute(args):
    lines = []
    
    if len(args) < 2:
        lines.append({"text": "❌ שגיאה: יש לספק נתיב חיפוש (תיקייה) ותבנית שם קובץ.", "type": "error"})
        lines.append({"text": "דוגמה: מצא_קובץ . *.py", "type": "sys-out"})
        lines.append({"text": "דוגמה: מצא_קובץ /path/to/dir my_file.*", "type": "sys-out"})
        return {"lines": lines}

    search_path = args[0]
    pattern = args[1]
    
    if not os.path.exists(search_path):
        lines.append({"text": f"❌ שגיאה: נתיב החיפוש '{search_path}' לא נמצא.", "type": "error"})
        return {"lines": lines}
    if not os.path.isdir(search_path):
        lines.append({"text": f"❌ שגיאה: '{search_path}' אינו תיקייה. יש לספק תיקייה לחיפוש.", "type": "error"})
        return {"lines": lines}

    lines.append({"text": f"🔍 מחפש קבצים ב-'{search_path}' התואמים לתבנית '{pattern}'...", "type": "sys-out"})

    found_files = []
    try:
        # Convert glob-like pattern to regex pattern
        regex_pattern = pattern.replace('.', r'\.').replace('*', r'.*').replace('?', r'.')
        compiled_regex = re.compile(regex_pattern)

        for root, _, files in os.walk(search_path):
            for file in files:
                if compiled_regex.match(file):
                    found_files.append(os.path.join(root, file))
        
        if found_files:
            lines.append({"text": "--- קבצים שנמצאו ---", "type": "success"})
            for f in found_files:
                lines.append({"text": f, "type": ""})
            lines.append({"text": f"✅ נמצאו {len(found_files)} קבצים.", "type": "success"})
        else:
            lines.append({"text": "ℹ️ לא נמצאו קבצים התואמים לתבנית.", "type": "sys-out"})

    except PermissionError:
        lines.append({"text": f"❌ אין הרשאה לגשת לנתיב '{search_path}' או לתתי התיקיות שבו.", "type": "error"})
    except Exception as e:
        lines.append({"text": f"❌ שגיאת מערכת בלתי צפויה: {e}", "type": "error"})
    
    return {"lines": lines}
