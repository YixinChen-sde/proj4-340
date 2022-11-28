import socket
import ssl
import subprocess

def get_tls(hostname):
    supported_tls = []
    try:
        cmd_response = subprocess.check_output("nmap --script ssl-enum-ciphers -p 443 " + hostname, timeout=10, stderr=subprocess.STDOUT, shell=True).decode("utf-8")
        if "TLSv1.0" in cmd_response:
            supported_tls.append("TLSv1.0")
        if "TLSv1.1" in cmd_response:
            supported_tls.append("TLSv1.1")
        if "TLSv1.2" in cmd_response:
            supported_tls.append("TLSv1.2")
        if "SSLv2" in cmd_response:
            supported_tls.append("SSLv2")
        if "SSLv3" in cmd_response:
            supported_tls.append("SSLv3")
    except Exception as excep:
        pass
    return supported_tls