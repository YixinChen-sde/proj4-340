import sys
import os
import time
import json
import subprocess
import re
from ipaddress import ip_address, IPv4Address
from requestHelper import get_server_info
from tls_getter import get_tls
from dnsHelper import get_dns_info
from rtt_helper import get_rtt_info
import maxminddb

def validIPAddress(IP: str) -> str:
        return "IPv4" if type(ip_address(IP)) is IPv4Address else "IPv6"

def get_ipv4_address(hostname):
    request = "nslookup -type=A "
    request += hostname + " " + "8.8.8.8"
    res_lst = []
    try:
        second = 2
        result = subprocess.check_output(request, timeout=second, stderr=subprocess.STDOUT).decode("utf-8")
    except:
        return None
    if "Name" in result:
        temp_output = result.split("\n\n")
        output = temp_output[1]
        response_output = output.split("\n")
        for line in response_output:
            if "Address" in line:
                ip_addr = line.split(" ")
                ip_address = ip_addr[1]
                print(ip_address)
                res_lst.append(ip_address)
        return res_lst

    return []

def get_ipv6_address(hostname):
    res = []
    request = "nslookup -type=AAAA " + hostname + " " + "208.67.222.222"
    seconds = 3
    try:
        result = subprocess.check_output(request, timeout=seconds, stderr=subprocess.STDOUT, shell=True).decode("utf-8")
    except:
        result = None

    if not result.__contains__("No answer"):
        split = result.split("\n\n")
        for each_split in split:
            if "Non-authoritative answer" in each_split:
                addresses = each_split.split("\n")
                addresses = addresses[1:]
                for i in range(len(addresses)):
                    each_address = addresses[i]
                    if "Address" in each_address:
                        ipv6_address = each_address.split(" ")
                        ipv6 = ipv6_address[-1]
                        if "\r" in ipv6:
                            ipv6.remove("\r")
                        res.append(ipv6)
        return res
    return []

def get_geo_info(reader, ip_address):
    location_lst = []
    for ip in ip_address:
        ip_location = ""
        db_response = reader.get(ip)
        if "subdivisions" in db_response:
            if "en" in db_response["subdivisions"][0]["names"]:
                ip_location += db_response["subdivisions"][0]["names"]["en"] + ", "
        if "city" in db_response:
            if "en" in db_response["city"]["names"]:
                ip_location += db_response["city"]["names"]["en"] + ", "
        if "country" in db_response:
            if "en" in db_response["country"]["names"]:
                ip_location += db_response["country"]["names"]["en"]
        if not location_lst.count(ip_location):
            location_lst.append(ip_location)
    return location_lst

def start_scanning(inputFileName, outputFileName):
    curr_path = os.getcwd() + "/" + inputFileName
    file = open(curr_path, "r")
    file_content = file.read().split("\n")
    file.close()

    db_reader = maxminddb.open_database("GeoLite2-City.mmdb")
    json_dict = {}
    for website in file_content:
        website_info = {}
        # scanner for scan time
        scan_time = time.time()
        # scanner for ipv4 address
        ipv4 = get_ipv4_address(website)
        # scanner for ipv6 address
        ipv6 = get_ipv6_address(website)
        # scanner for http server
        redirect_to_https, insecure_http, http_server, hsts = get_server_info(website)
        # scanner for tls version
        #tls_versions = get_tls(website)
        # scanner for rdns name
        rdns_name = get_dns_info(ipv4)
        # scanner for rtt
        rtt_range = get_rtt_info(ipv4)
        # scanner for geo location
        geo_location_lst = get_geo_info(db_reader, ipv4)

        website_info["scan_time"] = scan_time
        website_info["ipv4_addresses"] = ipv4
        website_info["ipv6_addresses"] = ipv6
        website_info["http_server"] = http_server
        website_info["redirect_to_https"] = redirect_to_https
        website_info["insecure_http"] = insecure_http
        website_info["hsts"] = hsts
        #website_info["tls_versions"] = tls_versions
        #website_info["root_ca"] = root_ca
        website_info["rdns_name"] = rdns_name
        website_info["rtt_range"] = rtt_range
        website_info["geo_locations"] = geo_location_lst

        json_dict[website] = website_info

    db_reader.close()
    with open(outputFileName, "w") as f:
        json.dump(json_dict, f, sort_keys=True, indent=4)

if __name__ == '__main__':
    inputfile, outputfile = sys.argv[1], sys.argv[2]
    curr_dir_path = os.getcwd()
    curr_path = curr_dir_path + "/" + inputfile
    if not os.path.exists(curr_path):
        print("The input file is not in the current directory")
    else:
        start_scanning(inputfile, outputfile)