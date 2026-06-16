import textwrap

lyrics_raw = """"""

def format_for_lcd(text, cols=16):
    """
    Split lyrics into 16-char lines, then pair into 2-line LCD frames.
    Each frame = row1\nrow2
    Frames are separated by a blank line in the file.
    Arduino reads until blank line, displays row1 on line 1, row2 on line 2.
    """
    # Wrap every source line to 16 chars
    wrapped = []
    for line in text.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        chunks = textwrap.wrap(line, width=cols)
        if not chunks:
            continue
        wrapped.extend(chunks)

    # Pair into 2-line frames
    frames = []
    for i in range(0, len(wrapped), 2):
        row1 = wrapped[i].ljust(cols)
        row2 = wrapped[i+1].ljust(cols) if i+1 < len(wrapped) else " " * cols
        frames.append((row1, row2))

    return frames

frames = format_for_lcd(lyrics_raw)

# Write output file
out_lines = []
for r1, r2 in frames:
    out_lines.append(r1)
    out_lines.append(r2)
    out_lines.append("")  # blank line = frame separator for Arduino

output = "\n".join(out_lines).rstrip() + "\n"

with open("T01.TXT", "w", newline="\n") as f:
    f.write(output)

# Print preview
print(f"Total frames: {len(frames)}\n")
print("=" * 20)
for i, (r1, r2) in enumerate(frames):
    print(f"Frame {i+1:02d}:")
    print(f"|{r1}|")
    print(f"|{r2}|")
    print("-" * 20)
