#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

with open(r'C:\Users\Eagle\Desktop\ballsackblud.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the return statement with the orphaned base64 data
# The pattern is: return `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(svg)}`;
# followed by a large base64 string that shouldn't be there

# Use a simpler approach - find the line and replace it
idx = content.find("return `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(svg)}`")
if idx >= 0:
    # Find the semicolon after the return statement
    semicolon_idx = content.find(";", idx)
    if semicolon_idx >= 0:
        # Check what comes after the semicolon
        after_semi = content[semicolon_idx:semicolon_idx+50]
        print(f"After semicolon: {repr(after_semi)}")
        
        # Look for the next newline or closing brace after semicolon
        # The goal is to remove the orphaned base64 data between semicolon and the newline
        newline_idx = content.find("\n", semicolon_idx)
        if newline_idx >= 0:
            stuff_after = content[semicolon_idx+1:newline_idx]
            print(f"Content between semicolon and newline: {repr(stuff_after)}")
            
            # If it's not empty (i.e., has base64 garbage), remove it
            if stuff_after and stuff_after[0].isalnum() or stuff_after[0] in '+=':
                print("Found orphaned data! Removing...")
                # Replace with just the return statement and newline
                content = content[:semicolon_idx+1] + content[newline_idx:]
                
                with open(r'C:\Users\Eagle\Desktop\ballsackblud.html', 'w', encoding='utf-8') as f:
                    f.write(content)
                print("✓ File cleaned!")
            else:
                print("No orphaned data found after semicolon")
        else:
            print("Could not find newline after return statement")
else:
    print("Could not find return statement")
