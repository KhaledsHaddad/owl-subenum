# 🦉 owl-subenum

**owl-subenum** is a fast and lightweight subdomain enumeration tool written in Python.  
It aggregates subdomains from multiple online sources and checks their HTTP(S) status.

Created by **KHALED.S.HADDAD**  
🌐 [https://khaledhaddad.tech](https://khaledhaddad.tech)

---

## 🔍 Features

- 📡 Queries public subdomain sources:
  - [crt.sh](https://crt.sh)
  - [BufferOver](https://dns.bufferover.run)
  - [RapidDNS](https://rapiddns.io)
- 📦 Cleans and deduplicates subdomain results
- 🌐 Checks live status (`HTTP` / `HTTPS`) with response code
- 💾 Saves output to `<domain>_subdomains.txt`
- ⚡ Fast and simple CLI usage

---

## 🛠️ Requirements

- Python 3.x
- `requests` module

Install the required library if needed:

```bash
pip install requests

