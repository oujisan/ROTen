#!/usr/bin/env python3

import sys
import argparse
import random

banner = r'''
  ___  ___ _____         
 | _ \/ _ \_   _|__ _ _  
 |   / (_) || |/ -_) ' \ 
 |_|_\\___/ |_|\___|_||_|
                         
by: oujisan
'''
def rotation(text, rot, reverse=False):
    rotated = ''
    for i in text:
        direction = -1 if reverse else 1
            
        if rot in range(1,26) and i.isalpha():
            base, mod = ord('a') if i.islower() else ord('A'), 26
            rotated += chr((ord(i) - base + rot * direction) % mod + base)
        elif rot in range(33,127) and 33 <= ord(i) <= 126:
            base, mod = 33, 94
            rotated += chr((ord(i) - base + rot * direction) % mod + base)
        else:
            rotated += i
    return rotated

def bruteforce(text):
    space = 7
    for i in range(127):
        if i in range(26):
            print(f'ROT-{i:02} → = {rotation(text=text, rot=i, reverse=False)}')
            print(f'{' '*space}← = {rotation(text=text, rot=i, reverse=True)}')
        elif i in range(33,127):
            if len(str(i)) == 3:
                space = 8
            print(f'ROT-{i:02} → = {rotation(text=text, rot=i, reverse=False)}')
            print(f'{' '*space}← = {rotation(text=text, rot=i, reverse=True)}')

def main():
    try:
        parser = argparse.ArgumentParser(
            prog='ROTen',
            description='A tool to encrypt and decrypt text using ROT (Caesar cipher) with customizable rotation, reverse direction, and brute-force decryption.',
            usage='roten "text" -rot [number] [SETTING]',
            epilog='''Example:
                roten "HelloWorld" -rot 13 | 
                roten "GdkknVnqkc" -rot 13 --reverse | 
                roten "GdkknVnqkc" --bruteforce'''
        )
        parser.add_argument(
            "text",
            type=str,
            help="Text to be rotated"
        )

        options_group = parser.add_mutually_exclusive_group(required=True)
        options_group.add_argument(
            "-rot", "--rotation",
            type=int,
            help='Rotation character. Required for encryption and reverse mode'
        )
        options_group.add_argument(
            "--bruteforce",
            action="store_true",
            help='List all possible ROT13 and ROT47 decryptions (Requires -d/--decrypt)'
        )
        options_group.add_argument(
            "--random",
            action="store_true",
            help='Choose random rotation and direction for encrypt plaintext (Requires -e/--encrypt)'
        )

        settings = parser.add_argument_group("Settings")
        settings_group = settings.add_mutually_exclusive_group(required=False)
        settings_group.add_argument(
            "--reverse",
            action="store_true",
            help='Reverse rotate direction (Default: right or "→")'
        )
        settings_group.add_argument(
            "--both",
            action="store_true",
            help='display decryption in right and left direction of rotation (Requires -d/--decrypt)'
        )

        if len(sys.argv) == 1:
            print(banner)
            parser.print_help()
            raise SystemExit

        args = parser.parse_args()

        if args.reverse and args.rotation is None:
            parser.error("--reverse requires --rotation")
            raise SystemExit
        if args.random and (args.rotation or args.reverse):
            parser.error("--random cannot be used with --rotation, --both or --reverse")
            raise SystemExit
        if args.bruteforce and (args.reverse or args.both or args.random):
            parser.error("--bruteforce cannot be used with --reverse, --rotation or --both")
            raise SystemExit
        if args.both and args.reverse:
            parser.error("--both doesn't need --reverse")
            raise SystemExit

        if args.text:
            if args.bruteforce:
                bruteforce(args.text)

            if args.rotation:
                if args.both:
                    print(f'ROT-{args.rotation:02} → = {rotation(text=args.text, rot=args.rotation, reverse=False)}')
                    print(f'{' '*7}← = {rotation(text=args.text, rot=args.rotation, reverse=True)}')    
                else:             
                    switch = True if args.reverse else False
                    rotated = rotation(text=args.text, rot=args.rotation, reverse=switch)
                    print(rotated)
            elif args.random:
                while True:
                    rand = random.randint(1,127)
                    if rand not in range(26,33):
                        break
                direction = random.randint(0,1)
                print(rotation(text=args.text, rot=rand, reverse=direction))
                print(f'ROT = {rand}')
                print(f'Direction = {'left' if direction == 1 else 'Right'}')
            else:
                parser.error("Text requires -rot / --rotation. Try --random to random the rotation and direction")
                raise SystemExit

    except SystemExit:
        sys.exit(1)

if __name__ == "__main__":
    main()
