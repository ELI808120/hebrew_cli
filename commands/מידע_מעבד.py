import subprocess
import platform

def execute(args):
    lines = []
    
    lines.append({"text": "💻 מאחזר מידע על המעבד...", "type": "sys-out"})

    try:
        if platform.system() == "Windows":
            command = ["wmic", "cpu", "get", "Name,NumberOfCores,NumberOfLogicalProcessors", "/value"]
            process = subprocess.run(command, capture_output=True, text=True, check=True, encoding='utf-8')
            output = process.stdout.strip()

            cpu_info = {}
            for line in output.splitlines():
                line = line.strip()
                if "=" in line:
                    key, value = line.split("=", 1)
                    cpu_info[key.strip()] = value.strip()
            
            if cpu_info:
                lines.append({"text": "--- פרטי מעבד ---", "type": "success"})
                lines.append({"text": f"  שם מעבד: {cpu_info.get('Name', 'לא ידוע')}", "type": ""})
                lines.append({"text": f"  מספר ליבות פיזיות: {cpu_info.get('NumberOfCores', 'לא ידוע')}", "type": ""})
                lines.append({"text": f"  מספר מעבדים לוגיים: {cpu_info.get('NumberOfLogicalProcessors', 'לא ידוע')}", "type": ""})
                lines.append({"text": "✅ מידע מעבד נשלף בהצלחה.", "type": "success"})
            else:
                lines.append({"text": "⚠️ לא ניתן היה לאתר מידע על המעבד.", "type": "sys-out"})

        elif platform.system() == "Linux":
            command = ["lscpu"]
            process = subprocess.run(command, capture_output=True, text=True, check=True, encoding='utf-8', errors='ignore')
            output = process.stdout.strip()
            
            lines.append({"text": "--- פרטי מעבד (Linux lscpu) ---", "type": "success"})
            for line in output.splitlines():
                if "Model name:" in line: lines.append({"text": f"  שם מעבד: {line.split(':', 1)[1].strip()}", "type": ""})
                elif "CPU(s):" in line: lines.append({"text": f"  סה"כ מעבדים לוגיים: {line.split(':', 1)[1].strip()}", "type": ""})
                elif "Core(s) per socket:" in line: lines.append({"text": f"  ליבות לכל שקע: {line.split(':', 1)[1].strip()}", "type": ""})
                elif "Socket(s):" in line: lines.append({"text": f"  שקעים: {line.split(':', 1)[1].strip()}", "type": ""})
            lines.append({"text": "✅ מידע מעבד נשלף בהצלחה.", "type": "success"})
            
        elif platform.system() == "Darwin": # macOS
            name_cmd = ["sysctl", "-n", "machdep.cpu.brand_string"]
            cores_cmd = ["sysctl", "-n", "machdep.cpu.core_count"]
            logical_cmd = ["sysctl", "-n", "machdep.cpu.thread_count"]

            cpu_name = subprocess.run(name_cmd, capture_output=True, text=True, encoding='utf-8').stdout.strip()
            cpu_cores = subprocess.run(cores_cmd, capture_output=True, text=True, encoding='utf-8').stdout.strip()
            cpu_logical = subprocess.run(logical_cmd, capture_output=True, text=True, encoding='utf-8').stdout.strip()

            lines.append({"text": "--- פרטי מעבד (macOS) ---", "type": "success"})
            lines.append({"text": f"  שם מעבד: {cpu_name}", "type": ""})
            lines.append({"text": f"  ליבות פיזיות: {cpu_cores}", "type": ""})
            lines.append({"text": f"  מעבדים לוגיים: {cpu_logical}", "type": ""})
            lines.append({"text": "✅ מידע מעבד נשלף בהצלחה.", "type": "success"})

        else:
            lines.append({"text": "❌ שגיאה: מערכת הפעלה לא נתמכת כרגע עבור פקודה זו.", "type": "error"})
            lines.append({"text": f"  מערכת: {platform.system()}", "type": "sys-out"})

    except FileNotFoundError:
        lines.append({"text": "❌ שגיאה: הפקודה הנדרשת לא נמצאה. ודא שהיא מותקנת ובנתיב המערכת.", "type": "error"})
    except subprocess.CalledProcessError as cpe:
        lines.append({"text": f"❌ שגיאה בהפעלת פקודה: {cpe.stderr}", "type": "error"})
    except Exception as e:
        lines.append({"text": f"❌ שגיאת מערכת בלתי צפויה: {e}", "type": "error"})
    
    return {"lines": lines}
