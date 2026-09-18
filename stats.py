from collections import Counter

fisier = open('blocked_queries.log', 'r')
domenii = [linie.strip() for linie in fisier.readlines() if linie.strip()]
fisier.close()

total_cereri = len(domenii)
numarator_domenii = Counter(domenii)

companii_cheie = ['google', 'facebook', 'amazon', 'microsoft', 'criteo', 'appnexus', 'tiktok', 'doubleclick', 'analytics']
statistici_companii = {companie: 0 for companie in companii_cheie}

for domeniu in domenii:
    domeniu_mic = domeniu.lower()
    for companie in companii_cheie:
        if companie in domeniu_mic:
            statistici_companii[companie] += 1

print(f"Total: {total_cereri}\n")

print("Top 10:")
top_domenii = numarator_domenii.most_common(10)
for domeniu, numar in top_domenii:
    print(f"{domeniu}: {numar}")

print("\nCompanii:")
companii_sortate = sorted(statistici_companii.items(), key=lambda x: x[1], reverse=True)
for companie, numar in companii_sortate:
    if numar > 0:
        print(f"{companie.capitalize()}: {numar}")
