with open("./message.txt", 'r', encoding='utf-8') as file:
    message = file.read().strip()
    
print(message)