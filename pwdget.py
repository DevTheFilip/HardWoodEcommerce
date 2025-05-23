with open('created_users.txt', 'r') as file:
    for line in file:
        print(line.strip())  # Removes trailing newline characters