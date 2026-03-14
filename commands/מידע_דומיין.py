import socket
import re

def execute(args):
    lines = []
    
    if not args:
        lines.append({"text": "❌ שגיאה: יש לספק שם דומיין או כתובת IP לחיפוש.", "type": "error"})
        lines.append({"text": "דוגמה: מידע_דומיין google.com", "type": "sys-out"})
        lines.append({"text": "דוגמה: מידע_דומיין 8.8.8.8", "type": "sys-out"})
        return {"lines": lines}

    target = args[0]
    lines.append({"text": f"🌐 מאחזר מידע DNS עבור '{target}'...", "type": "sys-out"})

    try:
        # Check if target is an IP address
        if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", target):
            # Reverse DNS lookup (IP to hostname)
            hostname, _, ip_list = socket.gethostbyaddr(target)
            lines.append({"text": f"✅ חיפוש הפוך עבור IP: {target}", "type": "success"})
            lines.append({"text": f"  שם מארח: {hostname}", "type": ""})
            lines.append({"text": f"  כינויים: {', '.join(_)}", "type": ""}) # _ would contain aliases
            lines.append({"text": f"  כתובות IP: {', '.join(ip_list)}", "type": ""})
        else:
            # Forward DNS lookup (hostname to IP)
            ip_address = socket.gethostbyname(target)
            lines.append({"text": f"✅ חיפוש קדימה עבור דומיין: {target}", "type": "success"})
            lines.append({"text": f"  כתובת IP: {ip_address}", "type": ""})
            
            # Try to get all addresses if available (getaddrinfo returns a list of 5-tuples)
            # This is more verbose but provides more details
            try:
                addr_info = socket.getaddrinfo(target, None)
                lines.append({"text": "  כל הכתובות:", "type": ""})
                for res in addr_info:
                    family, socktype, proto, canonname, sa = res
                    lines.append({"text": f"    כתובת: {sa[0]} (משפחה: {family}, סוג שקע: {socktype})", "type": ""})
            except Exception:
                pass # ignore if getaddrinfo fails or is not available for some reason


    except socket.gaierror as e:
        lines.append({"text": f"❌ שגיאת חיפוש DNS: שם הדומיין/IP '{target}' לא נמצא או לא חוקי. {e}", "type": "error"})
    except Exception as e:
        lines.append({"text": f"❌ שגיאת מערכת בלתי צפויה: {e}", "type": "error"})
    
    return {"lines": lines}
