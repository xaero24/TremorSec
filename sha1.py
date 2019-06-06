class shaControl(object):

    def __init__(self, password):
        self.password = password

    def sha1(self):
        bytes = ""

        h0 = 0x42D05CF1
        h1 = 0x1A5E6329
        h2 = 0x7EC27543
        h3 = 0x12D54B86
        h4 = 0xF03A9472

        for n in range(len(self.password)):
            bytes += '{0:08b}'.format(ord(self.password[n]))
        bits = bytes+"1"
        pBits = bits

        while len(pBits) % 512 != 448:
            pBits += "0"

        pBits += '{0:064b}'.format(len(bits) -1)

        def cnks(l, n):
            return [l[i:i+n] for i in range(0, len(l), n)]

        def roll(n, b):
            return ((n << b) | (n >> (32 - b))) & 0xFFFFFFFF

        for c in cnks(pBits, 512):
            words = cnks(c, 32)
            newBits = [0]*80

            for n in range(0,16):
                newBits[n] = int(words[n], 2)

            for i in range(16,80):
                newBits[i] = roll((newBits[i - 3] ^ newBits[i - 8] ^ newBits[i - 14] ^ newBits[i - 16]), 1)

            a = h0
            b = h1
            c = h2
            d = h3
            e = h4

            for i in range(0, 80):
                if  0 <= i <= 19:
                    f = (b&c) | ((~b)&d)
                    k = 0xC326E8A9

                elif 20 <= i <= 39:
                    f = b ^ c ^ d
                    k = 0x145B6723

                elif 40 <= i <= 59:
                    f = (b&c) | (b&d) | (c&d)
                    k = 0x123CD5A9

                elif 60 <= i <= 79:
                    f = b ^ c ^ d
                    k = 0x34C5A692

                temp = roll(a, 5) + f + e + k + newBits[i] & 0xffffffff
                e = d
                d = c
                c = roll(b, 30)
                b = a
                a = temp

            h0 = h0 + a & 0xffffffff
            h1 = h1 + b & 0xffffffff
            h2 = h2 + c & 0xffffffff
            h3 = h3 + d & 0xffffffff
            h4 = h4 + e & 0xffffffff

        self.password = '%08x%08x%08x%08x%08x' % (h0, h1, h2, h3, h4)

    def saveToDB(self):
        return 0

    def compareToDB(self):
        return 0

    def __str__(self):
        return self.password

# c = shaControl("hellow world")
# c.sha1()
# print(c)