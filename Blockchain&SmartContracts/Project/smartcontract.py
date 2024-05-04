# Performans metrikleri ve ağırlıklarını tanımla
performance_metrics = {
    "code_quality": 0.4,
    "peer_review": 0.3,
    "bug_fixing": 0.2,
    "collaboration": 0.1
}

# Geliştirici verilerini topla
developers = {
    "DevA": {"code_quality": 85, "peer_review": 90, "bug_fixing": 75, "collaboration": 80},
    "DevB": {"code_quality": 70, "peer_review": 80, "bug_fixing": 60, "collaboration": 75}
}

# Performans skorunu hesaplama fonksiyonu
def calculate_performance_score(metrics, weights):
    score = sum(metrics[metric] * weight for metric, weight in weights.items())
    return score

# Token tahsisatını hesapla
def allocate_tokens(developers, total_tokens):
    # Toplam performans puanını hesapla
    total_score = sum(calculate_performance_score(dev, performance_metrics) for dev in developers.values())
    allocation = {}
    # Her geliştirici için token tahsis et
    for dev, metrics in developers.items():
        score = calculate_performance_score(metrics, performance_metrics)
        allocation[dev] = round((score / total_score) * total_tokens)
    return allocation

# Örnek token dağıtımı
total_tokens = 1000
token_allocation = allocate_tokens(developers, total_tokens)
print(token_allocation)
