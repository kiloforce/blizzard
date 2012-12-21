# Purpose: Decode Warcraft II Serial Number
# Maintainer: Kilo Force <kiloforce@k.ttak.org> (2012)

import sys  # for command line arguments
import optparse  # for command line arguments


def run():
    parser = optparse.OptionParser()

    parser.add_option('--serial', default=None)
    parser.add_option('--debug', action='store_true', default=False)

    (options, args) = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    serial = options.serial
    if serial is None and args:
        serial = args[0]
    serial = serial.replace('-', '')
    serial = serial.upper()

    print "Decoding Warcraft II Serial Number: %s" % serial

    (product_id, public_key, private_key) = blizzard_decode(serial, options.debug)

    print "Product ID:  %d" % product_id
    print "Public Key:  %d" % public_key
    print "Private Key: %d" % private_key


def blizzard_decode(serial, debug):

    # Example:
    #   serial: FNFVMD6W887G2P64
    #   product_id: 4 (Warcraft II)
    #   public_key: 1111
    #   private_key: 1111

    SALT = int("13AC9741", 16)
    VALID_CODES = "246789BCDEFGHJKMNPRTVWXZ"
    AORD = (5, 6, 0, 1, 2, 3, 4, 9, 10, 11, 12, 13, 14, 15, 7, 8)

    cKey = list(serial)
    eKey = list(serial)

    if len(serial) != 16:
        if debug:
            print "Error: Invalid serial length"
        return None

    for i in range(0, len(serial)):
        if not cKey[i] in VALID_CODES:
            if debug:
                print "Error: Invalid character %s" % i
            return None

    for i in range(0, len(serial), 2):
        n = VALID_CODES.index(cKey[i+1]) + VALID_CODES.index(cKey[i]) * 24
        n = n & int('FF', 16)

        if ((n >> 4) & int('F', 16)) < 10:
            c = chr(((n >> 4) & int('F', 16)) + int('30', 16))
            eKey[i] = c
        else:
            c = chr(((n >> 4) & int('F', 16)) + int('37', 16))
            eKey[i] = c
        if (n & int('F', 16)) < 10:
            c = chr((n & int('F', 16)) + int('30', 16))
            eKey[i+1] = c
        else:
            c = chr((n & int('F', 16)) + int('37', 16))
            eKey[i+1] = c

    decoded = ['0']*16

    for i in range(15, -1, -1):
        c = ord(eKey[AORD[i]])
        if c <= 55:
            decoded[i] = chr(c ^ (SALT & 7))
            SALT = SALT >> 3
        elif c < 65:
            decoded[i] = chr(c ^ i & 1)
        else:
            decoded[i] = chr(c)

    if debug:
        print "Decoded String:  " + ''.join(decoded)
        print "Product ID Hex:  " + ''.join(decoded[0:2])
        print "Public Key Hex:  " + ''.join(decoded[2:8])
        print "Private Key Hex: " + ''.join(decoded[8:])

    product_id = int(''.join(decoded[0:2]), 16)
    public_key = int(''.join(decoded[2:8]), 16)
    private_key = int(''.join(decoded[8:]), 16)

    return (product_id, public_key, private_key)


if __name__ == '__main__':
    sys.exit(run())

# EOF
