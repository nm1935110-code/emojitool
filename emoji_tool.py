#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import base64
import random
import glob
import argparse

# màu 
G = '\033[92m'
R = '\033[91m'
B = '\033[94m'
E = '\033[0m'

# 90 emoji đủ xài mọi người muốn thêm tự thêm ad bị lười 😇
emojis = [
    "😀","😃","😄","😁","😆","😅","😂","🤣","😊","😇","🙂","🙃","😉","😌","😍","🥰",
    "😘","😗","😙","😚","😋","😛","😝","😜","🤪","🤨","🧐","🤓","😎","🥸","🤩","🥳",
    "😏","😒","😞","😔","😟","😕","🙁","☹️","😣","😖","😫","😩","🥺","😢","😭","😤",
    "😠","😡","🤬","🤯","😳","🥵","🥶","😱","😨","😰","😥","😓","🤗","🤔","🤭","🤫",
    "🤥","😶","😐","😑","😬","🙄","😯","😦","😧","😮","😲","🥱","😴","🤤","😪","😵",
    "🤐","🥴","🤢","🤮","🤧","😷","🤒","🤕","🤑","🤠"
]

# unicode selectors để giấu 
vs = [chr(0xFE00 + i) for i in range(16)] + [chr(0xE0100 + i) for i in range(80)]
vs_fwd = {i: vs[i] for i in range(96)}
vs_rev = {v: k for k, v in vs_fwd.items()}

# tag chars
tg = [chr(0xE0040 + i) for i in range(64)]
tg_fwd = {i: tg[i] for i in range(64)}
tg_rev = {v: k for k, v in tg_fwd.items()}

def encode_v(data, e="😈"):
    if not data:
        return e
    out = []
    for b in data:
        if b < 96:
            out.append(vs_fwd[b])
        else:
            out.append(vs_fwd[b // 96])
            out.append(vs_fwd[b % 96])
    return e + ''.join(out)

def decode_v(s):
    if not s or len(s) < 2:
        return None
    p = s[1:]
    res = []
    i = 0
    while i < len(p):
        if p[i] not in vs_rev:
            i += 1
            continue
        v1 = vs_rev[p[i]]
        i += 1
        if v1 < 96:
            res.append(v1)
            continue
        if i >= len(p) or p[i] not in vs_rev:
            res.append(v1)
            continue
        v2 = vs_rev[p[i]]
        res.append((v1 - 96) * 96 + v2)
        i += 1
    return bytes(res) if res else None

def encode_t(data, e="😈"):
    if not data:
        return e
    out = []
    for b in data:
        if 32 <= b <= 126:
            out.append(tg_fwd[b - 32])
    return e + ''.join(out)

def decode_t(s):
    if not s or len(s) < 2:
        return None
    res = []
    for ch in s[1:]:
        if ch in tg_rev:
            res.append(tg_rev[ch] + 32)
    return bytes(res) if res else None

def trim(s):
    if not s:
        return s
    keep = [s[0]]
    for ch in s[1:]:
        if ch not in vs_rev and ch not in tg_rev:
            keep.append(ch)
    return ''.join(keep)

def read_file(path):
    try:
        with open(path, 'rb') as f:
            return f.read()
    except:
        return None

def write_file(path, data):
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(data)
        return True
    except:
        return False

def find_files(patt):
    return glob.glob(patt)

def main():
    # cli mode
    if len(sys.argv) > 1:
        p = argparse.ArgumentParser()
        p.add_argument('-f', '--file')
        p.add_argument('-t', '--text')
        p.add_argument('-d', '--decode')
        p.add_argument('-m', choices=['v','t'], default='v')
        p.add_argument('-e', default='😈')
        p.add_argument('-o', '--output')
        args = p.parse_args()
        
        if args.decode:
            x = decode_v(args.decode) or decode_t(args.decode)
            if not x:
                print("can't decode")
                return
            if args.output:
                with open(args.output, 'wb') as f:
                    f.write(x)
                print("ok")
            else:
                try:
                    print(x.decode())
                except:
                    print(x.hex())
        elif args.file or args.text:
            data = None
            if args.file:
                data = read_file(args.file)
            else:
                data = args.text.encode()
            if not data:
                print("can't read file")
                return
            out = encode_v(data, args.e) if args.m == 'v' else encode_t(data, args.e)
            if args.output:
                write_file(args.output, out)
                print("ok")
            else:
                print(out)
        return
    
    # interactive mode
    cur_data = None
    cur_enc = None
    cur_method = 'v'
    cur_e = '😈'
    
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        print("\n=== emoji smuggler ===\n")
        print("1. load file")
        print("2. manual input")
        print("3. method [{}]".format('variant' if cur_method=='v' else 'tag'))
        print("4. emoji [{}]".format(cur_e))
        print("5. encode")
        print("6. show")
        print("7. decode")
        print("8. trim")
        print("9. save")
        print("10. random emoji")
        print("11. generate variants")
        print("12. ls")
        print("0. exit")
        
        if cur_data:
            h = cur_data[:20].hex()
            if len(cur_data) > 20:
                h += '...'
            print("\n> data: {}".format(h))
        if cur_enc:
            prv = cur_enc[:30]
            if len(cur_enc) > 30:
                prv += '...'
            print("> encoded: {}".format(repr(prv)))
        
        c = input("\nchoice: ").strip()
        
        if c == '1':
            path = input("path: ").strip()
            if not path:
                continue
            if '*' in path or '?' in path:
                fl = find_files(path)
                if not fl:
                    print("no files found")
                    input("enter...")
                    continue
                for i, f in enumerate(fl):
                    sz = os.path.getsize(f) if os.path.isfile(f) else 0
                    print("{}. {} ({}b)".format(i+1, f, sz))
                sel = input("choose: ").strip()
                try:
                    idx = int(sel) - 1
                    if idx < 0 or idx >= len(fl):
                        continue
                    path = fl[idx]
                except:
                    continue
            data = read_file(path)
            if data:
                cur_data = data
                print("ok {} bytes".format(len(data)))
        
        elif c == '2':
            print("1. text")
            print("2. hex")
            print("3. base64")
            t = input("choose: ").strip()
            if t == '1':
                s = input("text: ")
                cur_data = s.encode()
                print("ok {} bytes".format(len(cur_data)))
            elif t == '2':
                s = input("hex: ").replace(' ', '').replace('\\x', '')
                try:
                    cur_data = bytes.fromhex(s)
                    print("ok {} bytes".format(len(cur_data)))
                except:
                    print("invalid hex")
            elif t == '3':
                s = input("base64: ")
                try:
                    cur_data = base64.b64decode(s)
                    print("ok {} bytes".format(len(cur_data)))
                except:
                    print("invalid base64")
        
        elif c == '3':
            print("1. variant (all)")
            print("2. tag (ascii)")
            m = input("choose: ").strip()
            if m == '1':
                cur_method = 'v'
                print("method: variant")
            elif m == '2':
                cur_method = 't'
                print("method: tag")
        
        elif c == '4':
            print("emoji list:")
            for i in range(0, len(emojis), 8):
                row = emojis[i:i+8]
                print(' '.join("{:2}.{}".format(i+j+1, e) for j, e in enumerate(row)))
            e = input("choose (1-{} or paste): ".format(len(emojis))).strip()
            try:
                idx = int(e) - 1
                if 0 <= idx < len(emojis):
                    cur_e = emojis[idx]
                    print("ok " + cur_e)
            except:
                if e:
                    cur_e = e
                    print("ok " + cur_e)
        
        elif c == '5':
            if not cur_data:
                print("no data")
                continue
            if cur_method == 'v':
                cur_enc = encode_v(cur_data, cur_e)
            else:
                cur_enc = encode_t(cur_data, cur_e)
            print("encoded ({} chars)".format(len(cur_enc)))
        
        elif c == '6':
            if not cur_enc:
                print("not encoded")
                continue
            print("\n" + cur_enc)
            print("\nhex:")
            hx = []
            for ch in cur_enc[:20]:
                hx.append('{:04x}'.format(ord(ch)))
            print(' '.join(hx) + ('...' if len(cur_enc) > 20 else ''))
        
        elif c == '7':
            s = input("paste emoji: ").strip()
            if not s:
                continue
            d = decode_v(s) or decode_t(s)
            if not d:
                print("no data found")
                continue
            print("ok {} bytes".format(len(d)))
            try:
                print("text: {}".format(d.decode()))
            except:
                pass
            print("hex: {}".format(d.hex()))
            print("b64: {}".format(base64.b64encode(d).decode()))
        
        elif c == '8':
            s = input("paste emoji: ").strip()
            if s:
                print("result: {}".format(trim(s)))
        
        elif c == '9':
            if not cur_enc:
                print("nothing to save")
                continue
            name = input("filename: ").strip()
            if name and write_file(name, cur_enc):
                print("ok")
        
        elif c == '10':
            cur_e = random.choice(emojis)
            print("ok " + cur_e)
        
        elif c == '11':
            if not cur_data:
                print("no data")
                continue
            try:
                n = int(input("count (max 20): ") or "5")
                n = min(max(n, 1), 20)
            except:
                n = 5
            lst = []
            for i in range(n):
                e = random.choice(emojis)
                m = random.choice(['v','t'])
                if m == 'v':
                    out = encode_v(cur_data, e)
                else:
                    out = encode_t(cur_data, e)
                lst.append((e, m, out))
                print("\n{}. {} [{}]".format(i+1, e, 'var' if m=='v' else 'tag'))
                print("   {}".format(repr(out[:60]) + ('...' if len(out)>60 else '')))
            if input("\nsave? (y/n): ").lower() == 'y':
                fn = input("filename: ").strip()
                if fn:
                    with open(fn, 'w', encoding='utf-8') as f:
                        for i, (e, m, out) in enumerate(lst, 1):
                            f.write("[{}] {} ({})\n{}\n\n".format(i, e, m, out))
                    print("ok")
        
        elif c == '12':
            p = input("pattern (default *): ").strip() or "*"
            fl = find_files(p)
            if not fl:
                print("not found")
            else:
                for i, f in enumerate(fl):
                    sz = os.path.getsize(f) if os.path.isfile(f) else 0
                    print("{:3}. {} ({}b)".format(i+1, f, sz))
        
        elif c == '0':
            print("bye")
            break
        
        if c in [str(x) for x in range(1,13)]:
            input("\nenter...")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nbye")
    except Exception as e:
        print("\nerror: {}".format(e))