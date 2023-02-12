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

    def address(self):
        # 生成地址
        public_key = self._public_key.to_string()
        public_key_hash = hashlib.sha3_256(public_key).digest().hex()
        return Address(public_key_hash[-20:])


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


class Address:

    def __init__(self, address: str) -> None:
        self._address = address
    
    @property
    def address(self) -> str:
        return self._address


def generate_key_pair() -> tuple[PrivateKey, PublicKey]:
    # 生成公钥和私钥
    private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
    public_key = private_key.get_verifying_key()
    return PrivateKey(private_key.to_string().hex()), PublicKey(public_key.to_string().hex())

# def compress_public_key(public_key: str) -> str:
#     # 压缩公钥
#     public_key_bytes = bytes.fromhex(public_key)
#     x = int.from_bytes(public_key_bytes[:32], 'big')
#     y = int.from_bytes(public_key_bytes[32:], 'big')
#     if y % 2 == 0:
#         return '02' + x.to_bytes(32, 'big').hex()
#     else:
#         return '03' + x.to_bytes(32, 'big').hex()

# def wallet_import_format_private_key(private_key: str) -> str:
#     # 非压缩私钥
#     private_key_bytes = bytes.fromhex(private_key)
#     checksum = hashlib.sha256(hashlib.sha256(private_key_bytes).digest()).digest()[:4]
#     bytes37 =  '80' + private_key_bytes.hex() + checksum.hex()
#     return base58.b58encode(bytes.fromhex(bytes37)).decode()