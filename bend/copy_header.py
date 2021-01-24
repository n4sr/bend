import argparse
import pathlib
import imghdr


def main(args):
    with open(args.source, 'rb') as f:
        if imghdr.what(args.source) != 'bmp':
            raise Exception('source file is not a bitmap image.')
        source = f.read()

    header = get_header(source)

    for file in args.target:
        with open(file, 'rb') as f:
            data = f.read()
        
        data = overwrite_header(data, header)

        with open(file, 'wb') as f:
            f.write(data)
        

def get_header(b):
    offset = int.from_bytes(b[0xa:0xe], 'little')
    return b[:offset]


def overwrite_header(b, header):
    return header + b[len(header):]
