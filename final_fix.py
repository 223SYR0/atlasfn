#!/usr/bin/env python
# -*- coding: utf-8 -*-

with open(r'C:\Users\Eagle\Desktop\ballsackblud.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the location of the return statement with the SVG
start = content.find('return `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(svg)}`')
if start == -1:
    print("ERROR: Could not find the return statement")
else:
    # Find where it should end - with a semicolon
    end = start + len('return `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(svg)}`')
    
    # The line should end with a semicolon
    if end < len(content) and content[end] == ';':
        end += 1  # Include the semicolon
        
        # Check if there's garbage after it before the closing brace
        after_semi = content[end:]
        # Look for the next newline and closing brace pattern
        newline_idx = after_semi.find('\n    }')
        
        if newline_idx > 0:
            # Everything between 'end' and the newline is garbage (if any)
            garbage = after_semi[:newline_idx]
            if garbage.strip():
                print(f"Found garbage of {len(garbage)} characters")
                print(f"Garbage starts with: {repr(garbage[:50])}")
                # Remove the garbage
                content = content[:end] + after_semi[newline_idx:]
                
                # Write back
                with open(r'C:\Users\Eagle\Desktop\ballsackblud.html', 'w', encoding='utf-8') as f:
                    f.write(content)
                print("✓ File successfully cleaned!")
            else:
                print("No garbage found")
        else:
            print(f"Could not find closing brace after return statement")
    else:
        print(f"Expected semicolon at position {end}")

