import base64
import zlib
import re
import os
import argparse

__author__ = "Eric Munene"
__purpose__ = "PHP Obfuscation Decoder / Malware Analysis Utility"


class PhpObfuscationDecoder:
    def __init__(self, encoded_str: str):
        self.encoded_str = encoded_str
        self.decoded_result = None

    def decode(self) -> str:
        """
        Decoding pipeline:
        Base64 → raw DEFLATE → byte shift (-1)
        """
        try:
            raw = base64.b64decode(self.encoded_str, validate=True)
        except Exception:
            raise ValueError("Invalid Base64 payload")

        try:
            decompressed = zlib.decompress(raw, -15)
        except Exception:
            raise ValueError("Zlib decompression failed")

        # Reverse byte shift safely
        shifted = bytes((b - 1) & 0xFF for b in decompressed)

        self.decoded_result = shifted.decode("latin1", errors="ignore")
        return self.decoded_result

    def save(self, filepath: str):
        if not self.decoded_result:
            raise RuntimeError("Nothing to save")
        with open(filepath, "w", encoding="utf-8", errors="ignore") as f:
            f.write(self.decoded_result)


def extract_payloads(php_code: str):
    """
    Extract function calls containing Base64 payloads
    """
    pattern = re.compile(
        r"([a-zA-Z_][a-zA-Z0-9_]*)\(\s*['\"]([A-Za-z0-9+/=]{40,})['\"]\s*\)",
        re.MULTILINE
    )
    return pattern.findall(php_code)


def main():
    parser = argparse.ArgumentParser(
        description="Decode obfuscated PHP payloads (Base64 + zlib + char shift)"
    )
    parser.add_argument("file", help="PHP file to analyze")
    parser.add_argument("-o", "--out", default="decoded_payloads", help="Output directory")
    args = parser.parse_args()

    if not os.path.isfile(args.file):
        print("[!] File not found")
        return

    with open(args.file, "r", encoding="utf-8", errors="ignore") as f:
        php_code = f.read()

    payloads = extract_payloads(php_code)

    if not payloads:
        print("[!] No encoded payloads found")
        return

    os.makedirs(args.out, exist_ok=True)

    print(f"[+] Found {len(payloads)} payload(s)\n")

    for index, (func, encoded) in enumerate(payloads, start=1):
        print(f"[{index}] Decoding payload from function: {func}")

        decoder = PhpObfuscationDecoder(encoded)

        try:
            decoded = decoder.decode()
            outfile = os.path.join(args.out, f"payload_{index}_{func}.php")
            decoder.save(outfile)
            print(f"    ✔ Saved to {outfile}")
        except Exception as e:
            print(f"    ✖ Failed: {e}")

    print("\n[✓] Analysis complete")


if __name__ == "__main__":
    main()
