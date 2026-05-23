import os, glob

replacements = {
    '<span class="nav-icon">🏠</span>': '<i class="ph ph-house nav-icon"></i>',
    '<span class="nav-icon">🔍</span>': '<i class="ph ph-magnifying-glass nav-icon"></i>',
    '<span class="nav-icon">🧭</span>': '<i class="ph ph-compass nav-icon"></i>',
    '<span class="nav-icon">🎬</span>': '<i class="ph ph-video-camera nav-icon"></i>',
    '<span class="nav-icon">💬</span>': '<i class="ph ph-chat-circle nav-icon"></i>',
    '<span class="nav-icon">🔔</span>': '<i class="ph ph-bell nav-icon"></i>',
    '<span class="nav-icon">➕</span>': '<i class=\"ph ph-plus-circle nav-icon\"></i>',
    '<span class="nav-icon">👤</span>': '<i class="ph ph-user nav-icon"></i>',
    '<span class="nav-icon">🌙</span>': '<i class="ph ph-moon nav-icon"></i>',
    '<span class="nav-icon">🚪</span>': '<i class="ph ph-sign-out nav-icon"></i>',
}

files = glob.glob('myapp/templates/myapp/*.html')
for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    original_content = content
    for old, new in replacements.items():
        content = content.replace(old, new)
        
    if content != original_content:
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f'Updated {f}')
