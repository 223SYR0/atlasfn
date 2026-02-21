#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Read the entire file
with open(r'C:\Users\Eagle\Desktop\ballsackblud.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the getFallbackLogoDataUrl function
start_marker = 'function getFallbackLogoDataUrl() {'
end_marker = '    function handleLogoError(img) {'

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print("ERROR: Could not find function boundaries")
else:
    # Extract the function
    func_section = content[start_idx:end_idx]
    
    # Build the clean function
    clean_func = '''function getFallbackLogoDataUrl() {
      const svg = `
        <svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 200 200">
          <defs>
            <linearGradient id="purpleGrad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" style="stop-color:#d8b4fe;stop-opacity:1" />
              <stop offset="50%" style="stop-color:#a855f7;stop-opacity:1" />
              <stop offset="100%" style="stop-color:#581c87;stop-opacity:1" />
            </linearGradient>
          </defs>
          <!-- Left side of A -->
          <polygon points="50,170 100,30 100,170" fill="url(#purpleGrad)" />
          <!-- Right side of A -->
          <polygon points="100,170 150,30 150,170" fill="url(#purpleGrad)" opacity="0.85" />
          <!-- Horizontal bar -->
          <rect x="55" y="110" width="90" height="12" fill="url(#purpleGrad)" />
          <!-- Diagonal line cut -->
          <line x1="70" y1="115" x2="140" y2="165" stroke="rgba(255,255,255,0.25)" stroke-width="10" stroke-linecap="round" />
        </svg>
      `;
      return `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(svg)}`;
    }

    '''
    
    # Replace the corrupted function
    new_content = content[:start_idx] + clean_func + content[end_idx:]
    
    # Write back
    with open(r'C:\Users\Eagle\Desktop\ballsackblud.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✓ File successfully fixed!")
    print(f"Original function length: {len(func_section)}")
    print(f"Removed approximately {len(func_section) - len(clean_func)} bytes of garbage")
