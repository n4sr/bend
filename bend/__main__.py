import argparse
import pathlib
import random

from .version import VERSION


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', type=pathlib.Path)
    parser.add_argument('outfile', type=pathlib.Path, default='output.jpg')
    parser.add_argument('-m', type=int, default=1, dest='magnitude')
    args = parser.parse_args()

    with open(args.infile, 'rb') as f:
        img = f.read()

    data = split_jpg(img)

    for n, x in enumerate(data):
        if not marker_type(x) == 'SOS':
            continue
        data[n] = blast(x, args.magnitude)

    bent_img = b''.join(data)

    with open(args.outfile, 'wb') as f:
        f.write(bent_img)


def split_jpg(b):
    if not isinstance(b, bytes):
        raise TypeError()
    result = []
    last_marker = 0
    for i in range(2, len(b)-1):
        if b[i] == 0xff and b[i+1] != 0x00:
            result.append(b[last_marker:i])
            last_marker = i
    return result


def blast(b, magnitude):
    '''randomizes a portion of bytes.'''
    if not isinstance(b, bytes):
        raise TypeError()
    head, tail = split_marker(b)
    tail = [x for x in tail]
    n = int(magnitude / 100000 * len(tail))+1
    for _ in range(n):
        i = random.randrange(len(tail))
        tail[i] = random.randrange(0xff)
    tail = remove_markers(tail)
    tail = bytes(tail)
    return head + tail


def marker_length(b):
    '''returns the marker's self defined length.'''
    if not isinstance(b, bytes):
        raise TypeError()
    if marker_type(b) in ('SOI', 'EOI'):
        return 2
    return int.from_bytes(b[2:4], 'big')


def remove_markers(obj):
    r'''remove markers by finding all `FF` bytes and replacing the following 
        byte with `00`.'''
    if isinstance(obj, bytes):
        obj = [x for x in obj]
    if not isinstance(obj, list):
        raise TypeError()
    for i in range(len(obj)-1):
        if obj[i] == 0xff and obj[i+1] != 0x00:
            obj[i+1] = 0x00
    return bytes(obj)


def split_marker(b):
    i = marker_length(b)
    return b[:i], b[i:]


def marker_type(b):
    '''takes bytes, returns marker type.'''
    # https://en.wikipedia.org/wiki/JPEG#Syntax_and_structure
    if not isinstance(b, bytes):
        raise TypeError()
    return {
        b'\xff\xd8': 'SOI',  # start of image
        b'\xff\xc0': 'SOF0',  # start of frame (baseline DCT)
        b'\xff\xc2': 'SOF2',  # start of frame (progressive DCT)
        b'\xff\xc4': 'DHT',  # define huffman table
        b'\xff\xdb': 'DQT',  # define quantization table
        b'\xff\xdd': 'DRI',  # define restart interval
        b'\xff\xda': 'SOS',  # start of scan
        b'\xff\xd0': 'RST',  # restart
        b'\xff\xd1': 'RST',
        b'\xff\xd2': 'RST',
        b'\xff\xd3': 'RST',
        b'\xff\xd4': 'RST',
        b'\xff\xd5': 'RST',
        b'\xff\xd6': 'RST',
        b'\xff\xd7': 'RST',
        b'\xff\xe0': 'APP0',  # app specific
        b'\xff\xe1': 'APP1',  # exif
        b'\xff\xe2': 'APP2',
        b'\xff\xe3': 'APP3',
        b'\xff\xe4': 'APP4',
        b'\xff\xe5': 'APP5',
        b'\xff\xe6': 'APP6',
        b'\xff\xe7': 'APP7',
        b'\xff\xe8': 'APP8',
        b'\xff\xe9': 'APP9',
        b'\xff\xea': 'APP10',
        b'\xff\xeb': 'APP11',
        b'\xff\xec': 'APP12',
        b'\xff\xed': 'APP13',
        b'\xff\xee': 'APP14',
        b'\xff\xef': 'APP15',
        b'\xff\xfe': 'COM',  # comment (text)
        b'\xff\xd9': 'EOI',  # end of image
    }.get(b[:2], None)


if __name__ == '__main__':
    main()
