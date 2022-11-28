import subprocess

def get_rtt(ip_address, port):
    try:
        rtt_command = 'sh -c "time echo -e \'\\x1dclose\\x0d\' |timeout 2 telnet ' + ip_address + ' ' + port + '"'
        cmd_response = subprocess.check_output(rtt_command, timeout=5, stderr=subprocess.STDOUT, shell=True).decode(
            "utf-8")
        print(cmd_response)
        splitted_response = cmd_response.split("\n\n")
        flag = False
        for response in splitted_response:
            if response.find("real") != -1:
                flag = True
                temp_str = response.split("\n")[0]
                another_temp = temp_str.split("\t")[1]
                real_time_command = another_temp.split("m")[1]
                real_time_command = float(real_time_command[:len(real_time_command) - 1])
                real_time_command *= 1000
                return real_time_command
        if not flag:
            return float('inf')
    except Exception as ex:
        available_port = ["80", "22"]
        if port != "22":
            if port == "443":
                return get_rtt(ip_address, available_port[0])
            elif port == "80":
                return get_rtt(ip_address, available_port[1])
        else:
            return None

def get_rtt_info(ipv4_address):
    rtt_times = []
    for ipv4_addr in ipv4_address:
        rtt = get_rtt(ipv4_addr, "443")
        if rtt:
            rtt_times.append(rtt)
    if len(rtt_times) < 1:
        return None

    return [min(rtt_times), max(rtt_times)]
