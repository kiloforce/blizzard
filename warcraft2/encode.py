# Purpose: Encode Warcraft II Serial Number
# Maintainer: Kilo Force <kiloforce@k.ttak.org> (2012)

import sys  # for command line arguments
import optparse  # for command line arguments


def run():
    parser = optparse.OptionParser()

    parser.add_option('--product', help='Blizzard Product ID (default: 4 - Warcraft II)', default="4")
    parser.add_option('--public', help='Public Key', default=None)
    parser.add_option('--private', help='Private Key', default=None)
    parser.add_option('--debug', action='store_true', default=False)

    (options, args) = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    if not is_number(options.product):
        print "Error: Invalid Product ID"
        sys.exit(1)
    if not is_number(options.public):
        print "Error: Invalid Public ID"
        sys.exit(1)
    if not is_number(options.private):
        print "Error: Invalid Private ID"
        sys.exit(1)

    product_id = int(options.product)
    public_key = int(options.public)
    private_key = int(options.private)

    print "Encoding Warcraft II Serial Number: (%d, %d, %d)" % (product_id, public_key, private_key)

    (serial) = blizzard_encode(product_id, public_key, private_key, options.debug)

    print "Serial:  %s" % serial


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def blizzard_encode(product_id, public_key, private_key, debug):

    # Example:
    #   serial: FNFVMD6W887G2P64
    #   product_id: 4 (Warcraft II)
    #   public_key: 1111
    #   private_key: 1111

    SALT = int("13AC9741", 16)
    VALID_CODES = "246789BCDEFGHJKMNPRTVWXZ"
    AORD = (5, 6, 0, 1, 2, 3, 4, 9, 10, 11, 12, 13, 14, 15, 7, 8)

    encoded = ['']*16

    salt = SALT
    
    key =  hex(product_id)[2:].rjust(2, '0')
    key += hex(public_key)[2:].rjust(6, '0')
    key += hex(private_key)[2:].rjust(8, '0')
    key = key.upper()
    if debug:
        print "Decode Key: " + key
    
    for i in range(15, -1, -1):
        c = ord(key[i])
        if c <= 55:
            encoded[AORD[i]] = chr(c ^ (salt & 7))
            salt = salt >> 3
        elif c < 65:
            encoded[AORD[i]] = chr(c ^ i & 1)
        else:
            encoded[AORD[i]] = chr(c)
    if debug:
        print "Reordered Key: " + ''.join(encoded)
    
    r = 3
    for i in range(0, 16):
        if is_number(encoded[i]):
            r = r + ((ord(encoded[i]) - int('30', 16)) ^ (r * 2))
        else:
            r = r + ((ord(encoded[i]) - int('37', 16)) ^ (r * 2))
    
    r = r & int('FF', 16)
    t = int('80', 16)
    for i in range(14, -1, -2):
        a = 0
        if is_number(encoded[i]):
            a = (ord(encoded[i]) - int('30', 16))
        else:
            a = (ord(encoded[i]) - int('37', 16))
        b = 0
        if is_number(encoded[i+1]):
            b = (ord(encoded[i+1]) - int('30', 16))
        else:
            b = (ord(encoded[i+1]) - int('37', 16))
        a = "%s%s" % (hex(a)[2:], hex(b)[2:])
        a = a.upper()
        a = int(a, 16)
        if r & t:
            a = a + int('100', 16)
        b = 0
        while a >= int('18', 16):
            b = b + 1
            a = a - int('18', 16)
        encoded[i] = VALID_CODES[b]
        encoded[i+1] = VALID_CODES[a]
    
        t = t /2
    
    serial = ''.join(encoded)
    if debug:
        print "Encoded Serial: " + serial
    return serial


if __name__ == '__main__':
    sys.exit(run())

# EOF
