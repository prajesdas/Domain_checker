import csv, signal, sys, shutil
import dns.resolver
from tqdm import tqdm

CSV_FILE = "domains.csv"
BACKUP_FILE = CSV_FILE + ".bak"
rows = []


def check_domain(domain: str) -> str:
    try:
        # Try A record
        dns.resolver.resolve(domain, 'A')
        return "taken"
    except (dns.resolver.NXDOMAIN, dns.resolver.NoNameservers):
        return "available"
    except dns.resolver.NoAnswer:
        # No A record; try AAAA
        try:
            dns.resolver.resolve(domain, 'AAAA')
            return "taken"
        except dns.resolver.NoAnswer:
            # No AAAA record; try CNAME
            try:
                dns.resolver.resolve(domain, 'CNAME')
                return "taken"
            except dns.resolver.NoAnswer:
                return "available"
    except dns.resolver.LifetimeTimeout:
        # Treat timeout as "available" or handle separately
        return "available"


def handle_sigint(sig, frame):
    global rows
    print("\nStopping... saving progress.")
    with open(CSV_FILE, "w", newline="") as f:
        csv.writer(f).writerows(rows)
    sys.exit(0)

def main():
    global rows
    # Make a backup before modifying
    shutil.copyfile(CSV_FILE, BACKUP_FILE)
    print(f"Backup saved to {BACKUP_FILE}")

    # Load CSV into memory
    with open(CSV_FILE, newline="") as f:
        rows = list(csv.reader(f))

    signal.signal(signal.SIGINT, handle_sigint)

    for i, row in enumerate(tqdm(rows, desc="Checking domains")):
        if row[1] == "unknown":
            row[1] = check_domain(row[0])
            print(f"{row[0]}: {row[1]}")

    with open(CSV_FILE, "w", newline="") as f:
        csv.writer(f).writerows(rows)

if __name__ == "__main__":
    main()
