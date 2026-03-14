import subprocess
import platform
import re

def execute(args):
    lines = []
    
    if not args:
        lines.append({"text": "❌ שגיאה: יש לספק כתובת IP/שם מארח לפינג.", "type": "error"})
        lines.append({"text": "דוגמה: פינג_רציף google.com [מספר_פינגים]", "type": "sys-out"})
        return {"lines": lines}

    host = args[0]
    count = 4 # Default ping count
    if len(args) > 1:
        try:
            count = int(args[1])
            if count <= 0:
                lines.append({"text": "❌ שגיאה: מספר הפינגים חייב להיות מספר חיובי.", "type": "error"})
                return {"lines": lines}
        except ValueError:
            lines.append({"text": "❌ שגיאה: 'מספר_פינגים' חייב להיות מספר שלם.", "type": "error"})
            return {"lines": lines}

    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, str(count), host]

    lines.append({"text": f"📶 מבצע פינג ל-'{host}' ({count} פעמים)...", "type": "sys-out"})

    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
        
        while True:
            output_line = process.stdout.readline()
            if not output_line:
                break
            line = output_line.strip()
            if line:
                # Basic translation/summary for common ping outputs
                if "Reply from" in line or "bytes from" in line:
                    match = re.search(r"time=(\d+)ms", line)
                    if match:
                        lines.append({"text": f"✅ תגובה מ-{host}: זמן={match.group(1)}ms", "type": ""})
                    else:
                        lines.append({"text": f"✅ תגובה מ-{host}.", "type": ""})
                elif "Request timed out" in line or "Destination Host Unreachable" in line:
                    lines.append({"text": f"❌ פסק זמן לבקשה / יעד בלתי נגיש.", "type": "error"})
                elif "Ping statistics for" in line:
                    lines.append({"text": "📊 סטטיסטיקות פינג:", "type": "success"})
                elif "Packets: Sent" in line:
                    sent_match = re.search(r"Sent = (\d+), Received = (\d+), Lost = (\d+)", line)
                    if sent_match:
                        lines.append({"text": f"  נשלחו: {sent_match.group(1)}, התקבלו: {sent_match.group(2)}, אבדו: {sent_match.group(3)}", "type": "sys-out"})
                elif "Approximate round trip times" in line:
                    avg_match = re.search(r"Average = (\d+)ms", line)
                    if avg_match:
                        lines.append({"text": f"  זמן ממוצע: {avg_match.group(1)}ms", "type": "sys-out"})
                else:
                    lines.append({"text": line, "type": "sys-out"})

        process.wait() # Wait for the process to finish

        if process.returncode != 0 and process.stderr.read():
            lines.append({"text": f"❌ שגיאת פינג: {process.stderr.read().strip()}", "type": "error"})

    except FileNotFoundError:
        lines.append({"text": "❌ שגיאה: הפקודה 'ping' לא נמצאה. ודא שהיא מותקנת ובנתיב המערכת.", "type": "error"})
    except Exception as e:
        lines.append({"text": f"❌ שגיאת מערכת בלתי צפויה: {e}", "type": "error"})
    
    return {"lines": lines}
