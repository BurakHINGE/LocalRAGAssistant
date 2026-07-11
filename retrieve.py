import sqlite3
import json
import math
from foundry_local_sdk import Configuration, FoundryLocalManager

# İki vektör arasındaki Kosinüs Benzerliğini (Cosine Similarity) hesaplayan matematik fonksiyonu
def cosine_similarity(vec1, vec2):
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    magnitude1 = math.sqrt(sum(a * a for a in vec1))
    magnitude2 = math.sqrt(sum(b * b for b in vec2))
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    return dot_product / (magnitude1 * magnitude2)

def get_top_chunks(query, top_k=2):
    print(f"\n🔍 Soru: '{query}'")
    print("Soru vektöre çevriliyor ve veritabanında taranıyor...")
    
    # 1. Foundry Local ve Embedding modelini hazırla
    config = Configuration(app_name="LocalRAGAssistant")
    FoundryLocalManager.initialize(config)
    manager = FoundryLocalManager.instance
    
    model = manager.catalog.get_model("qwen3-embedding-0.6b")
    model.load()
    client = model.get_embedding_client()
    
    # 2. Kullanıcının sorusunu vektöre çevir
    response = client.generate_embeddings(inputs=[query])
    query_vector = response.data[0].embedding
    
    # 3. Veritabanına bağlan ve tüm kayıtları çek
    conn = sqlite3.connect('knowledge_base.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, content, embedding FROM documents')
    rows = cursor.fetchall()
    
    results = []
    
    # 4. Sorunun vektörü ile veritabanındaki her bir kaydın vektörünü karşılaştır
    for row in rows:
        doc_id = row[0]
        content = row[1]
        # Veritabanındaki JSON formatındaki vektörü tekrar Python listesine çevir
        doc_vector = json.loads(row[2])
        
        # Benzerlik skorunu hesapla (0 ile 1 arasında bir değer çıkar, 1'e ne kadar yakınsa o kadar alakalıdır)
        score = cosine_similarity(query_vector, doc_vector)
        results.append((score, content))
    
    conn.close()
    
    # 5. Sonuçları skora göre büyükten küçüğe sırala ve en iyi 'top_k' kadarını al
    results.sort(key=lambda x: x[0], reverse=True)
    top_results = results[:top_k]
    
    print("\n✅ En Alakalı Parçalar Bulundu:")
    for i, (score, text) in enumerate(top_results, 1):
        print(f"\n--- Sonuç {i} (Benzerlik Skoru: {score:.4f}) ---")
        print(text)
        
    return top_results

def main():
    # Sistemimizi test edelim! Dokümanda cevabı olan bir soru soruyoruz:
    test_query = "Kulübün eğitimleri hangi günler yapılıyor?"
    get_top_chunks(test_query)

if __name__ == "__main__":
    main()