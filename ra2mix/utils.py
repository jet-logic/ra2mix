import binascii
from struct import pack


SIZE_OF_ENCRYPTED_KEY = 80


def decrypt_blowfish_key_fast(encrypted_blowfish_key):
    BLOCK_SIZE = 40
    PUBLIC_EXPONENT = 65537
    PUBLIC_MODULUS = 681994811107118991598552881669230523074742337494683459234572860554038768387821901289207730765589

    if len(encrypted_blowfish_key) < SIZE_OF_ENCRYPTED_KEY:
        raise ValueError("Buffer is not long enough")

    # Process both blocks directly without creating list
    block1 = encrypted_blowfish_key[:40]
    block2 = encrypted_blowfish_key[40:80]

    # Decrypt both blocks
    result_parts = []

    for encrypted_block in (block1, block2):
        decrypted_int = pow(
            int.from_bytes(encrypted_block, "little"), 65537, PUBLIC_MODULUS
        )

        # Convert to bytes with minimal byte length
        decrypted = decrypted_int.to_bytes(
            (decrypted_int.bit_length() + 7) >> 3, "little"
        )

        # Efficient null stripping
        if decrypted[-1] == 0:
            # Find last non-zero byte
            for i in range(len(decrypted) - 1, -1, -1):
                if decrypted[i] != 0:
                    decrypted = decrypted[: i + 1]
                    break
            else:
                decrypted = b""  # All zeros

        result_parts.append(decrypted)

    return b"".join(result_parts)


def ra2_crc_fast(filename: str) -> int:
    """Ultra-fast RA2 CRC calculation."""
    length = len(filename)
    salt = length & 0xFFFFFFFC

    # Build obfuscated string efficiently
    obfuscated = filename.upper()

    remainder = length & 3
    if remainder:
        obfuscated += chr(length - salt) + obfuscated[salt] * (3 - remainder)

    crc = binascii.crc32(obfuscated.encode())
    return crc - 0x100000000 if crc >= 0x80000000 else crc


def names_db_enum(filenames: list[str], game=0):
    n = len(filenames)
    yield b"XCC by Olaf van der Spek\x1a\x04\x17\x27\x10\x19\x80\x00"
    yield pack("=5I", 52 + sum([len(v) + 1 for v in filenames]), 0, 0, game, n)
    for v in filenames:
        yield v.encode() + b"\x00"


def as_sink(path="-", mode="wb"):
    if path and path != "-":
        return open(path, mode)
    from sys import stdout

    return stdout.buffer if "b" in mode else stdout


def as_source(path="-", mode="rb"):
    if path and path != "-":
        return open(path, mode)
    from sys import stdin

    return stdin.buffer if "b" in mode else stdin
