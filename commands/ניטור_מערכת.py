import subprocess
import os

def execute(args):
    lines = [{"text": "📊 מנטר מערכת בסגנון btop - תמונת מצב:", "type": "success"}]
    
    def create_bar(percent, width=20):
        # יוצר שורת התקדמות ויזואלית [||||------]
        filled = int(width * percent / 100)
        return "█" * filled + "░" * (width - filled)

    try:
        # 1. שליפת מידע מעבד (CPU)
        cpu_res = subprocess.check_output('wmic cpu get loadpercentage /value', shell=True).decode('cp862', errors='ignore')
        cpu_val = 0
        for line in cpu_res.splitlines():
            if 'LoadPercentage=' in line:
                cpu_val = int(line.split('=')[1].strip())
        
        cpu_bar = create_bar(cpu_val)
        lines.append({"text": f"🧠 מעבד:   [{cpu_bar}] {cpu_val}%", "type": "error" if cpu_val > 80 else ""})

        # 2. שליפת מידע זיכרון (RAM)
        mem_res = subprocess.check_output('wmic OS get FreePhysicalMemory,TotalVisibleMemorySize /value', shell=True).decode('cp862', errors='ignore')
        mem_data = {l.split('=')[0]: l.split('=')[1] for l in mem_res.splitlines() if '=' in l}
        
        total_mem = int(mem_data['TotalVisibleMemorySize'])
        free_mem = int(mem_data['FreePhysicalMemory'])
        used_mem_pct = int(((total_mem - free_mem) / total_mem) * 100)
        
        mem_bar = create_bar(used_mem_pct)
        lines.append({"text": f"💾 זיכרון:  [{mem_bar}] {used_mem_pct}%", "type": "success" if used_mem_pct < 70 else "yellow"})

        # 3. שליפת מידע דיסק קשיח (C:)
        disk_res = subprocess.check_output('wmic logicaldisk where "DeviceID=\'C:\'" get FreeSpace,Size /value', shell=True).decode('cp862', errors='ignore')
        disk_data = {l.split('=')[0]: l.split('=')[1] for l in disk_res.splitlines() if '=' in l}
        
        total_disk = int(disk_data['Size'])
        free_disk = int(disk_data['FreeSpace'])
        used_disk_pct = int(((total_disk - free_disk) / total_disk) * 100)
        
        disk_bar = create_bar(used_disk_pct)
        lines.append({"text": f"💽 אחסון C: [{disk_bar}] {used_disk_pct}%", "type": "sys-out"})

        # 4. רשימת 3 תהליכים מובילים
        lines.append({"text": "---------------------------------------", "type": ""})
        lines.append({"text": "🔝 שלושת התהליכים הכבדים ביותר:", "type": "yellow"})
        task_res = subprocess.check_output('tasklist /v /fi "MEMUSAGE gt 100000" /fo list', shell=True).decode('cp862', errors='ignore')
        
        # לוקח רק את שמות התהליכים הראשונים שמופיעים
        tasks = []
        for line in task_res.splitlines():
            if "Image Name:" in line:
                tasks.append(line.split(":")[1].strip())
            if len(tasks) >= 3: break
            
        for task in tasks:
            lines.append({"text": f"  • {task}", "type": ""})

    except Exception as e:
        return {"lines": [{"text": f"❌ שגיאה בשאיבת נתונים: {str(e)}", "type": "error"}]}

    return {"lines": lines}