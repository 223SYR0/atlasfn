#!/usr/bin/env python
# -*- coding: utf-8 -*-

with open(r'C:\Users\Eagle\Desktop\ballsackblud.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Line 2806 (index 2805) contains the return statement with garbage
line_idx = 2805
line = lines[line_idx]

print(f"Original line length: {len(line)}")
print(f"First 100 chars: {repr(line[:100])}")

# Find the proper return statement  
proper_return = "return `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(svg)}`;"
idx = line.find(proper_return)

if idx >= 0:
    end_idx = idx + len(proper_return)
    # Get everything up to and including the proper return statement, then the newline
    fixed_line = line[:end_idx] + '\n'
    
    print(f"Fixed line: {repr(fixed_line)}")
    
    # Check if there's garbage after
    after = line[end_idx:]
    print(f"Removed {len(after)-1} characters of garbage")  # -1 for the newline
    
    # Replace the line
    lines[line_idx] = fixed_line
    
    # Write back
    with open(r'C:\Users\Eagle\Desktop\ballsackblud.html', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print("✓ File successfully fixed!")
else:
    print(f"ERROR: Could not find proper return statement in line")
