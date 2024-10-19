def main():
    entity_properties = {}
    print("Enter texts (type 'NO' to stop):")
    while True:
        text = input()
        if text.strip().upper() == 'NO':
            break
        # Try to parse sentences of the form "A X is a Y."
        words = text.strip('.').split()
        if len(words) >= 4 and words[1].lower() == 'is' and words[2].lower() in ('a', 'an'):
            entity = words[0].lower()
            property = words[3].lower()
            # Handle cases where property might be multiple words
            if len(words) > 4:
                property += ' ' + ' '.join(words[4:]).lower()
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

