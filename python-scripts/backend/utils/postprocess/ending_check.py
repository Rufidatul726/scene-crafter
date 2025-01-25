def ensure_nodes_end_with_newline(scene_content):
    """Ensure that every node in the scene ends with a newline."""
    scene_lines = scene_content.splitlines()  # Split the scene into individual lines
    cleaned_lines = []

    for line in scene_lines:
        # Skip lines that don’t meet our conditions (without line-end, not resource or node related)
        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # 1.1. Bracket Validation: Lines starting with '[' must end with ']'
        if line.startswith('[') and not line.endswith(']'):
            continue  # Skip this line if it does not end with ']'

        # 1.2. Bracket Validation: Lines starting with '{' must end with '}'
        if line.startswith('{') and not line.endswith('}'):
            continue  # Skip this line if it does not end with ']'

        # 1.3. Bracket Validation: Lines starting with '[' must end with ']'
        if line.startswith('(') and not line.endswith(')'):
            continue  # Skip this line if it does not end with ']'

        # 2. Quote Validation: Lines starting with '"' must have closing '"'
        if '"' in line and line.count('"') % 2 != 0:
            continue  # Skip this line if there's an unmatched quote

        # 3. Equals Validation: Lines with '=' must have something after it (right side must exist)
        if '=' in line and len(line.split('=', 1)[1].strip()) == 0:
            continue  # Skip lines where '=' has no right side value

        # If the line passed all checks, it's valid, so we keep it
        cleaned_lines.append(line)
    
    # Reassemble the scene content
    cleaned_scene = "\n".join(cleaned_lines)
    return cleaned_scene
