with open('token', 'rb') as file:
    print(''.join([chr((c - i) % 256) for i, c in enumerate(file.read())]))
