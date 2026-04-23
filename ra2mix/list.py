#!/usr/bin/env python


def list_stream(
    fp: "IO[bytes]", out: "IO", id_name_map={}, sort_offset="", file_offset=0
):
    file_count = struct.unpack("<H", fp.read(2))[0]
    flags = 0
    if file_count:  # old
        data_size = struct.unpack("<I", fp.read(4))[0]
        index_data = fp.read(4 * 3 * file_count)
    else:  # new
        flags = struct.unpack("<H", fp.read(2))[0]
        if (flags & 0x2) != 0:
            encrypted_blowfish_key = fp.read(80)
            decrypted_blowfish_key = cccrypto.decrypt_blowfish_key(
                encrypted_blowfish_key
            )
            cipher = blowfish.Cipher(decrypted_blowfish_key)
            decrypted_block = cipher.decrypt_block(fp.read(8))
            (file_count, data_size, _) = struct.unpack("<HIH", decrypted_block)
            decrypt_size, padding_size = cccrypto.get_decryption_block_sizing(
                file_count
            )
            data_decrypted = b"".join(cipher.decrypt_ecb(fp.read(decrypt_size)))
            index_data = decrypted_block[-2:] + data_decrypted[:-padding_size]
        else:
            file_count, data_size = struct.unpack("<HI", fp.read(2 + 4))
            index_data = fp.read(4 * 3 * file_count)
    body_start = fp.tell()

    def sflag(n):
        if n & 1:
            yield "checksumed"
        if n & 2:
            yield "encrypted"
        if n & 0xFFFC:
            yield hex(n)

    max_offset = max_size = 0
    id_filename_map = {}
    entries = []
    for i in range(file_count):
        o = i * 4 * 3
        (id, offset, size) = struct.unpack("<iII", index_data[o : o + (4 * 3)])
        max_offset = max(max_offset, offset)
        max_size = max(max_size, size)
        entries.append((id & 0xFFFFFFFF, offset, size, i))
        if id == MIX_DB_ID:
            fp.seek(file_offset + body_start + offset)
            local_mix_db_blob = fp.read()
            filenames = get_filenames_from_mix_db(local_mix_db_blob)
            id_filename_map.update(
                {ra2_crc(filename) & 0xFFFFFFFF: filename for filename in filenames}
            )

    if sort_offset:
        entries.sort(key=lambda v: v[1], reverse=(sort_offset[0] == "d"))
    pad_nth = len(str(file_count))
    pad_offset = len(str(max_offset))
    pad_size = len(str(max_size))
    head = ["nth", "id", "offset", "size", "name"]
    print(
        f"{head[0]} {head[1]:>{pad_nth+8-len(head[0])}} {head[2]:>{pad_offset}} {head[3]:>{pad_size}} {head[4]}",
        file=out,
    )
    for id, offset, size, i in entries:
        print(
            f"{(i+1):>{pad_nth}} {id:08X} {offset:>{pad_offset}} {size:>{pad_size}}",
            id_filename_map.get(id) or id_name_map.get(id) or "",
            file=out,
        )
    print(
        "   ",
        ", ".join([f"{file_count} files", f"{data_size} data bytes", *sflag(flags)]),
        file=out,
    )


def main():
    import argparse
    from sys import stdout, stderr

    parser = argparse.ArgumentParser(description="List files within a RA2 MIX file.")
    parser.add_argument("mix_files", help="Path to the .mix file", nargs="+")
    parser.add_argument(
        "--sort-by-offset",
        help="Sort entries by offset",
        dest="sort_offset",
        choices=["ascending", "descending", "a", "d"],
    )

    args = parser.parse_args()

    names = set(gmd.keys())
    id_name_map = dict((ra2_crc(filename) & 0xFFFFFFFF, filename) for filename in names)
    sname = set()
    sext = set()
    for filename in gmd.keys():
        name, dot, ext = filename.rpartition(".")
        sname.add(name)
        sext.add(ext)
    for x in sext:
        for n in sname:
            f = f"{n}.{x}"
            g = ra2_crc(f)
            id_name_map[g & 0xFFFFFFFF] = f
    for i, mix_file in enumerate(args.mix_files):
        if i > 0:
            print(file=stdout)
        print("File:", mix_file, file=stdout)
        try:
            with open(mix_file, "rb") as fh:
                list_stream(fh, stdout, id_name_map, sort_offset=args.sort_offset)
        except BrokenPipeError:
            break
        # except Exception as e:
        #     print(f"Error in file: {e}", file=stderr)


if __name__ == "__main__":
    import struct
    import blowfish
    from typing import IO
    from . import const, cccrypto
    from .checksum import ra2_crc
    from .reader import get_filenames_from_mix_db, gmd

    MIX_DB_ID = ra2_crc(const.MIX_DB_FILENAME)
    main()
