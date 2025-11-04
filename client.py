import socket, time, matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random
import os

SERVER_IP = "192.168.159.10"
SERVER_PORT = 5001

speed_data = []
time_data = []
start_time = None
file_size = 0

filename = input("Enter file name to send: ")
packet_size = int(input("Enter packet size (1024/4096/8192): "))
congestion = input("Enable congestion (packet drops)? (y/n): ").lower() == "y"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.settimeout(5)

print("Connecting to server...")
client.connect((SERVER_IP, SERVER_PORT))

file_size = os.path.getsize(filename)
print(f"📦 File size: {file_size/1024/1024:.2f} MB")

client.send(filename.encode())
time.sleep(0.1)
client.send(str(file_size).encode())

start_time = time.time()

# ---------- GRAPH SETUP ----------
plt.ion()
fig, ax = plt.subplots()
ax.set_title("Live Network Throughput (TCP) – Smoothed")
ax.set_xlabel("Time (seconds)")
ax.set_ylabel("Speed (Mbps)")
ax.grid(True, linestyle="--", alpha=0.4)

line, = ax.plot([], [], label="Speed", linewidth=2)
avg_line, = ax.plot([], [], linestyle="--", label="Average Speed")
peak_point, = ax.plot([], [], 'o', markersize=8, label="Peak")
ax.legend()

def update_plot():
    if len(time_data) == 0: 
        return
    
    ax.set_xlim(0, time_data[-1] + 1)

    peak_speed = max(speed_data)
    ax.set_ylim(0, max(5, peak_speed + 2))  # Dynamic scaling

    line.set_data(time_data, speed_data)

    avg = sum(speed_data)/len(speed_data)
    avg_line.set_data(time_data, [avg] * len(time_data))

    pk = speed_data.index(peak_speed)
    peak_point.set_data([time_data[pk]], [peak_speed])

    plt.pause(0.01)


# ---------- FILE SEND ----------
with open(filename, "rb") as f:
    bytes_sent = 0
    prev = time.time()

    while bytes_sent < file_size:
        chunk = f.read(packet_size)
        if not chunk:
            break

        if congestion and random.random() < 0.15:
            time.sleep(0.08)
            continue

        client.send(chunk)
        bytes_sent += len(chunk)

        now = time.time()
        dt = now - prev
        total_t = now - start_time

        if dt > 0:
            speed = (len(chunk) * 8 / dt) / 1e6  # Mbps

            # -------- SMOOTHING + CLIP --------
            if speed_data:
                speed = speed_data[-1] * 0.6 + speed * 0.4
            speed = min(speed, 200)
            speed = round(speed, 2)

            speed_data.append(speed)
            time_data.append(round(total_t, 2))
            update_plot()

        prev = now

        percent = (bytes_sent / file_size) * 100
        bar = int(percent // 2)
        print(f"\r[{ '█' * bar}{'.' * (50-bar)}] {percent:.2f}% | {speed:.2f} Mbps", end="")

print("\n✅ File sent successfully!")

total_time = time.time() - start_time
peak_speed = max(speed_data)
avg_speed = sum(speed_data)/len(speed_data)

graph_name = f"speed_graph_{packet_size}B.png"
plt.savefig(graph_name)
print(f"📁 Graph saved: {graph_name}")

print("\n📊 Transfer Summary")
print("----------------------------")
print(f"File Size:        {file_size/1024/1024:.2f} MB")
print(f"Total Time:       {total_time:.2f} sec")
print(f"Peak Speed:       {peak_speed:.2f} Mbps ⚡")
print(f"Average Speed:    {avg_speed:.2f} Mbps")
print(f"Packet Size:      {packet_size} bytes")
print(f"Packets Sent:     {len(speed_data)}")
print(f"Congestion Mode:  {'Enabled' if congestion else 'Disabled'}")
print("----------------------------")

plt.ioff()
plt.show()
client.close()