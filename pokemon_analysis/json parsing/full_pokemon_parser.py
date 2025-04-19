
import re
import json

def extract_float(line):
    match = re.search(r"\d+\.\d+|\d+", line)
    return float(match.group()) if match else None

def parse_section(lines):
    data = {}
    for line in lines:
        if "%" in line:
            parts = line.strip("| ").rsplit(" ", 1)
            if len(parts) == 2:
                key, value = parts
                key = key.strip()
                value = float(value.strip("% "))
                data[key] = value
    return data

def parse_teammates(lines):
    teammates = {}
    for line in lines:
        if "%" in line:
            parts = line.strip("| ").rsplit(" ", 1)
            if len(parts) == 2:
                name, percent = parts
                teammates[name.strip()] = float(percent.strip("% "))
    return teammates

def parse_counters(lines):
    counters = []
    i = 0
    while i < len(lines):
        line = lines[i].strip("| ").strip()
        if "(" in line and ")" in line:
            name = re.sub(r"\s+\(.*?\)", "", line)
            score_match = re.search(r"\(([\d.]+)±([\d.]+)\)", line)
            if score_match:
                score = float(score_match.group(1))
                std = float(score_match.group(2))
            else:
                score = std = None
            i += 1
            outcome = lines[i].strip("| ").strip("() ")
            ko_rate_match = re.search(r"([\d.]+)% KOed", outcome)
            switch_rate_match = re.search(r"([\d.]+)% switched out", outcome)
            ko_rate = float(ko_rate_match.group(1)) if ko_rate_match else None
            switch_rate = float(switch_rate_match.group(1)) if switch_rate_match else None
            counters.append({
                "Name": name,
                "Score": score,
                "Stdev": std,
                "KOed": ko_rate,
                "Switched Out": switch_rate
            })
        i += 1
    return counters

def parse_pokemon_blocks(raw_text):
    split_blocks = raw_text.split("+----------------------------------------+")
    structured_blocks = []
    current_block = []

    for line in split_blocks:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("|") and not any(header in stripped for header in ["Raw count", "Abilities", "Items", "Spreads", "Moves", "Tera Types", "Teammates", "Checks and Counters"]):
            if current_block:
                structured_blocks.append("\n".join(current_block))
            current_block = [stripped]
        else:
            current_block.append(stripped)
    if current_block:
        structured_blocks.append("\n".join(current_block))

    return structured_blocks

def parse_all_pokemon(text):
    blocks = parse_pokemon_blocks(text)
    required_keys = ["Abilities", "Items", "Spreads", "Moves", "Tera Types"]
    parsed_data = []

    for block in blocks:
        lines = block.splitlines()
        name_line = lines[0].strip("| ").strip()
        entry = {"Pokemon": name_line}

        i = 1
        while i < len(lines):
            line = lines[i]
            if "Raw count" in line:
                entry["Raw Count"] = int(re.search(r"\d+", line).group())
            elif "Avg. weight" in line:
                value = extract_float(line)
                if value is not None:
                    entry["Avg Weight"] = value
            elif "Viability Ceiling" in line:
                entry["Viability Ceiling"] = int(re.search(r"\d+", line).group())
            elif "Abilities" in line:
                section = []
                i += 1
                while i < len(lines) and not lines[i].startswith("|"):
                    section.append(lines[i])
                    i += 1
                entry["Abilities"] = parse_section(section)
                continue
            elif "Items" in line:
                section = []
                i += 1
                while i < len(lines) and not lines[i].startswith("|"):
                    section.append(lines[i])
                    i += 1
                entry["Items"] = parse_section(section)
                continue
            elif "Spreads" in line:
                section = []
                i += 1
                while i < len(lines) and not lines[i].startswith("|"):
                    section.append(lines[i])
                    i += 1
                entry["Spreads"] = parse_section(section)
                continue
            elif "Moves" in line:
                section = []
                i += 1
                while i < len(lines) and not lines[i].startswith("|"):
                    section.append(lines[i])
                    i += 1
                entry["Moves"] = parse_section(section)
                continue
            elif "Tera Types" in line:
                section = []
                i += 1
                while i < len(lines) and not lines[i].startswith("|"):
                    section.append(lines[i])
                    i += 1
                entry["Tera Types"] = parse_section(section)
                continue
            elif "Teammates" in line:
                section = []
                i += 1
                while i < len(lines) and not lines[i].startswith("|"):
                    section.append(lines[i])
                    i += 1
                entry["Teammates"] = parse_teammates(section)
                continue
            elif "Checks and Counters" in line:
                section = []
                i += 1
                while i < len(lines) and not lines[i].startswith("|"):
                    section.append(lines[i])
                    i += 1
                entry["Checks and Counters"] = parse_counters(section)
                continue
            i += 1

        if all(k in entry for k in required_keys):
            parsed_data.append(entry)

    return parsed_data

# Example usage:
# with open("gen9ou-0.txt", "r") as f:
#     raw = f.read()
# parsed = parse_all_pokemon(raw)
# with open("gen9ou_full_data.json", "w") as out:
#     json.dump(parsed, out, indent=4)
