#!/usr/bin/python3

import json
from pathlib import Path
from unittest import TestCase, main
from subprocess import run

from ra2mix.checksum import ra2_crc
from ra2mix.utils import names_db_enum, ra2_crc_fast
from ra2mix.writer import get_mix_db_data


class Test(TestCase):
    def test_1(self):
        from ra2mix.reader import gmd

        for filename in gmd.keys():
            assert ra2_crc_fast(filename) == ra2_crc(filename)

    def test_2(self):
        # names_db_enum()
        # get_mix_db_data()
        from ra2mix.checksum import ra2_crc
        from ra2mix.reader import gmd
        from ra2mix.const import XCCGame

        names = list(gmd.keys())
        print(names)
        b1 = get_mix_db_data(names, XCCGame.RA2)
        b2 = b"".join(names_db_enum(names, XCCGame.RA2.value))
        # self.assertEqual(len(b1),len(b2))
        self.assertEqual(b1, b2)

    def test_3(self):
        from ra2mix.const import XCCGame

        print(
            [
                (member.name, member.value, i == member.value)
                for i, member in enumerate(XCCGame)
            ]
        )
        print([member.name for member in XCCGame])

    def test_4(self):
        from ra2mix.const import XCCGame
        from ra2mix.writer import write
        from ra2mix.__main__ import create

        m1 = Path("/tmp/mix1")
        m2 = Path("/tmp/mix2")
        files = r"""ra2mix/cccrypto.py
ra2mix/checksum.py
ra2mix/const.py
ra2mix/reader.py""".strip().splitlines()
        write(str(m1), filepaths=files)
        create(str(m2), files)
        self.assertEqual(m1.stat().st_size, m2.stat().st_size)
        self.assertEqual(m1.read_bytes(), m2.read_bytes())


if __name__ == "__main__":
    main()
