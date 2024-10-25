import random
import string

def generate_large_payload(size=8192):
    """
    Gera um payload aleatório com dados de caracteres e números.
    """
    return {
        "data": ''.join(random.choices(string.ascii_letters + string.digits, k=size)),
        "list": [random.randint(0, 100) for _ in range(1000)],
        "nested": {
            "info": ''.join(random.choices(string.ascii_letters + string.digits, k=256)),
            "details": {
                "field1": random.random(),
                "field2": random.choice(['A', 'B', 'C']),
                "field3": ''.join(random.choices(string.ascii_letters, k=50))
            }
        }
    }

def generate_udp_payload(size=1024):
    """
    Gera um payload de tamanho fixo para ataques UDP.
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=size)).encode('utf-8')

def generate_tcp_payload():
    """
    Gera um payload básico para ataques TCP (como um SYN Flood não precisa de payloads grandes).
    """
    return None  # SYN Flood não usa payload, então retorna None.
