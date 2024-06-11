import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 12345))

try:
    while True:
        data = client_socket.recv(1024).decode()
        print(data)

        if 'Choose an option' in data:
            option = input('Your choice: ')
            client_socket.send(option.encode())
        elif 'Enter' in data:
            value = input()
            client_socket.send(value.encode())
        elif 'Invalid' in data or 'Authenticated' in data or 'Your balance' in data or 'Successfully' in data or 'Insufficient' in data:
            # Print the message received and continue
            continue
        elif 'final balance' in data:
            break
except Exception as e:
    print(f"Error: {e}")
finally:
    client_socket.close()

