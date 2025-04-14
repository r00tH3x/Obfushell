import base64

def base64_encode(payload): return base64.b64encode(payload.encode()).decode()

def xor_encode(payload, key=42): return ''.join(chr(ord(c) ^ key) for c in payload)

def reverse_string(payload): return payload[::-1]

def chain_encode(payload, methods): result = payload for method in methods: if method == "base64": result = base64_encode(result) elif method == "xor": result = xor_encode(result) elif method == "reverse": result = reverse_string(result) return result

def decode_hint(methods): hints = [] for method in reversed(methods): if method == "base64": hints.append("base64 -d") elif method == "xor": hints.append("XOR decode (key=42)") elif method == "reverse": hints.append("reverse string") return " -> ".join(hints)
