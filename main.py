from foundry_local_sdk import Configuration, FoundryLocalManager
from retrieve import get_top_chunks

def main():
    print("Foundry Local başlatılıyor...")
    
    config = Configuration(app_name="LocalRAGAssistant")
    FoundryLocalManager.initialize(config)
    manager = FoundryLocalManager.instance
    
    # Kullanıcıdan soruyu al (Şimdilik test için sabit, ileride input() yapabilirsin)
    user_query = "Kulübün eğitimleri hangi günler yapılıyor?"
    print(f"\n👤 Kullanıcı Sorusu: {user_query}")
    
    # 1. RAG AŞAMASI: Veritabanından alakalı paragrafları getir
    print("\n[RAG] Bilgi aranıyor...")
    top_chunks = get_top_chunks(user_query, top_k=2)
    
    # Paragrafları birleştirerek bir bağlam (context) oluştur
    context = ""
    for score, text in top_chunks:
        context += text + "\n\n"
        
    # 2. PROMPT MÜHENDİSLİĞİ AŞAMASI
    system_prompt = f"""Sen Marmara Üniversitesi Siber Güvenlik Kulübü'nün (MÜSİBER) resmi yapay zeka asistanısın.
Amacın kulüp üyelerine ve öğrencilere yardımcı olmaktır.
Lütfen aşağıdaki 'BİLGİLER' kısmında sana verdiğim metinlere dayanarak kullanıcının sorusunu cevapla.
Eğer kullanıcının sorusunun cevabı aşağıdaki bilgilerde yoksa, kibarca "Bu konuda veritabanımda bir bilgi bulunmuyor" de ve asla yalan bilgi uydurma.

BİLGİLER:
{context}
"""

    model_name = "phi-3.5-mini"
    model = manager.catalog.get_model(model_name)
    
    if model is None:
        print(f"HATA: '{model_name}' kataloğda bulunamadı. Lütfen ismi kontrol edin.")
        return
        
    print(f"\n{model_name} hazırlanıyor...")
    model.download()
    model.load()
    
    client = model.get_chat_client()
    
    # Hem sistem kurallarını hem de kullanıcının sorusunu yolluyoruz
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query}
    ]
    
    print("\nModel cevap üretiyor...\n")
    response = client.complete_chat(messages)
    
    print("🤖 --- MÜSİBER ASİSTANI CEVABI --- 🤖")
    if hasattr(response, 'choices') and len(response.choices) > 0:
        print(response.choices[0].message.content.strip())
    else:
        print(response)

if __name__ == "__main__":
    main()