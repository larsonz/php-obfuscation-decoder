# PHP Obfuscation Decoder

## Overview

The **PHP Obfuscation Decoder** is a production-grade Python utility designed to identify, extract, and decode obfuscated PHP payloads commonly found in compromised websites, malicious web shells, and protected PHP loaders.

It targets a widely used obfuscation pattern that combines:

* **Base64 encoding**
* **Raw zlib (DEFLATE) compression**
* **Character-level byte shifting**

The tool operates in a **read-only, non-executing manner**, making it suitable for malware analysis, incident response, and forensic review.

---

## Key Features

* Binary-safe decoding (prevents payload corruption)
* Decodes **all** discovered payloads in a file
* Supports single and double quoted PHP strings
* Validates Base64 and zlib layers before decoding
* Produces separate output files per payload
* Analysis-only (never executes decoded PHP)

---

## How It Works

For each detected payload, the decoder applies the following pipeline:

1. **Payload Discovery**
   Scans the PHP source file for function calls containing long Base64-encoded strings.

2. **Decoding Pipeline**

   * Base64 decoding with strict validation
   * Raw zlib decompression (headerless DEFLATE)
   * Binary-safe character shift reversal (-1 byte)

3. **Output Generation**
   Each decoded payload is written to an individual output file for inspection.

---

## Supported Obfuscation Pattern

The tool is effective against PHP code similar to:

```php
eval(gzinflate(base64_decode($payload)));
```

As well as variants that:

* Use raw DEFLATE streams
* Apply `chr(ord($c)+1)`-style character shifting
* Load payloads via custom wrapper functions

---

## Installation

### Requirements

* Python 3.8 or later
* No external dependencies (standard library only)

### Clone the Repository

```bash
git clone https://github.com/yourusername/php-obfuscation-decoder.git
cd php-obfuscation-decoder
```

---

## Usage

```bash
python php_decoder.py suspicious.php
```

Specify a custom output directory:

```bash
python php_decoder.py suspicious.php -o decoded_output
```

---

## Output Structure

```text
decoded_output/
├── payload_1_eval.php
├── payload_2_loader.php
└── payload_3_inject.php
```

Each file contains a fully decoded PHP payload preserved exactly as recovered.

---

## Use Cases

* PHP malware and webshell analysis
* Incident response and post-breach investigation
* Reverse engineering of obfuscated PHP loaders
* Security research and controlled forensic examination
* Educational analysis of PHP obfuscation techniques

---

## Security Notice

* This tool **does not execute** decoded PHP code
* Always review decoded payloads in an isolated environment
* Do not deploy decoded code to production systems

---

## Disclaimer

This tool is intended for **educational, forensic, and defensive security purposes only**. Ensure you have proper authorization before analyzing third-party code.

---

## Author

Eric Munene

---

## License

MIT License
