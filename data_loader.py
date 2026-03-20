import os
import google.generativeai as genai
from llama_index.readers.file import PDFReader
from llama_index.core.node_parser import SentenceSplitter
from dotenv import load_dotenv


load_dotenv()





api_key = os.environ.get("GEMINI_API_KEY")
    

    # 3. Configure the Gemini API
genai.configure(api_key=api_key)
print("✅ Gemini API successfully configured!")

    # 4. Initialize the model
    # gemini-1.5-pro is great for complex tasks and large context windows
model = genai.GenerativeModel("gemini-2.5-pro")

EMBEDDING_MODEL = "gemini-embedding-001"    
EMBEDDING_DIM = 3072

splitter = SentenceSplitter(chunk_size=1000, chunk_overlap=200)


def load_and_chunk_pdf(path: str):
    docs = PDFReader().load_data(file=path)
    texts = [d.text for d in docs if getattr(d,"text",None)]
    chunks = []
    for t in texts:
        chunks.extend(splitter.split_text(t))
    return chunks
    
  