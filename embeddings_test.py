from foundry_local_sdk import Configuration, FoundryLocalManager

def main():
    print("Foundry Local başlatılıyor...")
    config = Configuration(app_name="LocalRAGAssistant")
    FoundryLocalManager.initialize(config)
    manager = FoundryLocalManager.instance
    
    # Katalog listeleme kısmını sildik, direkt hedef modele gidiyoruz.
    model_name = "qwen3-embedding-0.6b" 
    
    try:
        model = manager.catalog.get_model(model_name)
    except Exception as e:
        print(f"HATA: '{model_name}' alınırken bir sorun oluştu. Detay: {e}")
        return
        
    if model is None:
        print(f"HATA: '{model_name}' bulunamadı. Lütfen model adını kontrol et.")
        return
        
    print(f"'{model_name}' embedding modeli yükleniyor...")
    model.download()
    model.load()
    
    # Vektöre çevrilecek cümlemiz
    text = "Marmara Üniversitesi Siber Güvenlik Kulübü etkinlikleri çok faydalıdır."
    print(f"\nOrijinal Metin: '{text}'")
    
    # Vektör (Embeddings) istemcisi alıyoruz
    client = model.get_embedding_client()
    response = client.generate_embeddings(inputs=[text])
    
    # Gelen ilk sonucun vektör dizisini alıyoruz
    vector = response.data[0].embedding
    
    print(f"\nVektör Uzunluğu: {len(vector)} boyutlu (Her bir kelime/anlam için bir koordinat)")
    print(f"Vektörün İlk 5 Değeri: {vector[:5]}")
    print("\nİşte yapay zeka bu cümleyi arka planda böyle görüyor!")

if __name__ == "__main__":
    main()