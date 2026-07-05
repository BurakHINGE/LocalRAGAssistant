import sqlite3
import json
from foundry_local_sdk import Configuration, FoundryLocalManager

def setup_database():
    # Reponun içine 'knowledge_base.db' adında bir dosya oluşturur
    conn = sqlite3.connect('knowledge_base.db')
    cursor = conn.cursor()
    
    # Dokümanları ve vektörleri tutacağımız tabloyu oluşturuyoruz
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            embedding TEXT NOT NULL
        )
    ''')
    conn.commit()
    return conn

def main():
    print("Foundry Local başlatılıyor...")
    config = Configuration(app_name="LocalRAGAssistant")
    FoundryLocalManager.initialize(config)
    manager = FoundryLocalManager.instance
    
    model_name = "qwen3-embedding-0.6b"
    model = manager.catalog.get_model(model_name)
    
    print(f"'{model_name}' yükleniyor...")
    model.download()
    model.load()
    
    # Veritabanına kaydedeceğimiz metin
    text = "Marmara Üniversitesi Siber Güvenlik Kulübü etkinlikleri çok faydalıdır."
    
    # Vektörü oluştur (Senin terminalinde çalışan doğru metot isimleriyle)
    client = model.get_embedding_client()
    response = client.generate_embeddings(inputs=[text])
    vector = response.data[0].embedding
    
    print("Veritabanı hazırlanıyor...")
    conn = setup_database()
    cursor = conn.cursor()
    
    # 1024 boyutlu diziyi (list) SQLite'a kaydedebilmek için JSON string'ine çeviriyoruz
    vector_json = json.dumps(vector)
    
    # Veriyi tabloya ekle
    cursor.execute('INSERT INTO documents (content, embedding) VALUES (?, ?)', (text, vector_json))
    conn.commit()
    
    print("\n✅ Metin ve vektörü başarıyla 'knowledge_base.db' dosyasına kaydedildi!")
    
    # Kaydettiğimiz veriyi okuyup teyit edelim
    cursor.execute('SELECT id, content FROM documents')
    rows = cursor.fetchall()
    print("\nŞu an veritabanında bulunan kayıtlar:")
    for row in rows:
        print(f"ID: {row[0]} | Metin: {row[1]}")
        
    conn.close()

if __name__ == "__main__":
    main()