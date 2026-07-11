import sqlite3
import json
import math
from foundry_local_sdk import Configuration, FoundryLocalManager

def cosine_similarity(vec1, vec2):
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    magnitude1 = math.sqrt(sum(a * a for a in vec1))
    magnitude2 = math.sqrt(sum(b * b for b in vec2))
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    return dot_product / (magnitude1 * magnitude2)

def get_top_chunks(query, embed_client, top_k=2):
    # Kullanıcının sorusunu vektöre çevir
    response = embed_client.generate_embeddings(inputs=[query])
    query_vector = response.data[0].embedding
    
    # Veritabanında ara
    conn = sqlite3.connect('knowledge_base.db')
    cursor = conn.cursor()
    cursor.execute('SELECT content, embedding FROM documents')
    rows = cursor.fetchall()
    
    results = []
    for row in rows:
        content = row[0]
        doc_vector = json.loads(row[1])
        score = cosine_similarity(query_vector, doc_vector)
        results.append((score, content))
    conn.close()
    
    # En yüksek skoru alan parçaları döndür
    results.sort(key=lambda x: x[0], reverse=True)
    return [res[1] for res in results[:top_k]]

def main():
    print("Sistem ayağa kaldırılıyor (Modeller yükleniyor, bu biraz sürebilir)...")
    config = Configuration(app_name="LocalRAGAssistant")
    FoundryLocalManager.initialize(config)
    manager = FoundryLocalManager.instance
    
    # 1. Embedding modeli (Veritabanında arama yapmak için)
    embed_model = manager.catalog.get_model("qwen3-embedding-0.6b")
    embed_model.load()
    embed_client = embed_model.get_embedding_client()
    
    # 2. Chat modeli (Arama sonucunu düzgün bir cevaba çevirmek için)
    chat_model = manager.catalog.get_model("phi-3.5-mini")
    chat_model.load()
    chat_client = chat_model.get_chat_client()
    
    print("\n" + "="*50)
    print("✅ Local RAG Asistanı Hazır!")
    print("Kulüp hakkında sorular sorabilirsiniz. Çıkmak için 'q' veya 'çıkış' yazın.")
    print("="*50)
    
    # Sürekli sohbet döngüsü (CLI Arayüzü)
    while True:
        user_input = input("\nSen: ")
        if user_input.lower() in ['q', 'çıkış', 'quit', 'exit']:
            print("Asistan kapatılıyor. Görüşmek üzere!")
            break
            
        print("🤖 Asistan düşünüyor (veritabanı taranıyor)...")
        
        # Soruyu arama motoruna gönderip en alakalı parçaları buluyoruz
        top_chunks = get_top_chunks(user_input, embed_client)
        
        # Bulduğumuz parçaları birleştirip bir bağlam (context) metni oluşturuyoruz
        context_text = "\n\n".join(top_chunks)
        
        # İngilizce, katı kurallı Sistem Promptumuz
        system_prompt = f"""You are a precise AI assistant. 
Use ONLY the information provided in the 'Context' below to answer questions. 
If the answer is not contained in the context, do not guess, do not explain why, and do not hallucinate. Simply say: 'I do not have this information.'

Context: 
{context_text}
"""
        
        # Sohbet modeline sistem kurallarını ve kullanıcının sorusunu gönderiyoruz
        response = chat_client.complete_chat(messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ])
        
        print(f"\n🤖 Asistan: {response.choices[0].message.content}")

if __name__ == "__main__":
    main()