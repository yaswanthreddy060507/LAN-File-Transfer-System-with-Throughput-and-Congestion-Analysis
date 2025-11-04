import socket, time

server = socket.socket()
server.bind(("0.0.0.0", 9999))
server.listen(1)

print("Waiting for connection...")
conn, addr = server.accept()
print("Connected:", addr)

file_name = conn.recv(1024).decode()
file_size = int(conn.recv(1024).decode())

print(f"Receiving {file_name} ({file_size} bytes)")

received = 0
start = time.time()

with open("received_"+file_name, "wb") as f:
    while True:
        data = conn.recv(8192)
        if not data:
            break
        f.write(data)
        received += len(data)
        speed = (received/(1024*1024)) / (time.time()-start)
        print(f"Received {received}/{file_size} bytes | {speed:.2f} Mbps", end="\r")

conn.close()
server.close()
print("\n✅ File received")
