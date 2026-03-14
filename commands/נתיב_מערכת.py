import os

def execute(args):
    lines = []
    
    lines.append({"text": "🗺️ מציג את משתנה סביבת PATH...", "type": "sys-out"})

    try:
        path_variable = os.environ.get('PATH')
        
        if path_variable:
            lines.append({"text": "--- נתיבים ב-PATH ---", "type": "success"})
            # Split by os.pathsep (';' on Windows, ':' on Unix)
            for path in path_variable.split(os.pathsep):
                lines.append({"text": f"  {path}", "type": ""})
            lines.append({"text": "✅ הצגת נתיב מערכת הושלמה.", "type": "success"})
        else:
            lines.append({"text": "⚠️ משתנה סביבת PATH לא נמצא.", "type": "sys-out"})

    except Exception as e:
        lines.append({"text": f"❌ שגיאת מערכת בלתי צפויה: {e}", "type": "error"})
    
    return {"lines": lines}
