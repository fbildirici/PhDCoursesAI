# Gerekli kütüphaneleri içe aktarıyoruz
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# The Big Bang Theory temalı bilimsel sayılar
big_bang_theory_numbers = [
    13.8,  # Evrenin yaşı (milyar yıl)
    2.725,  # Kozmik mikrodalga arka plan ısısı (Kelvin)
    6.626e-34,  # Planck sabiti (Joule*second)
    299792458,  # Işık hızı (m/s)
    9.81,  # Yerçekimi ivmesi (m/s^2)
    1.602e-19,  # Elektron yükü (Coulomb)
    1.380649e-23,  # Boltzmann sabiti (Joule/Kelvin)
    6.02214076e23,  # Avogadro sayısı (1/mol)
    3.1415926535,  # Pi sayısı
    2.99792458e8,  # Işık hızı (m/s)
    1.6726219e-27,  # Proton kütlesi (kg)
    9.10938356e-31,  # Elektron kütlesi (kg)
    8.314462618,  # Gaz sabiti (Joule/(mol*K))
    5.670374419e-8,  # Stefan-Boltzmann sabiti (W/(m^2*K^4))
    6.67430e-11,  # Evrensel çekim sabiti (m^3/(kg*s^2))
    1.25663706212e-6,  # Manyetik alan sabiti (N/A^2)
    8.9875517923e9,  # Coulomb sabiti (N*m^2/C^2)
    273.15,  # Suyun donma noktası (Kelvin)
    5.9722e24,  # Dünya'nın kütlesi (kg)
    1.989e30  # Güneş'in kütlesi (kg)
]

# Diziyi numpy array'e çeviriyoruz
data = np.array(big_bang_theory_numbers)

# Logaritmik ölçekte histogram oluşturma
plt.figure(figsize=(12, 6))

# Bin sayısını belirleyin
num_bins = 20  # İhtiyacınıza göre bu sayıyı değiştirebilirsiniz

# Veri aralığının logaritmasını hesaplayın
log_min = np.log10(data.min())
log_max = np.log10(data.max())

# Logaritmik olarak eşit aralıklı binler oluşturun
bins = np.logspace(log_min, log_max, num_bins)

# Histogramı çizdirin
plt.hist(data, bins=bins, edgecolor='black')
plt.title('Bilimsel Sayıların Dağılımı')
plt.xlabel('Değerler (logaritmik ölçek)')
plt.ylabel('Frekans')
plt.xscale('log')  # x eksenini logaritmik ölçeğe ayarla
plt.grid(True, which="both", ls="-", alpha=0.2)
plt.show()

# Temel istatistikler
print("Temel İstatistikler:")
print(f"Ortalama: {np.mean(data):.2e}")
print(f"Medyan: {np.median(data):.2e}")
print(f"Standart Sapma: {np.std(data):.2e}")

# Dağılım analizi için verileri logaritmik olarak dönüştürelim
log_data = np.log(data)

# Dağılım analizi
distributions = [
    ('Normal', stats.norm),
    ('Log-normal', stats.lognorm),
    ('Exponential', stats.expon),
    ('Gamma', stats.gamma)
]

results = []

for name, distribution in distributions:
    # Dağılım parametrelerini tahmin et
    if name == 'Log-normal':
        # Log-normal dağılımı için özel işlem
        shape, loc, scale = distribution.fit(data, floc=0)
        params = (shape, loc, scale)
        # K-S testi için CDF fonksiyonunu tanımla
        cdf = lambda x: distribution.cdf(x, *params)
    else:
        # Diğer dağılımlar için
        params = distribution.fit(log_data)
        # K-S testi için CDF fonksiyonunu tanımla
        cdf = lambda x: distribution.cdf(np.log(x), *params)

    # Kolmogorov-Smirnov testi uygula
    D, p_value = stats.kstest(data, cdf)

    # Benzerlik oranını hesapla (1 - D istatistiği)
    similarity = 1 - D

    results.append((name, similarity, p_value))

# Sonuçları benzerlik oranına göre sırala
results.sort(key=lambda x: x[1], reverse=True)

print("\nDağılım Analizi Sonuçları:")
for name, similarity, p_value in results:
    print(f"{name} Dağılımı:")
    print(f"  Benzerlik Oranı: {similarity:.2%}")
    print(f"  p-değeri: {p_value:.4e}")
    if p_value > 0.05:
        print("  Veriler bu dağılıma uyuyor olabilir.")
    else:
        print("  Veriler bu dağılıma uymama eğiliminde.")
    print()
