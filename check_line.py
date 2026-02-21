#!/usr/bin/env python
# -*- coding: utf-8 -*-

with open(r'C:\Users\Eagle\Desktop\ballsackblud.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
if len(lines) > 2805:
    line = lines[2805]
    print(f"Line 2806 length: {len(line)}")
    print(f"First 200 chars: {repr(line[:200])}")
    print(f"Looking for return statement...")
    if 'return' in line:
        idx = line.find('return')
        print(f"Found 'return' at position {idx}")
        print(f"Content around return: {repr(line[idx:idx+150])}")
