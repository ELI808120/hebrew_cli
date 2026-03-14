def execute(args):
    lines = []
    
    if len(args) < 3:
        lines.append({"text": "❌ שגיאה: יש לספק פעולה (encrypt/decrypt), טקסט ומפתח.", "type": "error"})
        lines.append({"text": "דוגמה: הצפנה_פשוטה encrypt 'סוד' 'מפתח'", "type": "sys-out"})
        lines.append({"text": "דוגמה: הצפנה_פשוטה decrypt '....' 'מפתח'", "type": "sys-out"})
        return {"lines": lines}

    action = args[0].lower()
    text = args[1]
    key = args[2]

    lines.append({"text": f"🔐 מבצע {action} טקסט באמצעות הצפנת XOR...", "type": "sys-out"})

    try:
        if not key:
            lines.append({"text": "❌ שגיאה: מפתח ההצפנה אינו יכול להיות ריק.", "type": "error"})
            return {"lines": lines}

        # Simple XOR encryption/decryption
        # Key is repeated if shorter than text
        encrypted_decrypted_text_chars = []
        for i in range(len(text)):
            char_code = ord(text[i])
            key_char_code = ord(key[i % len(key)])
            
            xor_result = char_code ^ key_char_code
            encrypted_decrypted_text_chars.append(chr(xor_result))
        
        result = "".join(encrypted_decrypted_text_chars)

        if action == "encrypt":
            lines.append({"text": f"✅ הטקסט המוצפן: '{result}'", "type": "success"})
            lines.append({"text": "⚠️ אזהרה: זוהי הצפנה פשוטה מאוד ואינה מאובטחת לשימוש אמיתי.", "type": "sys-out"})
        elif action == "decrypt":
            lines.append({"text": f"✅ הטקסט המפוענח: '{result}'", "type": "success"})
            lines.append({"text": "⚠️ אזהרה: זוהי הצפנה פשוטה מאוד ואינה מאובטחת לשימוש אמיתי.", "type": "sys-out"})
        else:
            lines.append({"text": "❌ שגיאה: פעולה לא חוקית. השתמש ב-'encrypt' או 'decrypt'.", "type": "error"})

    except Exception as e:
        lines.append({"text": f"❌ שגיאת מערכת בלתי צפויה: {e}", "type": "error"})
    
    return {"lines": lines}
