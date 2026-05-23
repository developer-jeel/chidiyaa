import os, glob

replacements = {
    'Chidiyaa 🐦': 'Chidiyaa <i class="ph ph-bird"></i>',
    '<button class="theme-toggle-btn">🌙</button>': '<button class="theme-toggle-btn"><i class="ph ph-moon"></i></button>',
    '<a href="create.html"><button>➕</button></a>': '<a href="create.html"><button><i class="ph ph-plus"></i></button></a>',
    '💬<span': '<i class="ph ph-chat-circle"></i><span',
    'Chidiyaa 📷': 'Chidiyaa <i class="ph ph-camera"></i>',
    'Farm Manager 🌾': 'Farm Manager <i class="ph ph-plant"></i>',
    '🎨': '<i class="ph ph-palette"></i>',
    '🚀': '<i class="ph ph-rocket"></i>',
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
