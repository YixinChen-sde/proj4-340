import subprocess
if __name__ == '__main__':
    result = subprocess.check_output(["nslookup", "northwestern.edu", "8.8.8.8"], timeout=2, stderr=subprocess.STDOUT).decode("utf -8")
    print(result)