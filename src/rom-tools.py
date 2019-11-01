#! /usr/bin/env python3
import argparse


###############################################################################
# Main
###############################################################################
if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="rom-tools 0.0.0.1")

    parser.add_argument("--ifile",
                        help="the input rom file",
                        nargs=1,
                        type=str,
                        required=True
                        )

    args = parser.parse_args()
