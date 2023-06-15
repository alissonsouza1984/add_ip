import subprocess

def add_ip_address(ip_address, subnet_mask=None, gateway=None, dns_primary=None, dns_secondary=None):
    # Verifica a interface de rede disponível
    interfaces = subprocess.check_output(['ip', 'link', 'show']).decode('utf-8')
    interface_names = []

    for line in interfaces.split('\n'):
        if 'state UP' in line:
            interface_name = line.split(':')[1].strip()
            interface_names.append(interface_name)

    if not interface_names:
        print('Nenhuma interface de rede ativa encontrada.')
        return

    # Solicita ao usuário a escolha da interface de rede
    print('Interfaces disponíveis:')
    for i, name in enumerate(interface_names):
        print(f'{i}: {name}')

    choice = input('Digite o número da interface desejada: ')

    try:
        choice = int(choice)
        interface_name = interface_names[choice]
    except (ValueError, IndexError):
        print('Opção inválida. Saindo do programa.')
        return

    # Configura o endereço IP
    subprocess.run(['ip', 'addr', 'add', '{}/{}'.format(ip_address, subnet_mask), 'dev', interface_name])

    # Configura o gateway padrão
    if gateway is not None:
        gateway = ip_address[:-2] + '1'
        subprocess.run(['ip', 'route', 'add', 'default', 'via', gateway, 'dev', interface_name])

    # Configura os servidores DNS
    if dns_primary is not None and dns_secondary is not None:
        with open('/etc/resolv.conf', 'w') as file:
            file.write('nameserver {}\n'.format(dns_primary))
            file.write('nameserver {}'.format(dns_secondary))

    print('Endereço IP adicionado com sucesso.')


def remove_ip_address(ip_address):
    # Verifica a interface de rede disponível
    interfaces = subprocess.check_output(['ip', 'link', 'show']).decode('utf-8')
    interface_names = []

    for line in interfaces.split('\n'):
        if 'state UP' in line:
            interface_name = line.split(':')[1].strip()
            interface_names.append(interface_name)

    if not interface_names:
        print('Nenhuma interface de rede ativa encontrada.')
        return

    # Solicita ao usuário a escolha da interface de rede
    print('Interfaces disponíveis:')
    for i, name in enumerate(interface_names):
        print(f'{i}: {name}')

    choice = input('Digite o número da interface desejada: ')

    try:
        choice = int(choice)
        interface_name = interface_names[choice]
    except (ValueError, IndexError):
        print('Opção inválida. Saindo do programa.')
        return

    # Remove o endereço IP
    subprocess.run(['ip', 'addr', 'del', ip_address, 'dev', interface_name])

    print('Endereço IP removido com sucesso.')


# Solicita a escolha de adicionar, obter via DHCP ou remover um endereço IP
print('Digite (0) para adicionar um endereço IP estático:')
print('Digite (1) para obter IP via DHCP:')
print('Digite (2) para remover um endereço IP:')

choice = input('Opção selecionada: ')

if choice == '0':
    # Solicita o endereço IP
    ip_address = input('Digite o endereço IP: ')

    # Solicita a máscara de sub-rede
    subnet_mask_choice = input('Digite (0) para usar a máscara de sub-rede padrão (255.255.255.0), ou (1) para fornecer outra máscara: ')
    if subnet_mask_choice == '0':
        subnet_mask = '255.255.255.0'
    elif subnet_mask_choice == '1':
        subnet_mask = input('Digite a máscara de sub-rede: ')
    else:
        print('Opção inválida. Saindo do programa.')
        exit()

    # Solicita o gateway
    gateway_choice = input('Digite (0) para usar o gateway padrão ({}), ou (1) para fornecer outro gateway: '.format(ip_address[:-2] + '1'))
    if gateway_choice == '0':
        gateway = ip_address[:-2] + '1'
    elif gateway_choice == '1':
        gateway = input('Digite o gateway: ')
    else:
        print('Opção inválida. Saindo do programa.')
        exit()

    # Solicita os servidores DNS
    dns_primary = input('Digite o DNS primário: ')
    dns_secondary = input('Digite o DNS secundário: ')

    # Chama a função para adicionar o endereço IP
    add_ip_address(ip_address, subnet_mask, gateway, dns_primary, dns_secondary)

elif choice == '1':
    # Configura o IP via DHCP
    subprocess.run(['dhclient', '-v'])

elif choice == '2':
    # Solicita o endereço IP a ser removido
    ip_address = input('Digite o endereço IP a ser removido: ')

    # Chama a função para remover o endereço IP
    remove_ip_address(ip_address)

else:
    print('Opção inválida. Saindo do programa.')
