#!/usr/bin/env python3
import requests
from datetime import datetime
import subprocess
import textwrap

def get_ascii_image(image_path, size="35x20"):
    result = subprocess.run(
        ["chafa", "--size", size, image_path],
        capture_output=True,
        text=True
    )
    return result.stdout.splitlines()

def get_wrapped_kural(data, width=60):
    lines = []

    lines.append(f"{BOLD}{BLUE}🪷 Thirukkural #{data['number']}: {data['athigaram']} ({data['paal']}){RESET}")
    lines.append("")

    # Add Kural lines in white bold
    lines.append(f"{CYAN}{BOLD}{data['line1']}{RESET}")
    lines.append(f"{CYAN}{BOLD}{data['line2']}{RESET}")
    lines.append("")

    # English Translation
    lines.append(f"{YELLOW}{BOLD}📜 English Translation:{RESET}")
    lines += [f"{YELLOW}{line}{RESET}" for line in textwrap.wrap(data['translation'], width=width)]
    lines.append("")

    # Tamil Explanation
    lines.append(f"{MAGENTA}{BOLD}🎓 Tamil Explanation (மு.கருணாநிதி):{RESET}")
    lines += [f"{MAGENTA}{line}{RESET}" for line in textwrap.wrap(data['urai2'], width=width)]

    return lines


def print_side_by_side(left_lines, right_lines, gap=4):
    max_lines = max(len(left_lines), len(right_lines))
    left_lines += [''] * (max_lines - len(left_lines))
    right_lines += [''] * (max_lines - len(right_lines))

    for left, right in zip(left_lines, right_lines):
        print(left.ljust(40) + ' ' * gap + right)

# Get today's Thirukkural
# ANSI color codes
RESET = "\033[0m"
BOLD = "\033[1m"

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"

day = datetime.now().timetuple().tm_yday
day = ((day - 1) % 1330) + 1
url = f"https://getthirukural.appspot.com/api/3.0/kural/{day}?appid=ebpd84rly7hik"


try:
    res = requests.get(url)
    data = res.json()

    if 'number' not in data:
        raise ValueError("Invalid Kural structure")

    ascii_image = get_ascii_image("/home/keera/Downloads/blue1.png", size="35x20")
    kural_text = get_wrapped_kural(data, width=60)

    print_side_by_side(ascii_image, kural_text)

except Exception as e:
    print("❌ Error fetching or displaying Kural")
    print("Exception:", e)
