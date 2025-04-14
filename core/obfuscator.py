import base64
import random
import string

def analyze_payload(payload):
    """Choose best obfuscation methods based on payload."""
    length = len(payload)
    if length < 50:
        return ["xor", "hex"]  # Lightweight buat payload pendek
    elif "python" in payload.lower():
        return ["base64", "reverse", "xor"]  # Heavy buat Python
    return random.sample(["base64", "xor", "reverse", "hex"], k=2)

def base64_encode(payload):
    return base64.b64encode(payload.encode()).decode()

def xor_encode(payload, key=None):
    if key is None:
        key = random.randint(1, 255)
    return ''.join(chr(ord(c) ^ key) for c in payload), key

def reverse_string(payload):
    return payload[::-1]

def hex_encode(payload):
    return payload.encode().hex()

def chain_encode(payload, methods=None):
    """Smart obfuscation with dynamic methods."""
    try:
        if not methods or methods == ["chain"]:
            methods = analyze_payload(payload)
        
        result = payload
        applied_methods = []
        keys = {}
        
        for method in methods:
            if method == "base64":
                result = base64_encode(result)
                applied_methods.append("base64")
            elif method == "xor":
                result, key = xor_encode(result)
                applied_methods.append("xor")
                keys["xor"] = key
            elif method == "reverse":
                result = reverse_string(result)
                applied_methods.append("reverse")
            elif method == "hex":
                result = hex_encode(result)
                applied_methods.append("hex")
        
        return result, applied_methods, keys
    except Exception as e:
        raise ValueError(f"[!] Error obfuscating payload: {str(e)}")

def decode_hint(methods, keys):
    """Generate professional decode hint."""
    hint = "[*] Decode Instructions:\n"
    for i, method in enumerate(reversed(methods), 1):
        if method == "base64":
            hint += f"  {i}. Run: `echo '<payload>' | base64 -d`\n"
        elif method == "xor":
            key = keys.get("xor", 42)
            hint += f"  {i}. XOR decode with key={key} (use custom script)\n"
        elif method == "reverse":
            hint += f"  {i}. Reverse string (e.g., Python: string[::-1])\n"
        elif method == "hex":
            hint += f"  {i}. Run: `echo '<payload>' | xxd -r -p`\n"
    return hint
