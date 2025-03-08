from flask import Flask, jsonify
import nmap

app = Flask(__name__)

# Define network range to scan
NETWORK_RANGE = "192.168.0.0/24"
PORTS = "27017,9042,5432,3306"

def scan_databases():
    nm = nmap.PortScanner()
    print(f"Scanning {NETWORK_RANGE} on ports {PORTS}...")  # Debug info

    nm.scan(hosts=NETWORK_RANGE, arguments=f'-p {PORTS} --open')

    results = []
    for host in nm.all_hosts():
        for proto in nm[host].all_protocols():
            for port in nm[host][proto].keys():
                service_name = nm[host][proto][port].get("name", "unknown")
                print(f"Host: {host}, Port: {port}, Service: {service_name}")  # Debug output
                results.append({
                    "host": host,
                    "port": port,
                    "service": service_name
                })

    if not results:
        print("⚠️ No databases found! Check firewall and services.")
    
    return results


@app.route('/scan-databases', methods=['GET'])
def get_databases():
    data = scan_databases()
    return jsonify({"databases": data, "total": len(data)})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
