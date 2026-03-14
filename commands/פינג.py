import subprocess
import os
import re

def execute(args):
    # אם לא סופק יעד, נבדוק מול גוגל כברירת מחדל
    target = args[0] if args else "google.com"
    cmd = f"ping -n 4 {target}" if os.name == "nt" else f"ping -c 4 {target}"
    
    lines = [{"text": f"מבצע בדיקת תקשורת (Ping) לכתובת {target} עם 32 בתים של נתונים:", "type": "success"}]
    
    try:
        # הפעלת הפקודה וקבלת הפלט
        res = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
        # מנסים לפענח לפי הקידוד של ווינדוס באנגלית או בעברית
        try:
            output = res.decode('utf-8')
        except UnicodeDecodeError:
            output = res.decode('cp862', errors='ignore')
            
        # מעבר על כל שורה בפלט ותרגום חכם שלה
        for line in output.splitlines():
            line = line.strip()
            if not line:
                continue
                
            # 1. תרגום שורות תגובה (Reply from...)
            # Reply from 142.250.75.100: bytes=32 time=14ms TTL=110
            match_reply = re.search(r'Reply from ([\d\.]+): bytes=(\d+) time[=<](\d+ms) TTL=(\d+)', line, re.IGNORECASE)
            if match_reply:
                ip, bytes_size, time, ttl = match_reply.groups()
                translated = f"תשובה מ-{ip}: בתים={bytes_size} זמן={time} TTL={ttl}"
                lines.append({"text": translated, "type": ""})
                continue
                
            # תרגום חלופי למקרה שזה אומר "Request timed out"
            if "Request timed out" in line or "פג תוקפה של הבקשה" in line:
                lines.append({"text": "פג תוקפה של הבקשה (אין תגובה).", "type": "error"})
                continue
                
            # 2. תרגום שורות סטטיסטיקה
            # Ping statistics for 142.250.75.100:
            match_stats = re.search(r'Ping statistics for (.*):', line, re.IGNORECASE)
            if match_stats:
                ip = match_stats.group(1).strip()
                lines.append({"text": "", "type": ""}) # שורה ריקה ליופי
                lines.append({"text": f"סטטיסטיקת Ping עבור {ip}:", "type": "success"})
                continue
                
            # Packets: Sent = 4, Received = 4, Lost = 0 (0% loss)
            match_packets = re.search(r'Packets: Sent = (\d+), Received = (\d+), Lost = (\d+) \((.*) loss\)', line, re.IGNORECASE)
            if match_packets:
                sent, received, lost, loss_percent = match_packets.groups()
                translated = f"    מנות: נשלחו = {sent}, התקבלו = {received}, אבדו = {lost} ({loss_percent} אובדן)"
                # צבע לפי אובדן
                color = "error" if int(lost) > 0 else "sys-out"
                lines.append({"text": translated, "type": color})
                continue
                
            # 3. תרגום שורות זמנים
            # Approximate round trip times in milli-seconds:
            if "Approximate round trip times" in line:
                lines.append({"text": "זמני יציאה וחזרה משוערים במילי-שניות:", "type": "sys-out"})
                continue
                
            # Minimum = 14ms, Maximum = 20ms, Average = 16ms
            match_times = re.search(r'Minimum = (.*), Maximum = (.*), Average = (.*)', line, re.IGNORECASE)
            if match_times:
                min_time, max_time, avg_time = match_times.groups()
                translated = f"    מינימום = {min_time}, מקסימום = {max_time}, ממוצע = {avg_time}"
                lines.append({"text": translated, "type": "sys-out"})
                continue
                
            # התעלמות משורות כותרת מיותרות
            if "Pinging" in line:
                continue

        return {"lines": lines}
        
    except subprocess.CalledProcessError as e:
        # קורה אם הכתובת לא קיימת בכלל
        return {"lines": [
            {"text": f"שגיאה: לא ניתן לאתר את הכתובת '{target}'.", "type": "error"},
            {"text": "אנא בדוק את שם היעד ונסה שנית.", "type": "sys-out"}
        ]}
    except Exception as e:
        return {"lines": [{"text": f"שגיאת מערכת בלתי צפויה: {e}", "type": "error"}]}