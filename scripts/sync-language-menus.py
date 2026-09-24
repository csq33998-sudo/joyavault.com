"""Synchronize language menus and hreflang while preserving every page design."""
import sys
from localization import ROOT, LANGUAGES, sync_language_menu

def run(check=False):
    changed = []
    for lang in LANGUAGES:
        for path in sorted((ROOT / lang).rglob('index.html')):
            source = path.read_text(encoding='utf-8')
            output = sync_language_menu(path, source)
            if output != source:
                changed.append(str(path.relative_to(ROOT)))
                if not check:
                    path.write_text(output, encoding='utf-8', newline='\n')
    print(f'Language menus: {len(changed)} ' + ('out of sync' if check else 'updated'))
    return int(check and bool(changed))

if __name__ == '__main__':
    sys.exit(run('--check' in sys.argv))
