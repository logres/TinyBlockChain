import ecdsa
import hashlib
# 设计思路

# 1. 私钥 256bit随机数  | base58 -> 压缩私钥
# 2. 公钥 私钥 -> ecdsa SECP256k1 -> 公钥
# 3. 地址 公钥 -> keccak256 -> 地址

class PublicKey:

    def __init__(self, public_key: str) -> None:
        public_key.removeprefix('0x')
        self._public_key = ecdsa.VerifyingKey.from_string(bytes.fromhex(public_key), curve=ecdsa.SECP256k1)

    @property
    def public_key(self) -> str:
        return '04' + self._public_key.to_string().hex()
    
    def verify(self, message: bytes, signature: bytes) -> bool:
        return self._public_key.verify(signature, message)
    
    def public_key_hash(self):
        # 生成公钥hash
        public_key_bytes = bytes.fromhex(self.public_key)
        return hashlib.sha3_256(public_key_bytes).hexdigest()

    def to_address(self) -> "Address":
        # 生成地址
        public_key_hash = self.public_key_hash()
        public_key_hash_bytes = bytes.fromhex(public_key_hash)
        checksum = hashlib.sha3_256(public_key_hash_bytes).hexdigest()[:8]
        return Address('0x' + public_key_hash + checksum)

class Address:

    def __init__(self, address: str) -> None:
        self._address = address

    @property
    def address(self) -> str:
        return self._address

    def to_public_key_hash(self) -> str:
        # 地址转公钥hash
        return self._address[2:-8]
    
    def is_valid(self) -> bool:
        # 验证地址是否有效
        address = self._address[2:]
        checksum = hashlib.sha3_256(bytes.fromhex(address[:-8])).hexdigest()[:8]
        return checksum == address[-8:]


class PrivateKey:

    def __init__(self, private_key: str) -> None:
        private_key.removeprefix('0x')
        self._private_key = ecdsa.SigningKey.from_string(bytes.fromhex(private_key), curve=ecdsa.SECP256k1)

    @property
    def private_key(self) -> str:
        return self._private_key.to_string().hex()
    
    def sign(self, message: bytes) -> bytes:
        return self._private_key.sign(message)
    
    def public_key(self) -> PublicKey:
        # 生成公钥
        public_key = self._private_key.get_verifying_key()
        return PublicKey(public_key.to_string().hex())


def generate_key_pair() -> tuple[PrivateKey, PublicKey]:
    # 生成公钥和私钥
    private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
    public_key = private_key.get_verifying_key()
    return PrivateKey(private_key.to_string().hex()), PublicKey(public_key.to_string().hex())