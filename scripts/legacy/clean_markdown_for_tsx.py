"""Clean Markdown formatting from the generated page.tsx content sections.

Removes #, ##, ###, **, ---, and converts - bullets to -- format.
Processes the TSX file in-place.
"""
import re
import sys


def clean_markdown_value(text: str) -> str:
    """Clean Markdown syntax from a content section value."""
    lines = text.split("\\n")
    cleaned = []

    for line in lines:
        original = line

        # Remove heading markers: # ## ### ####
        line = re.sub(r'^#{1,4}\s+', '', line)

        # Remove horizontal rules
        if line.strip() == '---':
            continue

        # Convert **bold** to plain text (remove markers)
        line = re.sub(r'\*\*([^*]+)\*\*', r'\1', line)

        # Convert *italic* to plain text
        line = re.sub(r'\*([^*]+)\*', r'\1', line)

        # Convert - bullet to -- bullet (template convention)
        line = re.sub(r'^- ', '-- ', line)

        # Convert numbered list markers to cleaner format
        # Keep "1. " style as-is (template handles it)

        # Remove leading | for table rows - convert to readable text
        if line.startswith('| '):
            # Table row - skip header separators
            if re.match(r'^\|[\s\-|]+\|$', line):
                continue
            # Clean table formatting
            cells = [c.strip() for c in line.split('|') if c.strip()]
            if cells:
                line = ' | '.join(cells)

        cleaned.append(line)

    # Rejoin and remove excessive blank lines
    result = "\\n".join(cleaned)

    # Remove multiple consecutive blank lines
    result = re.sub(r'(\\n){3,}', '\\\\n\\\\n', result)

    # Remove trailing/leading whitespace from the value
    result = result.strip('\\n').strip()

    return result


def process_tsx_file(filepath: str):
    """Process the TSX file to clean all content section values."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all section value strings: { type: "text", value: "..." }
    # Pattern matches the value string in content sections
    def clean_match(m):
        prefix = m.group(1)  # everything before the value
        value = m.group(2)    # the value content
        suffix = m.group(3)   # closing quote and rest

        cleaned = clean_markdown_value(value)
        return f'{prefix}{cleaned}{suffix}'

    # Match: type: "text", value: "..." or type: "warning", value: "..." etc
    pattern = r'(\{ type: "(?:text|warning|tip)", value: ")(.*?)(" \})'
    content = re.sub(pattern, clean_match, content)

    # Also clean checkpoint values
    pattern2 = r'(\{ type: "checkpoint", value: ")(.*?)(" \})'
    content = re.sub(pattern2, clean_match, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Cleaned: {filepath}")


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "C:/Sandyboxclaude/landing-page-geo/src/app/educacao/seo-geo-revendedoras-joias/page.tsx"
    process_tsx_file(path)
