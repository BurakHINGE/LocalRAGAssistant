# 🚀 Local RAG AI Assistant
*(Scroll down for the Turkish version / Türkçe versiyon için aşağı kaydırın)*

**Completely Offline, Privacy-First, Zero-Hallucination Q&A Agent**

This project is a completely offline Retrieval-Augmented Generation (RAG) assistant that runs locally on your device without any internet connection. Built with Microsoft Foundry Local, it allows you to query your local documents (PDFs, text files, notes) securely using your device's CPU/NPU resources.

## ✨ Key Features
* 🔒 **100% Offline & Secure:** No data is sent to cloud servers or third-party APIs. All inference happens locally.
* 🧠 **Zero Hallucination:** Thanks to the RAG architecture and a strict System Prompt, the model does not fabricate answers. If the information is not in the database, it clearly states: "I do not have this information."
* ⚡ **High Performance:** Optimized inference times averaging **~0.5 - 1.5 seconds** per query.
* 🗄️ **Lightweight Database:** Uses embedded `SQLite` for vector (Embedding) storage and Cosine Similarity calculations without needing an external vector database server.
* 🛡️ **Error Handling:** Robust CLI interface protected against empty or nonsensical user inputs.

## 🏗️ Architecture & Tech Stack
The pipeline consists of three main stages:
1. **Data Ingestion:** Documents are chunked, converted to embeddings using `qwen3-embedding-0.6b`, and stored in SQLite via `ingest.py`.
2. **Retrieval:** User queries are vectorized and compared against stored vectors using Cosine Similarity to fetch the most relevant context.
3. **Generation:** The retrieved context is fed into the `phi-3.5-mini` Small Language Model (SLM) to generate a grounded response.

* **Language:** Python 3.11+
* **Models:** `qwen3-embedding-0.6b` (Embedding), `phi-3.5-mini` (Chat)
* **Libraries:** `foundry-local-sdk`, `sqlite3`, `time`

---

## ⚙️ Setup & Run

### 1. Clone the repo and create a virtual environment
``
git clone https://github.com/YOUR_USERNAME/LocalRagAssistant.git
cd LocalRagAssistant
python3 -m venv venv
source venv/bin/activate  # For macOS/Linux
For Windows: venv\Scripts\activate
``

### 2. Install dependencies
``
pip install -r requirements.txt
``

### 3. Build the Database (Ingestion)
Place your documents (e.g., .txt) inside the docs/ folder and run the ingestion script:
``
python3 ingest.py
``

### 4. Start the Assistant
Run the main app to start chatting via CLI:
``
python3 app.py
``

---

## ⏱️ Performance Metrics (Apple Silicon)
•	Direct information retrieval: **~0.74 seconds**
•	Logical deduction queries: **~1.09 seconds**
•	Out-of-context edge cases (Refusals): **~0.38 seconds**

---

# 🚀 Local RAG AI Assistant (Türkçe)

---

Tamamen Çevrimdışı, Gizlilik Odaklı, Sıfır Halüsinasyon Q&A Asistanı

Bu proje, yerel belgeleriniz (notlar, metin dosyaları) üzerinde çalışan, internet bağlantısı gerektirmeyen ve cihazınızın kaynaklarını (CPU/NPU) kullanarak çalışan bir RAG (Retrieval-Augmented Generation) asistanıdır. Microsoft Foundry Local altyapısı kullanılarak geliştirilmiştir.

## ✨ Temel Özellikler
•	🔒 **%100 Çevrimdışı ve Güvenli:** Hiçbir veri bulut sunucularına veya üçüncü parti API'lere gönderilmez.
•	🧠 **Sıfır Halüsinasyon (Zero-Hallucination):** RAG mimarisi ve katı Sistem Komutu (System Prompt) sayesinde model uydurma yapmaz. Bilgi veritabanında yoksa net bir şekilde cevap veremediğini belirtir.
•	⚡ **Ultra Yüksek Performans:** Optimizasyonlar sayesinde ortalama yanıt süresi ~0.5 - 1.5 saniye arasındadır.
•	🗄️ **Hafif Veritabanı Mimarisi:** Vektör (Embedding) depolama ve arama işlemleri için harici bir sunucuya ihtiyaç duymayan gömülü SQLite kullanır.
•	🛡️ **Hata Yönetimi (Error Handling):** Boş veya anlamsız kullanıcı girdilerine karşı korumalı CLI arayüzü.

---

## 🏗️ Mimari ve Kullanılan Teknolojiler
Proje üç temel yapıtaşından oluşmaktadır:
	1.	**Data Ingestion (Veri Besleme):** ingest.py aracılığıyla belgeler parçalara ayrılır, qwen3-embedding-0.6b ile vektörlere dönüştürülür ve SQLite'a kaydedilir.
	2.	**Retrieval (Arama):** Kullanıcı sorusu vektöre dönüştürülür ve SQLite veritabanındaki kayıtlarla Kosinüs Benzerliği kullanılarak en alakalı bağlam (context) anında çekilir.
	3.	**Generation (Üretim):** Elde edilen bağlam, küçük ve hızlı bir dil modeli olan phi-3.5-mini modeline aktarılır ve yerel donanım ivmesiyle cevap üretilir.

---

## ⚙️ Kurulum ve Çalıştırma

### 1. Depoyu Klonlayın ve Sanal Ortam Oluşturun
``
git clone https://github.com/KULLANICI_ADINIZ/LocalRagAssistant.git
cd LocalRagAssistant
python3 -m venv venv
source venv/bin/activate  # macOS/Linux için
Windows için: venv\Scripts\activate
``

### 2. Gerekli Kütüphaneleri Yükleyin
``
pip install -r requirements.txt
``

### 3. Veritabanını Hazırlayın (Ingestion)
``
python3 ingest.py
``

### 4. Asistanı Başlatın
``
python3 app.py
``

---

Mehmet Burak Menteşe Marmara Üniversitesi - Bilgisayar Mühendisliği (İngilizce) Bu proje, Microsoft AI Innovators Summer Program kapsamında geliştirilmiş bitirme projesidir.

