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

# Belirli kelimelerle ilgili anlam grupları (genişletilebilir)
# "Jaguar" kelimesinin farklı anlamlarına dair bağlam kelimeleri
semantic_groups = {
    "jaguar": {
        "animal": ["wildlife", "animal", "creature", "predator", "jungle", "cat"],
        "car": ["car", "vehicle", "brand", "luxury", "drive", "engine", "model"]
    }
}


# Bir kelimenin anlamını bağlamına göre analiz eden fonksiyon
def get_contextual_meaning(word, sentence):
    word = word.lower()
    if word in semantic_groups:
        doc = nlp(sentence)
        for token in doc:
            token_text = token.text.lower()
            for meaning, related_words in semantic_groups[word].items():
                if token_text in related_words:
                    return meaning
    return None


# Semantik çelişki olup olmadığını kontrol eden fonksiyon
def check_semantic_conflict(word, meaning1, meaning2):
    return meaning1 != meaning2


# Paradoxları tespit eden ana fonksiyon
def find_paradoxes(sentences, already_checked_sentences, context_map, already_found_paradoxes):
    paradoxes = []

    # Yeni cümleleri kontrol et, daha önce kontrol edilen cümleler yeniden işlenmesin
    for sentence in sentences:
        if sentence in already_checked_sentences:
            continue  # Cümle zaten kontrol edildi, tekrar kontrol etmiyoruz

        already_checked_sentences.add(sentence)
        doc = nlp(sentence)

        # Her kelimenin bağlamına göre anlamını bul
        for token in doc:
            word = token.text.lower()

            if token.pos_ == "NOUN" and word not in stop_words:
                meaning = get_contextual_meaning(word, sentence)
                if meaning:
                    if word in context_map:
                        previous_meaning, previous_sentence = context_map[word]
                        if check_semantic_conflict(word, previous_meaning, meaning):
                            if (word, previous_sentence, sentence) not in already_found_paradoxes:
                                paradoxes.append(("Semantik Çelişki", word, previous_sentence, sentence))
                                already_found_paradoxes.add((word, previous_sentence, sentence))
                    else:
                        context_map[word] = (meaning, sentence)

    return paradoxes


# Sonsuz döngüde kullanıcıdan cümleleri alma
def main():
    all_text = ""
    already_checked_sentences = set()  # Daha önce kontrol edilen cümleler
    context_map = {}  # Her kelimenin önceki anlamı ve cümlesi
    already_found_paradoxes = set()  # Bulunan paradokslar

    while True:
        # Kullanıcıdan cümle al
        user_input = input("Lütfen bir veya birden fazla cümle girin (veya 'HAYIR' yazarak çıkabilirsiniz): ").strip()

        # Kullanıcı 'HAYIR' yazarsa çık
        if user_input.lower() == 'hayır':
            print("Çıkış yapılıyor...")
            break

        # Kullanıcı devam etmek istiyorsa cümleyi analiz et
        if user_input:
            # Metni bir bütün olarak birleştiriyoruz
            all_text += " " + user_input

            # Girilen tüm metni SpaCy ile cümlelere ayır
            doc = nlp(all_text)
            sentences = [sent.text.strip() for sent in doc.sents]

            # Paradoxları bul
            paradoxes = find_paradoxes(sentences, already_checked_sentences, context_map, already_found_paradoxes)

            # Sonuçları göster
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
                        print(
                            f"Açıklama: '{word}' kelimesi farklı bağlamlarda farklı anlamlarda kullanıldığı için bu bir semantik paradokstur.")
                        print("---")
            else:
                print("Paradox bulunamadı.\n")


# Programı çalıştır
if __name__ == "__main__":
    main()
