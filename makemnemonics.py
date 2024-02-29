from bip39 import Mnemonic

def generate_mnemonic(length=24):
    mnemo = Mnemonic("english")
    return mnemo.generate(strength=length * 11)

if __name__ == "__main__":
    for _ in range(3):
        mnemonic = generate_mnemonic(length=24)
        print("Mnemonic:", mnemonic)
