import ipaddress
import subprocess
import platform
import argparse
from concurrent.futures import ThreadPoolExecutor

CLASS_TO_CIDR = {
    "A": 8,
    "B": 16,
    "C": 24
}


def ping_host(ip):
    param = "-n" if platform.system().lower() == "windows" else "-c"

    result = subprocess.run(
        ["ping", param, "1", str(ip)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    return result.returncode == 0


def discover_hosts(gateway_ip, network_class):
    network_class = network_class.upper()

    if network_class not in CLASS_TO_CIDR:
        raise ValueError("Network class must be A, B, or C.")

    cidr = CLASS_TO_CIDR[network_class]

    network = ipaddress.ip_network(
        f"{gateway_ip}/{cidr}",
        strict=False
    )

    print(f"Scanning {network} ...")

    active_hosts = []

    with ThreadPoolExecutor(max_workers=100) as executor:
        results = executor.map(
            lambda host: (host, ping_host(host)),
            network.hosts()
        )

        for host, alive in results:
            if alive:
                active_hosts.append(str(host))
                print(f"[+] Host Alive: {host}")

    return active_hosts


def main():
    parser = argparse.ArgumentParser(
        description="Simple Host Discovery Tool"
    )

    parser.add_argument(
        "gateway_ip",
        help="Gateway IP address (e.g. 192.168.1.1)"
    )

    parser.add_argument(
        "network_class",
        choices=["A", "B", "C", "a", "b", "c"],
        help="Network class"
    )

    args = parser.parse_args()

    hosts = discover_hosts(
        args.gateway_ip,
        args.network_class
    )

    print("\nActive Hosts:")
    for host in hosts:
        print(host)


if __name__ == "__main__":
    main()