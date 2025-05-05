# first pip install -U langchain-community


from langchain.vectorstores import FAISS
from langchain.document_loaders import TextLoader
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Step 1: Load the .txt file
loader = TextLoader("/home/vasu/bots/new.txt")  # Adjust path if needed
documents = loader.load()

# Step 2: Split into smaller chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
docs = splitter.split_documents(documents)

# Step 3: Convert text to embeddings
embedding = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# Step 4: Store in FAISS vector store
vectorstore = FAISS.from_documents(docs, embedding)

# Optional: Save the FAISS index to disk
vectorstore.save_local("faiss_index")
