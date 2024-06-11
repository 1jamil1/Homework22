import socket
import threading

accounts = {
    '1234': {'pin': '1234', 'balance': 1000.0},
    '12345': {'pin': '12345', 'balance': 2000.0},
}

def handle_client(client_socket, accounts):
    try:
        client_socket.sendall(b'Welcome to the Bank ATM!\n')
        client_socket.sendall(b'Enter account number: ')
        account_number = client_socket.recv(1024).decode().strip()

        if account_number not in accounts:
            client_socket.sendall(b'Invalid account number.\n')
            client_socket.close()
            return

        client_socket.sendall(b'Enter PIN: ')
        pin = client_socket.recv(1024).decode().strip()

        if accounts[account_number]['pin'] != pin:
            client_socket.sendall(b'Invalid PIN.\n')
            client_socket.close()
            return

        client_socket.sendall(b'Authenticated successfully.\n')
        handle_transactions(client_socket, account_number, accounts)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

def handle_transactions(client_socket, account_number, accounts):
    while True:
        client_socket.sendall(b'\nChoose an option:\n1. Check Balance\n2. Deposit\n3. Withdraw\n4. Exit\n')
        option = client_socket.recv(1024).decode().strip()

        if option == '1':  # Check balance
            balance = accounts[account_number]['balance']
            client_socket.sendall(f'Your balance is: ${balance}\n'.encode())

        elif option == '2':  # Deposit
            client_socket.sendall(b'Enter amount to deposit: ')
            amount = float(client_socket.recv(1024).decode().strip())
            accounts[account_number]['balance'] += amount
            client_socket.sendall(f'Successfully deposited ${amount}. Your new balance is ${accounts[account_number]["balance"]}\n'.encode())

        elif option == '3':  # Withdraw
            client_socket.sendall(b'Enter amount to withdraw: ')
            amount = float(client_socket.recv(1024).decode().strip())
            if amount > accounts[account_number]['balance']:
                client_socket.sendall(b'Insufficient funds.\n')
            else:
                accounts[account_number]['balance'] -= amount
                client_socket.sendall(f'Successfully withdrew ${amount}. Your new balance is ${accounts[account_number]["balance"]}\n'.encode())

        elif option == '4':  # Exit
            client_socket.sendall(f'Your final balance is ${accounts[account_number]["balance"]}\n'.encode())
            break

        else:
            client_socket.sendall(b'Invalid option. Please try again.\n')

def client_handler(client_socket, accounts):
    thread = threading.Thread(target=handle_client, args=(client_socket, accounts))
    thread.start()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 12345))
server_socket.listen(5)
print('Server is listening on port 12345...')

while True:
    client_socket, addr = server_socket.accept()
    print(f'Connection from {addr}')
    client_handler(client_socket, accounts)