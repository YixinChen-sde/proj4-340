import dns.resolver, dns.reversename
import socket

def get_dns_info(ipv4_address):
    rdns = []
    if not ipv4_address:
        return []
    for ipv4 in ipv4_address:
        domain_name = None
        try:
            name = dns.reversename.from_address(ipv4)
            temp = dns.resolver.resolve(name, "PTR")
            rdns_name = str(temp[0])
            if rdns_name[-1] == '.':
                rdns_name = rdns_name[:len(rdns_name) - 1]
                domain_name = rdns_name
        except Exception as e:
            pass
        if domain_name:
            if domain_name not in rdns:
                rdns.append(domain_name)
    return rdns