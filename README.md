# TCP File Transfer System
## description
This project demonstrates high-speed file transfer between two systems connected over a Wireless LAN (Wi-Fi) using TCP socket programming in Python.
It simulates real-world data transmission between a client and server, while performing network performance analysis in real time.
The project also features a live throughput graph plotted using matplotlib, enabling visualization of network bandwidth utilization, packet size impact, and congestion simulation.

## Project Execution Procedure
### Step 1: Setup Environment 
1.Install Python 3 (recommended ≥ 3.9).
2.Install required libraries:
```pip install matplotlib```
3.Connect both systems to the same WiFi network (wireless LAN).
### Step 2: Configure Server
1.Open the server_file.py on the receiver’s machine.
2.Run:
```python server_file.py```
3.The terminal will display:
``` waiting for connection... ```
### Step 3: Configure Client
1.On the sender's machine, open client_file.py.
2.In the code, set the correct SERVER_IP (the IP address of the server machine).
Example: ```SERVER_IP = "192.168.1.10"```
3.Run the client:
```python client_file.py```
4.Enter:
      File name to send (e.g., movie.mp4)
      Packet size (e.g., 8192)
      Enable or disable congestion (y/n)
### Step 4: Observe Real-Time Graph
The system dynamically displays a Live Network Throughput Graph (Mbps vs Time).
Key elements shown:
Blue Line: Live transmission speed
Dashed Line: Average throughput
Marker Point: Peak speed
### Step 5: Results & Analysis
After the transfer completes:
A graph image (e.g., speed_graph_8192B.png) is saved.
Terminal displays performance summary:
File Size
Total Time
Peak Speed
Average Speed
Packet Size
Congestion Mode
---
✅ File sent successfully!
📁 Graph saved: speed_graph_8192B.png

📊 Transfer Summary
----------------------------
File Size:        3950.23 MB
Total Time:       84.12 sec
Peak Speed:       71.6 Mbps ⚡
Average Speed:    58.2 Mbps
Packet Size:      8192 bytes
Packets Sent:     48210
Congestion Mode:  Disabled
----------------------------
---
