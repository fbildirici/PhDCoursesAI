import re

def main():
    entity_properties = {}
    print("Enter texts (type 'NO' to stop):")
    # Regular expression to match sentences like "A X is a Y." or "An X is an Y."
    pattern = re.compile(r'A[n]? ([\w\s]+?) is a[n]? ([\w\s]+)\.', re.IGNORECASE)
    while True:
        text = input()
        if text.strip().upper() == 'NO':
            break
        match = pattern.match(text.strip())
        if match:
            entity = match.group(1).strip().lower()
            property = match.group(2).strip().lower()
            if entity in entity_properties:
                entity_properties[entity].add(property)
            else:
                entity_properties[entity] = set([property])
    paradoxes = []
    for entity, properties in entity_properties.items():
        if len(properties) > 1:
            paradoxes.append(f"Paradox detected: '{entity}' is both {', '.join(properties)}.")
    if paradoxes:
        print("\nParadoxes found:")
        for paradox in paradoxes:
            print(paradox)
    else:
        print("\nNo paradoxes detected.")

if __name__ == "__main__":
    main()
