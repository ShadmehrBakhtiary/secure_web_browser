import dns.resolver
import socket
import ssl
import threading

def web_browse(domain):
    try:
        answers = dns.resolver.resolve(domain, 'A')
        ip_address = answers[0].to_text()
        
        context = ssl.create_default_context()
        with socket.create_connection((ip_address, 443)) as client_socket:
            secure_socket = context.wrap_socket(client_socket, server_hostname=domain)
            request_packet = f"GET / HTTP/1.1\r\nHost: {domain}\r\n\r\n"
            secure_socket.sendall(request_packet.encode())
            response = secure_socket.recv(8192)
            headers, _, content = response.partition(b'\r\n\r\n')
            print(f"Content from {domain}:\n{content.decode()}")
    except Exception as e:
        print(f"Error browsing {domain}: {e}")

domains = ["www.google.com", "www.yahoo.com", "www.bing.com"]

threads = []
for domain in domains:
    thread = threading.Thread(target=web_browse, args=(domain,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()