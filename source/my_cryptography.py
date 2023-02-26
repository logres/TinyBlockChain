import ecdsa
import hashlib
# 设计思路

# 1. 私钥 256bit随机数  | base58 -> 压缩私钥
# 2. 公钥 私钥 -> ecdsa SECP256k1 -> 公钥
# 3. 地址 公钥 -> keccak256 -> 地址

# 字符串与bytes管理 注意，不使用0x前缀

def hash160(data: bytes) -> bytes:
    # 先计算SHA256 再计算RIPEMD160
    return hashlib.new('ripemd160', hashlib.sha256(data).digest()).digest()

def hash256(data: bytes) -> bytes:
    # 计算两遍SHA256
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()

class PublicKey:

    def __init__(self, public_key: str) -> None:
        # public_key b'04'+64字节
        self._public_key = ecdsa.VerifyingKey.from_string(bytes.fromhex(public_key), curve=ecdsa.SECP256k1) # 特殊对象

    @property
    def public_key(self) -> str:
        return '04' + self._public_key.to_string().hex()
    
    @property
    def x(self) -> str:
        return self._public_key.pubkey.point.x().to_bytes(32, 'big').hex()
    
    @property
    def y(self) -> str:
        return self._public_key.pubkey.point.y().to_bytes(32, 'big').hex()
    
    @property
    def compressed_public_key(self) -> str:
        return '02' + self.x if int(self.y, 16) % 2 == 0 else '03' + self.x

    @property
    def public_key_hash(self) -> str:
        return hash160(bytes.fromhex(self.public_key)).hex()

    def verify(self, message: bytes, signature: bytes) -> bool:
        return self._public_key.verify(signature, message)

    def to_address(self) -> "Address":
        # 生成地址 1+20+4
        public_key_hash_byte = bytes.fromhex(self.public_key_hash)
        prefix = b'\x00'
        checksum = hash256(prefix + public_key_hash_byte)[:4]
        return Address((prefix + public_key_hash_byte + checksum).hex())

class Address:

    def __init__(self, address: str) -> None:
        # address 1+20+4
        self._address :str = address

    @property
    def address(self) -> str:
        return self._address

    @property
    def public_key_hash(self) -> str:
        # 地址转公钥hash
        address_bytes = bytes.fromhex(self._address)
        return address_bytes[1:-4].hex()
    
    def is_valid(self) -> bool:
        # 验证地址是否有效
        address_bytes = bytes.fromhex(self._address)
        prefix = b'\x00'
        checksum = hash256(prefix + address_bytes[1:-4])[:4]
        return checksum == address_bytes[-4:]


class PrivateKey:

    def __init__(self, private_key: str) -> None:
        # private_key 256位
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