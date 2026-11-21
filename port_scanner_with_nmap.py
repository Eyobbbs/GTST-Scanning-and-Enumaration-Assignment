import nmap

target = input("Enter target IP: ")
ports = input("Enter ports (e.g. 22,80,443 or 1-1000): ")

scanner = nmap.PortScanner()
scanner.scan(target, ports)

for host in scanner.all_hosts():
    for proto in scanner[host].all_protocols():
        for port in scanner[host][proto]:
            info = scanner[host][proto][port]
            print(
                f"Port {port}: {info['state']} "
                f"Service: {info['name']}"
            )