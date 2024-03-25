from EmailSpoofing.app import create_app
import socket


if "__main__" == __name__:
    server_ip = socket.gethostbyname(socket.gethostname())
    print(f"[+] Open -> http://{server_ip}:4444")
    app = create_app()
    app.run(host=server_ip, port=4444)
