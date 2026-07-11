import os
import sqlite3
import json
from foundry_local_sdk import Configuration, FoundryLocalManager

def chunk_text(text):
    # Metni çift satır boşluklarına göre böler (Her bir paragrafı ayırır)
    paragraphs = text.split('\n\n')
    # Çok kısa olan veya boş kalan parçaları filtreleyip temizleriz
    chunks = [p.strip() for p in paragraphs if len(p.strip()) > 10]
    return chunks

def main():
    print("Foundry Local ve Embedding modeli hazırlanıyor...")
    config = Configuration(app_name="LocalRAGAssistant")
    FoundryLocalManager.initialize(config)
    manager = FoundryLocalManager.instance
    
    # Metinleri vektöre çevireceğimiz modeli yüklüyoruz
    model_name = "qwen3-embedding-0.6b"
    model = manager.catalog.get_model(model_name)
    model.load()
    client = model.get_embedding_client()
    
    # SQLite veritabanımıza bağlanıyoruz
    conn = sqlite3.connect('knowledge_base.db')
    cursor = conn.cursor()
    
    docs_dir = "docs"

    print("\nDokümanlar taranıyor ve veritabanına işleniyor (Data Ingestion)...")
    
    # docs klasörü içindeki her bir dosyayı tek tek okuyan döngü
    for filename in os.listdir(docs_dir):
        if filename.endswith(".txt") or filename.endswith(".md"):
            filepath = os.path.join(docs_dir, filename)
            
            # Dosyayı okuyoruz
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Metni paragraflara (chunk) ayırıyoruz
            chunks = chunk_text(content)
            
            for chunk in chunks:
                # 1. Her bir parça için embedding (vektör) oluştur
                response = client.generate_embeddings(inputs=[chunk])
                vector = response.data[0].embedding
                vector_json = json.dumps(vector)
                
                # 2. Parçayı ve vektörünü SQLite veritabanına kaydet
                cursor.execute('INSERT INTO documents (content, embedding) VALUES (?, ?)', (chunk, vector_json))
            
            print(f"✅ '{filename}' başarıyla parçalandı ({len(chunks)} parça) ve veritabanına kaydedildi.")
    
    # İşlemleri kalıcı olarak kaydet ve bağlantıyı kapat
    conn.commit()
    conn.close()
    print("\nVeri Besleme işlemi tamamen bitti. Asistanın hafızası doldu!")

if __name__ == "__main__":
    main()