import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch.nn.functional as F

def load_nli_model():
    """
    Load a smaller pre-trained NLI model and tokenizer from Hugging Face.
    """
    model_name = "joeddav/distilroberta-base-mnli"  # Corrected model name
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    # Move model to GPU if available
    if torch.cuda.is_available():
        model.to('cuda')
    return tokenizer, model

def predict_contradiction(model, tokenizer, premise, hypothesis):
    """
    Predict the relationship between premise and hypothesis.
    Returns True if a contradiction is detected, else False.
    """
    inputs = tokenizer.encode_plus(premise, hypothesis, return_tensors='pt', truncation=True)
    # Move inputs to GPU if available
    if torch.cuda.is_available():
        inputs = {k: v.to('cuda') for k, v in inputs.items()}
    with torch.no_grad():
        logits = model(**inputs).logits
    probabilities = F.softmax(logits, dim=1)
    # The labels are: 0 - entailment, 1 - neutral, 2 - contradiction
    contradiction_prob = probabilities[0][2].item()
    # Adjust the threshold as needed
    return contradiction_prob > 0.5  # Lowered threshold for smaller model

def main():
    print("Paradox Detector")
    print("Enter statements one by one. Type 'NO' to finish.\n")

    tokenizer, model = load_nli_model()
    statements = []
    paradoxes = []

    while True:
        user_input = input("Enter a statement (or 'NO' to finish): ").strip()
        if user_input.upper() == "NO":
            break
        if not user_input:
            print("Empty input. Please enter a valid statement.")
            continue

        # Check for contradictions with existing statements
        current_paradoxes = []
        for idx, stmt in enumerate(statements):
            contradiction = predict_contradiction(model, tokenizer, stmt, user_input)
            if contradiction:
                paradox = f"Contradiction detected between:\n  1. {stmt}\n  2. {user_input}\n"
                current_paradoxes.append(paradox)

            # Also check the reverse
            contradiction_rev = predict_contradiction(model, tokenizer, user_input, stmt)
            if contradiction_rev:
                paradox = f"Contradiction detected between:\n  1. {user_input}\n  2. {stmt}\n"
                current_paradoxes.append(paradox)

        if current_paradoxes:
            paradoxes.extend(current_paradoxes)
            print("\nParadox(es) detected:")
            for p in current_paradoxes:
                print(p)
        else:
            print("No paradox detected with the current statement.")

        statements.append(user_input)
        print()

    if paradoxes:
        print("\nSummary of Detected Paradoxes:")
        for p in paradoxes:
            print(p)
    else:
        print("\nNo paradoxes were detected in the provided statements.")

if __name__ == "__main__":
    main()
