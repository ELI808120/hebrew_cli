import subprocess
import platform

def execute(args):
    lines = []
    
    if platform.system() != "Windows":
        lines.append({"text": "❌ שגיאה: פקודה זו נתמכת רק במערכת הפעלה Windows.", "type": "error"})
        return {"lines": lines}

    try:
        command = ["tasklist", "/FO", "CSV", "/NH"] # Output as CSV, no header
        process = subprocess.run(command, capture_output=True, text=True, check=True, encoding='utf-8')

        output = process.stdout.strip()
        
        lines.append({"text": "📝 רשימת תהליכים פעילים:", "type": "success"})
        lines.append({"text": "----------------------------------------------------", "type": "sys-out"})
        lines.append({"text": "{:<30} {:<10} {:<10} {:<10}".format("שם תהליך", "PID", "זיכרון (MB)", "שם משתמש"), "type": "sys-out"})
        lines.append({"text": "----------------------------------------------------", "type": "sys-out"})

        for line in output.splitlines():
            parts = line.strip().split('","')
            if len(parts) >= 6: # Ensure we have enough parts to parse
                image_name = parts[0].strip('"')
                pid = parts[1].strip('"')
                session_name = parts[2].strip('"') # Not currently used, but good to know
                session_num = parts[3].strip('"')  # Not currently used
                mem_usage_raw = parts[4].strip('"')
                user_name = parts[5].strip('"') # This is the "User Name" in tasklist

                # Convert memory usage from KB to MB and clean up
                try:
                    mem_usage_mb = float(mem_usage_raw.replace(',', '').replace(' K', '')) / 1024
                    mem_usage_display = f"{mem_usage_mb:.2f}"
                except ValueError:
                    mem_usage_display = "N/A"

                lines.append({"text": "{:<30} {:<10} {:<10} {:<10}".format(
                    image_name, pid, mem_usage_display, user_name), "type": ""})
            else:
                # Fallback for unexpected line formats
                lines.append({"text": line, "type": "sys-out"})
        
        lines.append({"text": "----------------------------------------------------", "type": "sys-out"})

    except FileNotFoundError:
        lines.append({"text": "❌ שגיאה: הפקודה 'tasklist' לא נמצאה. ודא שמערכת ההפעלה תקינה.", "type": "error"})
    except subprocess.CalledProcessError as cpe:
        lines.append({"text": f"❌ שגיאה בהפעלת tasklist: {cpe.stderr}", "type": "error"})
    except Exception as e:
        lines.append({"text": f"❌ שגיאת מערכת בלתי צפויה: {e}", "type": "error"})
    
    return {"lines": lines}
