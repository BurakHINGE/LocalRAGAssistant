from foundry_local_sdk import Configuration, FoundryLocalManager

def main():
    print("Foundry Local başlatılıyor...")
    
    config = Configuration(app_name="LocalRAGAssistant")
    FoundryLocalManager.initialize(config)
    manager = FoundryLocalManager.instance
    
    prompt = "Hello, world!"
    print(f"Girdi (Prompt): {prompt}")
    
    model_name = "phi-3.5-mini"
    model = manager.catalog.get_model(model_name)
    
    if model is None:
        print(f"HATA: '{model_name}' kataloğda bulunamadı. Lütfen ismi kontrol edin.")
        return
        
    print(f"{model_name} indiriliyor ve belleğe yükleniyor (İlk seferde biraz sürebilir)...")
    model.download()
    model.load()
    
    # İŞTE BURAYI DÜZELTTİK: create yerine get kullandık
    client = model.get_chat_client()
    
    messages = [{"role": "user", "content": prompt}]
    
    print("Model cevap üretiyor...")
    response = client.complete_chat(messages)
    
    print("\n--- Model Çıktısı ---")
    if hasattr(response, 'choices') and len(response.choices) > 0:
        print(response.choices[0].message.content)
    else:
        print(response)

if __name__ == "__main__":
    main()