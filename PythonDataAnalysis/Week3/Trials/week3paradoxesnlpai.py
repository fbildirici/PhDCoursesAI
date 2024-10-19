import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
import spacy

# Gerekli veri kümelerini indiriyoruz
nltk.download('wordnet')
nltk.download('stopwords')

# spaCy'nin İngilizce modeli
nlp = spacy.load('en_core_web_sm')

# İngilizce stopwords'leri yüklüyoruz
stop_words = set(stopwords.words('english'))

# Bilinen çelişkili kelime çiftleri ve anlamları
semantic_conflicting_words = {
    "jaguar": ["animal", "car"],
    # Daha fazla çift ekleyerek genişletebilirsiniz
}

# Zıt anlamlı kelime çiftleri
antonym_pairs = [
    ("small", "giant"),
    ("simple", "complex"),
    ("man", "mankind"),
    # Daha fazla zıt anlamlı çift eklenebilir
]

def get_word_sense(word, sentence):
    """
    Kelimenin anlamını cümledeki bağlama göre WordNet kullanarak tespit eder.
    """
    synsets = wn.synsets(word, pos=wn.NOUN)
    if not synsets:
        return None

    # Cümledeki diğer kelimeleri elde et
    doc = nlp(sentence)
    context_words = set(token.text.lower() for token in doc if token.text.lower() != word and token.text.lower() not in stop_words)

    # Her bir anlam kümesini kontrol et ve bağlama uygun olup olmadığını belirle
    for synset in synsets:
        definition_words = set(synset.definition().split())
        if context_words.intersection(definition_words):
            return synset.name()  # Anlam kümelerinin adını döndür

    return synsets[0].name()  # Uygun bir eşleşme bulunamazsa ilk anlam kümesini döndür


def check_semantic_conflict(word, sense1, sense2):
    """
    İki farklı anlam kümesinin birbirine uyumlu olup olmadığını kontrol eder.
    """
    return sense1 != sense2


def check_manual_conflict(word, sentence):
    """
    Kelimenin bilinen manuel anlam gruplarını kontrol eder.
    """
    if word in semantic_conflicting_words:
        doc = nlp(sentence)
        context_words = set(token.text.lower() for token in doc if token.text.lower() not in stop_words)

        # Anlam gruplarını kontrol et
        conflicting_meanings = semantic_conflicting_words[word]
        for meaning in conflicting_meanings:
            if meaning in context_words:
                return meaning
    return None


def check_known_logical_paradox(sentence):
    """
    Bilinen mantıksal paradoksları cümlede kontrol eder.
    """
    doc = nlp(sentence)
    tokens = set(token.text.lower() for token in doc)

    # Zıt anlamlı kelimeleri kontrol et
    for antonym1, antonym2 in antonym_pairs:
        if antonym1 in tokens and antonym2 in tokens:
            return True

    return False


def find_paradoxes(sentences, context_map, already_checked_sentences, already_found_paradoxes):
    paradoxes = []

    # Her cümleyi kontrol et
    for sentence in sentences:
        if sentence in already_checked_sentences:
            continue

        already_checked_sentences.add(sentence)

        # Mantıksal paradoksları kontrol et
        if check_known_logical_paradox(sentence):
            if sentence not in already_found_paradoxes:
                paradoxes.append(("Mantıksal Çelişki", sentence))
                already_found_paradoxes.add(sentence)

        # Her isim (noun) kelimesi için bağlamını kontrol et
        doc = nlp(sentence)
        for token in doc:
            word = token.text.lower()

            if token.pos_ == "NOUN" and word not in stop_words:
                manual_conflict = check_manual_conflict(word, sentence)
                if manual_conflict:
                    if word in context_map:
                        previous_conflict, previous_sentence = context_map[word]
                        if manual_conflict != previous_conflict:
                            if (word, previous_sentence, sentence) not in already_found_paradoxes:
                                paradoxes.append(("Semantik Çelişki", word, previous_sentence, sentence))
                                already_found_paradoxes.add((word, previous_sentence, sentence))
                    else:
                        context_map[word] = (manual_conflict, sentence)

    return paradoxes


def main():
    all_text = ""
    context_map = {}  # Kelimenin anlamını ve bağlamını saklar
    already_checked_sentences = set()
    already_found_paradoxes = set()

    while True:
        user_input = input("Lütfen bir veya birden fazla cümle girin (veya 'HAYIR' yazarak çıkabilirsiniz): ").strip()

        if user_input.lower() == 'hayır':
            print("Çıkış yapılıyor...")
            break

        if user_input:
            all_text += " " + user_input

            # Metni cümlelere ayır
            doc = nlp(all_text)
            sentences = [sent.text.strip() for sent in doc.sents]

            # Paradoxları bul
            paradoxes = find_paradoxes(sentences, context_map, already_checked_sentences, already_found_paradoxes)

            if paradoxes:
                print("\nParadoxlar bulundu:")
                for paradox in paradoxes:
                    paradox_type = paradox[0]
                    if paradox_type == "Semantik Çelişki":
                        word, first_context, second_context = paradox[1:]
                        print(f"{paradox_type}:")
                        print(f"Kelime: {word}")
                        print(f"İlk bağlam: {first_context}")
                        print(f"İkinci bağlam: {second_context}")
                        print(f"Açıklama: '{word}' kelimesi farklı bağlamlarda farklı anlamlarda kullanıldığı için bu bir semantik paradokstur.")
                        print("---")
                    elif paradox_type == "Mantıksal Çelişki":
                        print(f"{paradox_type}:")
                        print(f"Cümle: {paradox[1]}")
                        print("Açıklama: Bu cümle mantıksal bir çelişki içeriyor.")
                        print("---")
            else:
                print("Paradox bulunamadı.\n")


if __name__ == "__main__":
    main()
