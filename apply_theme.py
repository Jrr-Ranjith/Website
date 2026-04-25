import os
import re

files = ["electrical-and-plumbing.html", "chairs-and-furnitures.html", "mechanical-design.html"]

css_addition = """
        /* THEME TOGGLE STYLES */
        :root[data-theme="dark"] {
            --gray-50: #0b1a33;
            --gray-100: #122040;
            --gray-200: rgba(255, 255, 255, 0.1);
            --gray-400: #94a3b8;
            --gray-600: rgba(255, 255, 255, 0.7);
            --gray-800: #ffffff;
            --white: #122040;
            --navy: #f8fafc;
        }
        
        .theme-toggle {
            display: inline-flex; align-items: center; justify-content: center;
            width: 38px; height: 38px; border-radius: 50%;
            background: rgba(255,255,255,0.15); color: var(--white);
            border: 1px solid rgba(255,255,255,0.3); transition: 0.3s;
            margin-right: 15px; font-size: 1.1rem;
        }
        .theme-toggle:hover { background: var(--gold); border-color: var(--gold); color: #fff; }
        :root[data-theme="dark"] .theme-toggle { color: #fff; }
"""

js_addition = """
        // ── THEME TOGGLE ──
        const themeToggle = document.getElementById('themeToggle');
        const root = document.documentElement;
        if(themeToggle) {
            const iconSpan = themeToggle.querySelector('.icon');
            
            // Note: Index page defaults to Dark. These pages default to Light.
            // If theme is 'light', we do nothing. If theme is 'dark', we apply dark mode here.
            const savedTheme = localStorage.getItem('theme') || 'dark';
            if (savedTheme === 'dark') {
                root.setAttribute('data-theme', 'dark');
                iconSpan.textContent = '☀';
            } else {
                root.removeAttribute('data-theme');
                iconSpan.textContent = '🌙';
            }

            themeToggle.addEventListener('click', () => {
                const isDark = root.hasAttribute('data-theme');
                if (isDark) {
                    root.removeAttribute('data-theme');
                    localStorage.setItem('theme', 'light');
                    iconSpan.textContent = '🌙';
                } else {
                    root.setAttribute('data-theme', 'dark');
                    localStorage.setItem('theme', 'dark');
                    iconSpan.textContent = '☀';
                }
            });
        }
"""

button_html = """            <button class="theme-toggle" id="themeToggle" aria-label="Toggle Theme">
                <span class="icon">🌙</span>
            </button>
            <button id="hamburger">"""

for fname in files:
    if not os.path.exists(fname): continue
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # REMOVE LOADER HTML (id="jrr-loader" or id="premium-3d-loader" or id="modern-loader" or similar)
    # The regex tries to find the top level loader div and its children.
    content = re.sub(r'<!--[^>]*LOADER[^>]*-->\s*<div id="(?:jrr-loader|premium-3d-loader|loader)[^>]*>.*?</div>\s*(<!--[^>]*HEADER|\s*<header)', r'\1', content, flags=re.DOTALL|re.IGNORECASE)
    # Another pattern for ones that didn't match perfectly:
    content = re.sub(r'<div id="(?:jrr-loader|premium-3d-loader|loader)[^>]*>.*?</div>\s*(<header)', r'\1', content, flags=re.DOTALL|re.IGNORECASE)

    # Add Theme Toggle Button
    if '<button id="hamburger">' in content and 'id="themeToggle"' not in content:
        content = content.replace('<button id="hamburger">', button_html)
        
    # Add CSS
    if '/* THEME TOGGLE STYLES */' not in content:
        content = content.replace('</style>', css_addition + '</style>')
        
    # Add JS
    if '── THEME TOGGLE ──' not in content:
        content = content.replace('</script>', js_addition + '</script>')
        
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(content)
        
print("Updated all secondary pages.")
