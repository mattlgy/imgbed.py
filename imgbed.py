from PIL import Image, ImageDraw
import random
import argparse
import sys

class ImageData (object):
    default_encoding = sys.getdefaultencoding()
    def __init__ (self, _img):
        super(ImageData, self).__init__()
        self._img = _img
        self._img_bytes = bytearray(_img.tobytes())

    def clear (self):
        for i, b in enumerate(self._img_bytes):
            self._img_bytes[i] = b & ~1

    def write (self, data, string_encodeing = default_encoding, offset = 0):
        if isinstance(data, str):
            data_bytes = bytes(data, string_encodeing)
        else:
            data_bytes = bytes(data)

        if (len(data_bytes) > self.available_size()):
            return False, 'Insufficient size'

        for i, b in enumerate(data_bytes):
            i8 = i * 8
            for j in range(8):
                self._img_bytes[i8 + j] = self._img_bytes[i8 + j] + ((b >> 7 - j) & 1)

    def read (self, offset = 0):
        data = bytearray()
        data_byte = 0
        j = 7
        for i, b in enumerate(self._img_bytes):
            data_byte = data_byte | ((b & 1) << j)
            j = j - 1
            if (j < 0):
                j = 7
                data.append(data_byte)
                data_byte = 0
        return data

    def available_size (self):
        return int(len(self._img_bytes) / 8)

    def to_image (self):
        return Image.frombytes(self._img.mode, self._img.size, bytes(self._img_bytes))


def main ():
    parser = argparse.ArgumentParser()
    parser.add_argument('image', help = 'image file')
    parser.add_argument('-s',    help = 'string to embed in the image',  dest = 'string')
    parser.add_argument('-f',    help = 'file to embed in the image',    dest = 'file')
    parser.add_argument('-o',    help = 'output file to save new image', dest = 'out')
    args = parser.parse_args()
    
    if ((args.file != None or args.string != None) and args.out == None):
        print('output file must be given (-o)')
        sys.exit(2)

    img = Image.open(args.image)
    img_data = ImageData(img)

    if (args.file == None and args.string == None):
        data = img_data.read()
        print(data.decode())
    else:
        if (args.file != None):
            fh = open(args.file, 'rb')
            data = fh.read()
        else:
            data = args.string

        img_data.clear()
        img_data.write(data)
        img_data.to_image().save(args.out, 'PNG')

if __name__ == "__main__":
   main()
