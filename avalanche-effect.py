import random
from Crypto.Cipher import AES, Blowfish

def encrypt(data, cipher, mode):
    # Encrypt <data> using <cipher>={"AES", "BLOWFISH"}, <mode>={"ECB", "CBC"}, using the same key everytime.
    key = b'Sixteen byte key'
    if (cipher == "AES"):
        if mode == "ECB":
            cipher = AES.new(key, AES.MODE_ECB)
        elif mode == "CBC":
            cipher = AES.new(key, AES.MODE_CBC) # library creates random IV
    elif (cipher == "BLOWFISH"):
        if mode == "ECB":
            cipher = Blowfish.new(key, Blowfish.MODE_ECB)
        elif mode == "CBC":
            cipher = Blowfish.new(key, Blowfish.MODE_CBC)

    ciphertext = cipher.encrypt(data)
    return ciphertext

def bitstring(b):
    # take a bytes object <b> and return the bit string represantation of it
    bits = ""
    for i in range(len(b)):
        byte = b[i]
        _bits = "{0:0>8b}".format(byte)
        bits += _bits
    return bits

def flip_bit(b):
    # take a bytes object <b> and returns a new one, which is the same as the argument, with a random bit flipped
    byte_index = random.randint(0,len(b)-1)
    bit_index = random.randint(0,7)
    bits = "{0:0>8b}".format(b[byte_index])
    if bits[bit_index]=='0':
        digit = '1'
    else:
        digit = '0'
    bits = bits[:bit_index] + digit + bits[bit_index+1:]
    changed_byte = int(bits,2)
    return b[:byte_index] + bytes([changed_byte]) + b[byte_index+1:]

def different_bits(b1, b2):
    # take two bitstrings <b1> and <b2> and return the number of different bits
    if len(b1) != len(b2):
        return -1
    count = 0
    for i in range(len(b1)):
        if b1[i] != b2[i]:
            count += 1
    return count

def run():
    for cipher in ["AES", "BLOWFISH"]:
        if cipher == "AES":
            bs=16
        else:
            bs=8
        for mode in ["ECB", "CBC"]:
            count = 0
            min = 128
            for i in range(100):
                m1 = random.randbytes(bs)
                m2 = flip_bit(m1)

                c1 = encrypt(m1, cipher, mode)
                c2 = encrypt(m2, cipher, mode)
                c1_bits = bitstring(c1)
                c2_bits = bitstring(c2)
            
                difference = different_bits(c1_bits,c2_bits)
                count += difference
                if difference < min:
                    min = difference

            print("\n{0} - {1}".format(cipher,mode))
            print("--------------------------")
            print("Διαφορά ανά μέσο όρο: {0} bits ({1}%) ".format(count/100, count/(bs*8)))
            print("Ελάχιστη διαφορά: {0} bits ({1}%)".format(min, min/(bs*8)*100))
            


run()
        