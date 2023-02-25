from source.my_cryptography import PrivateKey, PublicKey, Address, generate_key_pair

def test_toString_and_fromString():
    private_key,public_key = generate_key_pair()
    private_key_string = private_key.private_key
    public_key_string = public_key.public_key
    private_key2 = PrivateKey(private_key_string)
    public_key2 = PublicKey(public_key_string)

    message = b"Hello!"

    assert public_key2.verify(message,private_key.sign(message))

    assert public_key.verify(message,private_key2.sign(message))

def test_sign_and_verify():
    private_key,public_key = generate_key_pair()
    message = b"Hello!"
    signature = private_key.sign(message)
    assert public_key.verify(message,signature)

def test_get_public_key_from_private_key():
    private_key,public_key = generate_key_pair()
    public_key2 = private_key.public_key()
    assert public_key2.public_key == public_key.public_key

def test_translate_between_address_and_public_key_hash():
    private_key,public_key = generate_key_pair()
    address = public_key.to_address()
    assert address.public_key_hash == public_key.public_key_hash