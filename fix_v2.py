#!/usr/bin/env python
# -*- coding: utf-8 -*-

with open(r'C:\Users\Eagle\Desktop\ballsackblud.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the return statement line - we need to find where it ends
# The proper return statement is: return `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(svg)}`;
# followed by a newline and then the closing brace

# Strategy: find the line with this return statement and extract just the good part until the first newline after the semicolon

lines = content.split('\n')
for i, line in enumerate(lines):
    if 'return `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(svg)}`' in line:
        print(f"Found return statement at line {i}")
        print(f"Line content (first 150 chars): {repr(line[:150])}")
        print(f"Line content (last 100 chars): {repr(line[-100:])}")
        
        # The line should be:  return `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(svg)}`;
        # If there's garbage after it, remove it
        # Find where the proper return statement ends (after the semicolon that comes after the closing backtick)
        proper_end = line.find('${encodeURIComponent(svg)}`') + len('${encodeURIComponent(svg)}`')
        if proper_end > 0 and proper_end < len(line):
            # Check if there's a semicolon right after
            if line[proper_end] == ';':
                proper_end += 1  # Include the semicolon
                # Everything after this should be garbage
                if proper_end < len(line):
                    garbage = line[proper_end:]
                    print(f"Found garbage of length {len(garbage)}")
                    print(f"Garbage starts with: {repr(garbage[:50])}")
                    
                    # Remove the garbage
                    lines[i] = line[:proper_end]
                    print(f"Fixed line (first 150 chars): {repr(lines[i][:150])}")
                    
                    # Write back
                    with open(r'C:\Users\Eagle\Desktop\ballsackblud.html', 'w', encoding='utf-8') as f:
                        f.write('\n'.join(lines))
                    print("✓ File successfully cleaned!")
                else:
                    print("No garbage found after semicolon")
            else:
                print(f"Expected semicolon at position {proper_end}, but found '{line[proper_end]}'")
        break
