#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Read the file
with open(r'C:\Users\Eagle\Desktop\ballsackblud.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the end of the proper return statement and the start of garbage
proper_end = 'return `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(svg)}`;'
proper_idx = content.find(proper_end)

if proper_idx == -1:
    print("ERROR: Could not find the proper return statement ending")
else:
    # The proper statement ends after the semicolon
    clean_end = proper_idx + len(proper_end)
    
    # Find the next newline and closing brace
    next_newline = content.find('\n    }', clean_end)
    
    if next_newline == -1:
        print("ERROR: Could not find closing brace")
    else:
        # Everything between clean_end and next_newline is garbage
        garbage = content[clean_end:next_newline]
        print(f"Found {len(garbage)} characters of garbage")
        print(f"Garbage starts with: {repr(garbage[:50])}")
        
        # Remove the garbage
        new_content = content[:clean_end] + content[next_newline:]
        
        # Write back
        with open(r'C:\Users\Eagle\Desktop\ballsackblud.html', 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("✓ File successfully cleaned!")
