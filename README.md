# TCP File Transfer System
## description
This project demonstrates high-speed file transfer between two systems connected over a Wireless LAN (Wi-Fi) using TCP socket programming in Python.
It simulates real-world data transmission between a client and server, while performing network performance analysis in real time.
The project also features a live throughput graph plotted using matplotlib, enabling visualization of network bandwidth utilization, packet size impact, and congestion simulation.

## Project Execution Procedure
### Step 1: Setup Environment 
1.Install Python 3 (recommended ≥ 3.9).<br>
2.Install required libraries:<br>
```pip install matplotlib```<br>
3.Connect both systems to the same WiFi network (wireless LAN).<br>
### Step 2: Configure Server
1.Open the server_file.py on the receiver’s machine.<br>
2.Run:<br>
```python server_file.py```<br>
3.The terminal will display:<br>
``` waiting for connection... ```<br>
### Step 3: Configure Client<br>
1.On the sender's machine, open client_file.py.<br>
2.In the code, set the correct SERVER_IP (the IP address of the server machine).<br>
Example: ```SERVER_IP = "192.168.1.10"```<br>
3.Run the client:<br>
```python client_file.py```<br>
4.Enter:<br>
      File name to send (e.g., movie.mp4)<br>
      Packet size (e.g., 8192)<br>
      Enable or disable congestion (y/n)<br>
### Step 4: Observe Real-Time Graph<br>
The system dynamically displays a Live Network Throughput Graph (Mbps vs Time).<br>
Key elements shown:<br>
Blue Line: Live transmission speed<br>
Dashed Line: Average throughput<br>
Marker Point: Peak speed<br>
### Step 5: Results & Analysis<br>
After the transfer completes:<br>
A graph image (e.g., speed_graph_8192B.png) is saved.<br>
Terminal displays performance summary:<br>
     1.File Size<br>
     2.Total Time<br>
     3.Peak Speed<br>
     4.Average Speed<br>
     5.Packet Size<br>
     6.Congestion Mode<br>

```✅ File sent successfully!<br>
📁 Graph saved: speed_graph_8192B.png<br>
📊 Transfer Summary<br>
----------------------------
File Size:        3950.23 MB
Total Time:       84.12 sec
Peak Speed:       71.6 Mbps
Average Speed:    58.2 Mbps
Packet Size:      8192 bytes
Packets Sent:     48210
Congestion Mode:  Disabled
----------------------------
```
