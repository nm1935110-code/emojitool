is a Python-based steganography tool that allows users to hide data inside emoji characters in a stealthy manner. The tool leverages special Unicode characters, specifically Variation Selectors and Tag Characters, to encode data and invisibly “attach” it behind a normal emoji, making the hidden content difficult to detect.
Encoding Options:
-f, --file <PATH> Read a file to encode
-t, --text <TEXT> Use direct text to encode
-m <v|t> Encoding method (v: variant, t: tag)
-e <EMOJI> Emoji to use (default: 😈)
-o, --output <FILE> Write output to file
Decoding Options:
-d, --decode <STRING> Decode emoji string
-o, --output <FILE> Write output to file
Examples:
python emoji_smuggler.py -f secret.txt -o hidden.txt
python emoji_smuggler.py -t "HELLO WORLD" -m t -e "🔥" -o out.txt
python emoji_smuggler.py -d "😈" -o decrypted.bin
python emoji_smuggler.py -d "😈"
Author: Minh
How to contribute: You can send feedback and suggestions to help improve the tool.
Contact Email: MinhZOa565hgs@protonmail.com
