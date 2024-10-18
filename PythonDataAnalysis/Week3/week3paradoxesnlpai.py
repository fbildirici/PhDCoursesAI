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


# Bir kelimenin farklı anlamlara sahip olup olmadığını kontrol eden fonksiyon
def check_word_meanings(word):
    synsets = wn.synsets(word)
    if len(synsets) > 1:
        return True
    return False


# Paradoxları tespit eden fonksiyon
def find_paradoxes(sentences):
    paradoxes = []
    word_meanings = {}

    # Cümleleri analiz et
    for sentence in sentences:
        doc = nlp(sentence)
        for token in doc:
            word = token.text.lower()

            # Stopwords ve sadece isimleri dikkate al
            if token.pos_ == "NOUN" and word not in stop_words:
                # Kelimenin anlamlarını kontrol et
                if check_word_meanings(word):
                    if word in word_meanings:
                        # Daha önce farklı bir cümlede kullanıldıysa semantik paradoks olabilir
                        paradoxes.append(("Semantik Paradoks", word, word_meanings[word], sentence))
                    else:
                        word_meanings[word] = sentence

    # Mantıksal paradoksları tespit etmek için cümleleri incele
    for i in range(len(sentences) - 1):
        sentence1 = sentences[i].strip().lower()
        sentence2 = sentences[i + 1].strip().lower()

        # Basit mantıksal paradoks örneği: bir cümlenin diğerini yalanlaması
        if ("true" in sentence1 and "false" in sentence2) or ("false" in sentence1 and "true" in sentence2):
            paradoxes.append(("Mantıksal Paradoks", sentence1, sentence2))

    return paradoxes


# Sonsuz döngüde kullanıcıdan cümleleri alma
def main():
    all_sentences = []
    while True:
        # Kullanıcıdan cümle al
        user_input = input("Lütfen bir cümle girin (veya 'HAYIR' yazarak çıkabilirsiniz): ").strip()

        # Kullanıcı 'HAYIR' yazarsa çık
        if user_input.lower() == 'hayır':
            print("Çıkış yapılıyor...")
            break

        # Kullanıcı devam etmek istiyorsa cümleyi analiz et
        if user_input:
            all_sentences.append(user_input)

            # Paradoxları bul
            paradoxes = find_paradoxes(all_sentences)

            # Sonuçları göster
            if paradoxes:
                print("\nParadoxlar bulundu:")
                for paradox in paradoxes:
                    paradox_type = paradox[0]
                    if paradox_type == "Semantik Paradoks":
                        word, first_sentence, second_sentence = paradox[1:]
                        print(f"{paradox_type}:")
                        print(f"Kelime: {word}")
                        print(f"İlk cümle: {first_sentence}")
                        print(f"İkinci cümle: {second_sentence}")
                        print(
                            f"Açıklama: '{word}' kelimesi farklı anlamlarda kullanıldığı için bu bir semantik paradokstur.")
                        print("---")
                    elif paradox_type == "Mantıksal Paradoks":
                        first_sentence, second_sentence = paradox[1:]
                        print(f"{paradox_type}:")
                        print(f"İlk cümle: {first_sentence}")
                        print(f"İkinci cümle: {second_sentence}")
                        print("Açıklama: Bu iki cümle birbiriyle çelişiyor, dolayısıyla bu bir mantıksal paradokstur.")
                        print("---")
            else:
                print("Paradox bulunamadı.\n")


# Programı çalıştır
if __name__ == "__main__":
    main()
