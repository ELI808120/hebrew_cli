import subprocess
import platform
import re

def execute(args):
    lines = []
    
    if platform.system() != "Windows":
        lines.append({"text": "❌ שגיאה: פקודה זו נתמכת כרגע רק במערכת הפעלה Windows.", "type": "error"})
        return {"lines": lines}

    lines.append({"text": "📜 מאחזר את יומן אירועי האבטחה האחרונים...", "type": "sys-out"})

    try:
        # Use wevtutil to query the Security log for the last few events
        # We'll filter for recent events or limit the count to avoid overwhelming output
        # /q:"*[System[(Level=1 or Level=2 or Level=3 or Level=4) and TimeCreated[SystemTime>'2023-01-01T00:00:00Z']]]"
        # /c:5 to get last 5 events
        command = ["wevtutil", "qe", "Security", "/c:5", "/f:text"] # Query last 5 events in text format
        process = subprocess.run(command, capture_output=True, text=True, check=False, encoding='utf-8', errors='ignore')
        output = process.stdout.strip()
        stderr_output = process.stderr.strip()

        if process.returncode != 0:
            lines.append({"text": f"❌ שגיאה בהפעלת wevtutil: {stderr_output}", "type": "error"})
            return {"lines": lines}

        if not output:
            lines.append({"text": "⚠️ לא נמצאו אירועים ביומן האבטחה.", "type": "sys-out"})
            return {"lines": lines}

        lines.append({"text": "--- אירועי אבטחה אחרונים ---", "type": "success"})
        
        event_blocks = output.split("Event:") # Split output into individual event blocks
        for block in event_blocks:
            if not block.strip():
                continue
            
            event_details = {}
            for line in block.splitlines():
                line = line.strip()
                if not line: continue

                if line.startswith("Log Name:"):
                    event_details["יומן"] = line.split(":", 1)[1].strip()
                elif line.startswith("Source:"):
                    event_details["מקור"] = line.split(":", 1)[1].strip()
                elif line.startswith("Date:"):
                    event_details["תאריך"] = line.split(":", 1)[1].strip()
                elif line.startswith("Event ID:"):
                    event_details["מזהה אירוע"] = line.split(":", 1)[1].strip()
                elif line.startswith("Task Category:"):
                    event_details["קטגוריית משימה"] = line.split(":", 1)[1].strip()
                elif line.startswith("Level:"):
                    event_details["רמה"] = line.split(":", 1)[1].strip()
                elif line.startswith("User:"):
                    event_details["משתמש"] = line.split(":", 1)[1].strip()
                elif line.startswith("OpCode:"):
                    event_details["קוד פעולה"] = line.split(":", 1)[1].strip()
                elif line.startswith("Computer:"):
                    event_details["מחשב"] = line.split(":", 1)[1].strip()

            if event_details:
                lines.append({"text": "--------------------------------------------------------------------------------", "type": "sys-out"})
                lines.append({"text": f"  מזהה אירוע: {event_details.get('מזהה אירוע', 'N/A')}", "type": ""})
                lines.append({"text": f"  תאריך: {event_details.get('תאריך', 'N/A')}", "type": ""})
                lines.append({"text": f"  מקור: {event_details.get('מקור', 'N/A')}", "type": ""})
                lines.append({"text": f"  רמה: {event_details.get('רמה', 'N/A')}", "type": ""})
                lines.append({"text": f"  משתמש: {event_details.get('משתמש', 'N/A')}", "type": ""})
                lines.append({"text": f"  מחשב: {event_details.get('מחשב', 'N/A')}", "type": ""})
                # lines.append({"text": f"  קטגוריית משימה: {event_details.get('קטגוריית משימה', 'N/A')}", "type": ""})
                
        lines.append({"text": "--------------------------------------------------------------------------------", "type": "sys-out"})
        lines.append({"text": "✅ אחזור יומן אבטחה הושלם.", "type": "success"})

    except FileNotFoundError:
        lines.append({"text": "❌ שגיאה: הפקודה 'wevtutil' לא נמצאה. ודא שהיא קיימת בנתיב המערכת.", "type": "error"})
    except Exception as e:
        lines.append({"text": f"❌ שגיאת מערכת בלתי צפויה: {e}", "type": "error"})
    
    return {"lines": lines}
