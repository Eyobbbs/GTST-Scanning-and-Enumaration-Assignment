import socket
import time

def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.3)

        result = sock.connect_ex((ip, port))

        if result == 0:
            try:
                service = socket.getservbyport(port, "tcp")
            except:
                service = "unknown"

            print(f"[OPEN] Port {port:<5} Service: {service}")

        sock.close()

    except Exception as e:
        print(f"Error scanning port {port}: {e}")


def main():
    ip = input("Enter target IP address: ").strip()

    print(f"\nScanning {ip} on ports 1-1000...")
    start_time = time.time()

    for port in range(1, 1001):
        scan_port(ip, port)

    end_time = time.time()

    print(f"\nScan completed in {end_time - start_time:.2f} seconds.")


if __name__ == "__main__":
    main()