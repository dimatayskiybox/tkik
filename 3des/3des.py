from config import PI, CP_1, CP_2, E, S_BOX, P, PI_1, SHIFT
def string_to_bit_array(text):
    array = list()
    for char in text:
        binval = binvalue(char, 8)
        array.extend([int(x) for x in list(binval)])
    return array


def bit_array_to_string(array):
    res = ''.join([chr(int(y, 2)) for y in [''.join([str(x) for x in _bytes]) for _bytes in split_array(array, 8)]])
    return res


def binvalue(val, bitsize):
    binval = bin(val)[2:] if isinstance(val, int) else bin(ord(val))[2:]
    while len(binval) < bitsize:
        binval = "0" + binval
    return binval


def split_array(s, n):
    return [s[k:k + n] for k in range(0, len(s), n)]


ENCRYPT = 1
DECRYPT = 0


class des():
    def __init__(self):
        self.password = None
        self.text = None
        self.keys = list()

    def run(self, key, text, action=ENCRYPT, padding=False):
        padding = True
        self.password = key
        self.text = text

        if padding and action == ENCRYPT:
            self.addPadding()

        self.generatekeys()
        text_blocks = split_array(self.text, 8)
        result = list()
        for block in text_blocks:
            block = string_to_bit_array(block)
            block = self.permut(block, PI)
            g, d = split_array(block, 32)
            tmp = None
            for i in range(16):
                d_e = self.expand(d, E)
                if action == ENCRYPT:
                    tmp = self.xor(self.keys[i], d_e)
                else:
                    tmp = self.xor(self.keys[15 - i], d_e)
                tmp = self.substitute(tmp)
                tmp = self.permut(tmp, P)
                tmp = self.xor(g, tmp)
                g = d
                d = tmp
            result += self.permut(d + g, PI_1)
        final_res = bit_array_to_string(result)
        if padding and action == DECRYPT:
            return self.removePadding(final_res)
        else:
            return final_res

    def substitute(self, d_e):
        subblocks = split_array(d_e, 6)
        result = list()
        for i in range(len(subblocks)):
            block = subblocks[i]
            row = int(str(block[0]) + str(block[5]), 2)
            column = int(''.join([str(x) for x in block[1:][:-1]]), 2)
            val = S_BOX[i][row][column]
            bin = binvalue(val, 4)
            result += [int(x) for x in bin]
        return result

    def permut(self, block, table):
        return [block[x - 1] for x in table]

    def expand(self, block, table):
        return [block[x - 1] for x in table]

    def xor(self, t1, t2):
        return [x ^ y for x, y in zip(t1, t2)]

    def generatekeys(self):
        self.keys = []
        key = string_to_bit_array(self.password)
        key = self.additionalBytes(key)
        key = self.permut(key, CP_1)
        g, d = split_array(key, 28)
        for i in range(16):
            g, d = self.shift(g, d, SHIFT[i])
            tmp = g + d
            self.keys.append(self.permut(tmp, CP_2))

    def additionalBytes(self, key):
        genKey = []

        for i in range(0, len(key), 8):
            genKey += key[i:i + 8] + [1]

        return genKey
    def shift(self, g, d, n):
        return g[n:] + g[:n], d[n:] + d[:n]

    def addPadding(self):
        pad_len = 8 - (len(self.text) % 8)
        self.text += pad_len * chr(pad_len)

    def removePadding(self, data):
        pad_len = ord(data[-1])
        return data[:-pad_len]

    def encrypt(self, key, text, padding=False):
        return self.run(key, text, ENCRYPT, padding)

    def decrypt(self, key, text, padding=False):
        return self.run(key, text, DECRYPT, padding)

def tripleDesEncrypt(key, text):
    d = des()
    keys = split_array(key, 7)
    return d.encrypt(keys[0], d.encrypt(keys[1], d.encrypt(keys[2], text)))

def tripleDesDecrypt(key, text):
    d = des()
    keys = split_array(key, 7)
    return d.decrypt(keys[2], d.decrypt(keys[1], d.decrypt(keys[0], text)))

if __name__ == '__main__':
    key = "secrfdesecrqwesecrete"
    text = "Hello wo"
    a = tripleDesEncrypt(key, text)
    print(a)
    print(tripleDesDecrypt(key, a))