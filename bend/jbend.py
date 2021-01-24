import imghdr
import pathlib
import random


def main(args):
    if imghdr.what(args.infile) != 'jpeg':
        raise Exception('infile is not jpeg.')

    with open(args.infile, 'rb') as f:
        img = f.read()

    chunks = split_jpg(img)

    for i, chunk in enumerate(chunks):
        if marker_type(chunk) == 'SOS':
            chunks[i] = blast(chunk, args.magnitude)

    bent_img = b''.join(chunks)

    with open(args.outfile, 'wb') as f:
        f.write(bent_img)


def split_jpg(img):
    if not isinstance(img, bytes):
        raise TypeError(f'expected bytes, got {type(img).__name__}.')
    result = []
    last_marker = 0
    for i in range(2, len(img)-1):
        if img[i] == 0xff and img[i+1] != 0x00:
            result.append(img[last_marker:i])
            last_marker = i
    return result


def blast(chunk, n):
    '''randomizes a portion of bytes.'''
    MAX = 16
    if not isinstance(chunk, bytes):
        raise TypeError(f'expected bytes, got {type(chunk).__name__}.')
    if not 0 <= n <= MAX:
        raise ValueError(f'n must be between 1 and {MAX}.')
    head, tail = split_marker(chunk)
    tail = [x for x in tail]
    n = int(len(tail) / 2**(MAX - n))
    for _ in range(n):
        i = random.randrange(len(tail))
        tail[i] = random.randrange(0xff)
    tail = remove_markers(tail)
    tail = bytes(tail)
    return head + tail


def marker_length(chunk):
    '''returns the marker's self defined length.'''
    if not isinstance(chunk, bytes):
        raise TypeError(f'expected bytes, got {type(chunk).__name__}.')
    if marker_type(chunk) in ('SOI', 'EOI', 'RST'):
        return 2
    if marker_type(chunk) == 'DRI':
        return 6
    return int.from_bytes(chunk[2:4], 'big')


def remove_markers(obj):
    r'''remove markers by finding all `FF` bytes and replacing the following
        byte with `00`.'''
    if isinstance(obj, bytes):
        obj = [x for x in obj]
    if not isinstance(obj, list):
        raise TypeError(f'expects bytes or list, got {type(obj).__name__}')
    for i in range(len(obj)-1):
        if obj[i] == 0xff:
            obj[i+1] = 0x00
    return bytes(obj)


def split_marker(chunk):
    i = marker_length(chunk)
    return chunk[:i], chunk[i:]


def marker_type(chunk):
    '''takes bytes, returns marker type.'''
    # https://en.wikipedia.org/wiki/JPEG#Syntax_and_structure
    if not isinstance(chunk, bytes):
        raise TypeError(f'expected bytes, got {type(chunk).__name__}.')
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
    }.get(chunk[:2], None)


