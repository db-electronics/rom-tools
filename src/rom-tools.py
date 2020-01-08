#! /usr/bin/env python3
import argparse


###############################################################################
# Main
###############################################################################
if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="rom-tools 0.0.0.1")

    parser.add_argument("-i"
                        "--ifile",
                        help="the input rom file",
                        nargs=1,
                        type=str,
                        required=True
                        )

    parser.add_argument("-o"
                        "--ofile",
                        help="the output rom file",
                        nargs=1,
                        type=str,
                        default="out.bin"
                        )

    parser.add_argument("--end",
                        help="swap the endianness of the input file",
                        action="store_true"
                        )

    args = parser.parse_args()


