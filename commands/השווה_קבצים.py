import os
import difflib

def execute(args):
    lines = []
    
    if len(args) < 2:
        lines.append({"text": "❌ שגיאה: יש לספק נתיבים לשני קבצים להשוואה.", "type": "error"})
        lines.append({"text": "דוגמה: השווה_קבצים file1.txt file2.txt", "type": "sys-out"})
        return {"lines": lines}

    file1_path = args[0]
    file2_path = args[1]

    if not os.path.exists(file1_path):
        lines.append({"text": f"❌ שגיאה: הקובץ הראשון '{file1_path}' לא נמצא.", "type": "error"})
        return {"lines": lines}
    if not os.path.isfile(file1_path):
        lines.append({"text": f"❌ שגיאה: '{file1_path}' אינו קובץ.", "type": "error"})
        return {"lines": lines}

    if not os.path.exists(file2_path):
        lines.append({"text": f"❌ שגיאה: הקובץ השני '{file2_path}' לא נמצא.", "type": "error"})
        return {"lines": lines}
    if not os.path.isfile(file2_path):
        lines.append({"text": f"❌ שגיאה: '{file2_path}' אינו קובץ.", "type": "error"})
        return {"lines": lines}

    lines.append({"text": f"🆚 משווה בין '{file1_path}' ל-'{file2_path}'...", "type": "sys-out"})

    try:
        with open(file1_path, 'r', encoding='utf-8', errors='ignore') as f1:
            file1_lines = f1.readlines()
        with open(file2_path, 'r', encoding='utf-8', errors='ignore') as f2:
            file2_lines = f2.readlines()
        
        diff = difflib.unified_diff(
            file1_lines, file2_lines, fromfile=file1_path, tofile=file2_path, lineterm=''
        )

        diff_found = False
        lines.append({"text": "--- הבדלים בין הקבצים ---", "type": "success"})
        for line in diff:
            diff_found = True
            # difflib output lines start with ' ', '+', or '-'
            if line.startswith('+'):
                lines.append({"text": line, "type": "success"}) # Indicate addition with green-like
            elif line.startswith('-'):
                lines.append({"text": line, "type": "error"}) # Indicate removal with red-like
            else:
                lines.append({"text": line, "type": ""}) # Context or no change
        
        if not diff_found:
            lines.append({"text": "ℹ️ אין הבדלים בין הקבצים.", "type": "sys-out"})
        else:
            lines.append({"text": "✅ השוואת קבצים הושלמה.", "type": "success"})

    except PermissionError:
        lines.append({"text": "❌ אין הרשאה לקרוא אחד מהקבצים.", "type": "error"})
    except Exception as e:
        lines.append({"text": f"❌ שגיאת מערכת בלתי צפויה: {e}", "type": "error"})
    
    return {"lines": lines}
