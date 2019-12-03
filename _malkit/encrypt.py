from darkarp.malkit_modules import identifiers
from optparse import OptionParser

def fully_decrypt(instance: identifiers.Malware = None, filename: str = None):
    if instance:
        instance.decrypt_file_fully()
        return 0
    elif filename:
        instance = identifiers.Malware(filename)
        instance.decrypt_file_fully()
        return 0
    else:
        return 1

def encrypt(instance: identifiers.Malware = None, filename: str = None):
    if instance:
        instance.encrypt_file()
        return 0
    elif filename:
        instance = identifiers.Malware(filename)
        instance.encrypt_file()
        return 0
    else:
        return 1
def display(filename):
    with open(filename, "rb") as f:
        print(f.read())

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename",
                      help="file to encrypt", metavar="FILE")
    parser.add_option("-d", "--display", dest="display",
                      help="file to display", metavar="DISPLAY")
    parser.add_option("-F", "--fully-decrypt", dest="fuldec")

    (options, args) = parser.parse_args()
    if options.filename:
        if options.display:
            display(options.filename)
        elif options.fuldec:
            instance = identifiers.Malware(options.filename)
            print(fully_decrypt(instance))
        else:
            instance = identifiers.Malware(options.filename)
            print(encrypt(instance))
            