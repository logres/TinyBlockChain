from source.my_cryptography import generate_key_pair
import json


with open("default_user.json", 'w', encoding='utf-8') as f:
    content = {}
    for i in range(10):
        private_key,public_key = generate_key_pair()
        content[i] = {'private_key':private_key.private_key,'public_key':public_key.public_key}
    json.dump(content,f)