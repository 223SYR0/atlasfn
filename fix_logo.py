#!/usr/bin/env python3

file_path = r'C:\Users\Eagle\Desktop\ballsackblud.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Check if the problematic content exists
if '`data:image/svg+xml;charset=UTF-8,${encodeURIComponent(svg)}`;AAAgAElEQVR' in content:
    print("✓ Found the orphaned base64 pattern!")
    
    # Find the exact position
    bad_marker = '`;AAAgAElEQVR'
    good_marker = 'function handleLogoError(img)'
    
    start_idx = content.find(bad_marker)
    end_idx = content.find(good_marker, start_idx)
    
    if start_idx >= 0 and end_idx > start_idx:
        # Extract the clean part (up to and including the backtick and semicolon)
        before = content[:start_idx + 2]  # +2 for `; 
        after = '\n    }\n\n    ' + content[end_idx:]
        
        new_content = before + after
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("✓ Successfully cleaned the function!")
    else:
        print(f"✗ Could not find markers (start={start_idx}, end={end_idx})")
else:
    print("✗ Pattern not found - checking what we have...")
