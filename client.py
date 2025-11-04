import socket, time, matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random
import os

SERVER_IP = "192.168.159.10"  # <<< change if needed
SERVER_PORT = 5001

speed_data = []
time_data = []
start_time = None
total_bytes_sent = 0
peak_speed = 0
avg_speed = 0
file_size = 0

# ====== USER INPUT =======
filename = input("Enter file name to send: ")
packet_size = int(input("Enter packet size (1024/4096/8192): "))
congestion = input("Enable congestion (packet drops)? (y/n): ").lower() == "y"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Connecting to server...")
client.connect((SERVER_IP, SERVER_PORT))

# Send metadata
file_size = os.path.getsize(filename)
client.send(filename.encode())
time.sleep(0.1)
client.send(str(file_size).encode())

start_time = time.time()

# Graph Setup
plt.ion()
fig, ax = plt.subplots()
ax.set_title("Live Network Throughput (TCP)")
ax.set_xlabel("Time (seconds)")
ax.set_ylabel("Speed (Mbps)")
line, = ax.plot([], [], label="Speed")
avg_line, = ax.plot([], [], linestyle="--", label="Average Speed")
peak_point, = ax.plot([], [], 'o', markersize=8, label="Peak Speed")
ax.legend()

def update_plot(i):
    if len(time_data) == 0: return
    ax.set_xlim(0, time_data[-1] + 1)
    ax.set_ylim(0, max(speed_data) + 2)
    line.set_data(time_data, speed_data)
    avg_line.set_data(time_data, [sum(speed_data)/len(speed_data)]*len(speed_data))
    peak_idx = speed_data.index(max(speed_data))
    peak_point.set_data([time_data[peak_idx]], [speed_data[peak_idx]])

    plt.pause(0.01)

ani = FuncAnimation(fig, update_plot, interval=300, cache_frame_data=False)


# ====== FILE SEND ======
with open(filename, "rb") as f:
    bytes_sent = 0
    prev_time = time.time()

    while bytes_sent < file_size:
        chunk = f.read(packet_size)
        if not chunk: break

        if congestion and random.random() < 0.15:  
            time.sleep(0.080)
            continue 

        client.send(chunk)
        bytes_sent += len(chunk)

        current = time.time()
        elapsed = current - prev_time
        total_elapsed = current - start_time

        if elapsed > 0:
            speed = (len(chunk) * 8 / elapsed) / 1e6  # Mbps
            speed_data.append(round(speed, 2))
            time_data.append(round(total_elapsed, 2))

        prev_time = current
        
        # Progress Bar %
        percent = (bytes_sent / file_size) * 100
        bar = int(percent // 2)
        print(f"\r[{ '█' * bar}{'.' * (50-bar)}] {percent:.2f}% | Speed: {speed:.2f} Mbps", end="")

print("\n✅ File sent successfully!")

total_time = time.time() - start_time
peak_speed = max(speed_data)
avg_speed = sum(speed_data)/len(speed_data)

# Save graph
graph_name = f"speed_graph_{packet_size}B.png"
plt.savefig(graph_name)
print(f"📁 Graph saved as: {graph_name}")

print("\n📊 Transfer Summary")
print("----------------------------")
print(f"File Size:        {file_size/1024:.2f} KB")
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
