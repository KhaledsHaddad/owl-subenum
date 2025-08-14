#!/usr/bin/env python3
import sys
import requests
import re
import time

def from_crtsh(domain):
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            return list(set(entry['name_value'].lower() for entry in data))
    except:
        pass
    return []

def from_bufferover(domain):
    url = f"https://dns.bufferover.run/dns?q=.{domain}"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            raw = data.get("FDNS_A", []) + data.get("RDNS", [])
            subdomains = set()
            for item in raw:
                parts = item.split(",")
                for p in parts:
                    if domain in p:
                        subdomains.add(p.strip())
            return list(subdomains)
    except:
        pass
    return []

def from_rapiddns(domain):
    url = f"https://rapiddns.io/subdomain/{domain}?full=1"
    try:
        r = requests.get(url, timeout=10)
        subdomains = re.findall(r'>([a-zA-Z0-9\-_\.]+\.%s)<' % re.escape(domain), r.text)
        return list(set(subdomains))
    except:
        return []

def clean(subdomains, domain):
    cleaned = set()
    for sub in subdomains:
        sub = sub.strip().lower().replace("*.", "")
        if sub.endswith(domain) and re.match(r"^[a-z0-9\.\-\_]+$", sub):
            cleaned.add(sub)
    return sorted(cleaned)

def check_http_status(sub):
    urls = [f"http://{sub}", f"https://{sub}"]
    for url in urls:
        try:
            r = requests.get(url, timeout=5, verify=False)
            return f"{r.status_code} {url}"
        except:
            continue
    return "Unreachable"

def main():
    if len(sys.argv) != 2:
        print("Usage: owl-subenum <domain>")
        sys.exit(1)

    domain = sys.argv[1]
    print(f"Enumerating subdomains for {domain}...\n")

    results = []
    results += from_crtsh(domain)
    results += from_bufferover(domain)
    results += from_rapiddns(domain)

    all_subdomains = clean(results, domain)

    if all_subdomains:
        filename = f"{domain}_subdomains.txt"
        with open(filename, "w") as f:
            print(f"Found {len(all_subdomains)} subdomains:\n")
            for sub in all_subdomains:
                status = check_http_status(sub)
                line = f"{sub} => {status}"
                print(" -", line)
                f.write(line + "\n")
                time.sleep(0.3)
        print(f"\nResults saved to: {filename}")
    else:
        print("No subdomains found.")

if __name__ == "__main__":
    requests.packages.urllib3.disable_warnings()
    main()
