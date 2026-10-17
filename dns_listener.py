
from scapy.all import DNS, DNSQR, sniff

# --- CONFIGURATION ---
TARGET_DOMAIN = "google.com"


def dns_listener(packet):
    if not packet.haslayer(DNS):
        return

    dns = packet[DNS]

    # qr = 0 means DNS query
    if dns.qr != 0 or not packet.haslayer(DNSQR):
        return

    query_name = (
        packet[DNSQR].qname.decode("utf-8")
        .rstrip(".")
        .lower()
    )

    if query_name == TARGET_DOMAIN.lower():
        print(f"[DNS QUERY] Requested domain: {query_name}")


def main():
    print("DNS Monitoring Lab Started")
    print(f"Monitoring queries for: {TARGET_DOMAIN}")
    print("Press Ctrl+C to stop.")

    sniff(
        filter="udp port 53",
        prn=dns_listener,
        store=False
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nDNS monitoring stopped.")
