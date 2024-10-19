import spacy

# Load the English language model
nlp = spacy.load('en_core_web_sm')

def extract_subject_object_pairs(doc):
    pairs = []
    for sent in doc.sents:
        subj = None
        obj = None
        for token in sent:
            # Find nominal subject
            if token.dep_ == 'nsubj':
                subj = token.text.lower()
            # Find direct object or object complement
            if token.dep_ in ('dobj', 'attr'):
                obj = token.text.lower()
        if subj and obj:
            pairs.append((subj, obj))
    return pairs

def detect_paradoxes(entity_properties):
    paradoxes = []
    for entity, properties in entity_properties.items():
        if len(properties) > 1:
            paradox = f"Paradox detected: '{entity}' is both {', '.join(properties)}."
            paradoxes.append(paradox)
    return paradoxes

def main():
    entity_properties = {}
    print("Enter texts (type 'NO' to stop):")
    while True:
        text = input()
        if text.strip().upper() == 'NO':
            break
        doc = nlp(text)
        pairs = extract_subject_object_pairs(doc)
        for subj, obj in pairs:
            if subj in entity_properties:
                entity_properties[subj].add(obj)
            else:
                entity_properties[subj] = set([obj])
    paradoxes = detect_paradoxes(entity_properties)
    if paradoxes:
        print("\nParadoxes found:")
        for paradox in paradoxes:
            print(paradox)
    else:
        print("\nNo paradoxes detected.")

if __name__ == "__main__":
    main()
