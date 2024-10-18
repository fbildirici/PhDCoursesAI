import nltk
import spacy
from sentence_transformers import SentenceTransformer, util
from nltk.corpus import wordnet

# NLTK ve spaCy'nin gerekli bileşenlerini yükleme
nltk.download('punkt')
nltk.download('wordnet')
nlp = spacy.load('en_core_web_sm')

# Sentence Transformer modelini yükleme
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')


def split_into_sentences(text):
    return nltk.sent_tokenize(text)


def calculate_similarity(sent1, sent2):
    embeddings = model.encode([sent1, sent2])
    return util.pytorch_cos_sim(embeddings[0], embeddings[1]).item()


def check_contradiction(sent1, sent2):
    doc1 = nlp(sent1)
    doc2 = nlp(sent2)

    # Özneleri ve nesneleri karşılaştırma
    subjects1 = [token for token in doc1 if token.dep_ == "nsubj"]
    subjects2 = [token for token in doc2 if token.dep_ == "nsubj"]

    if subjects1 and subjects2 and subjects1[0].text.lower() == subjects2[0].text.lower():
        # Yüklemleri karşılaştırma
        verbs1 = [token for token in doc1 if token.pos_ == "VERB"]
        verbs2 = [token for token in doc2 if token.pos_ == "VERB"]

        if verbs1 and verbs2:
            # WordNet kullanarak yüklemlerin anlamlarını kontrol etme
            synsets1 = wordnet.synsets(verbs1[0].lemma_)
            synsets2 = wordnet.synsets(verbs2[0].lemma_)

            if synsets1 and synsets2:
                # Eğer yüklemler zıt anlamlıysa veya çok farklı anlamlara sahipse
                if synsets1[0].wup_similarity(synsets2[0]) < 0.5:
                    return True

    return False


def find_paradoxes(text):
    sentences = split_into_sentences(text)
    paradoxes = []

    for i in range(len(sentences)):
        for j in range(i + 1, len(sentences)):
            similarity = calculate_similarity(sentences[i], sentences[j])
            if similarity > 0.7:  # Benzerlik eşiği
                if check_contradiction(sentences[i], sentences[j]):
                    paradoxes.append((sentences[i], sentences[j]))

    return paradoxes


# Örnek kullanım
text = """
A jaguar is an animal. A Jaguar is a car.
The Earth is flat. The Earth is a sphere.
"""

paradoxes = find_paradoxes(text)
for pair in paradoxes:
    print(f"Paradoks tespit edildi:\n1: {pair[0]}\n2: {pair[1]}\n")