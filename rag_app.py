import os
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI  
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnableLambda, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv 

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY not found")

# =========================
# 📺 STEP 1: GET TRANSCRIPT
# =========================

def get_transcript(video_id: str) -> str:
    try:
        api = YouTubeTranscriptApi()

        transcript = api.fetch(video_id, languages=["en"])

        text = " ".join(chunk.text for chunk in transcript)
        return text

    except TranscriptsDisabled:
        raise Exception("No captions available.")

# =========================
# ✂️ STEP 2: SPLIT TEXT
# =========================
def split_text(text: str):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    return splitter.create_documents([text])

# =========================
# 🧠 STEP 3: VECTOR STORE (FREE)
# =========================
from langchain_community.embeddings import HuggingFaceEmbeddings

def create_vector_store(chunks):

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_store = FAISS.from_documents(chunks, embeddings)

    return vector_store

# =========================
# 🔍 STEP 4: RAG CHAIN
# =========================
def build_rag_chain(vector_store):

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.2
    )

    prompt = PromptTemplate(
        template="""
You are a helpful assistant.
Answer ONLY from the provided transcript context.
If the context is insufficient, say you don't know.

Context:
{context}
 
Question:
{question}
""",
        input_variables=["context", "question"]
    )

    # Format retrieved docs
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    parallel_chain = RunnableParallel({
        "context": retriever | RunnableLambda(format_docs),
        "question": RunnablePassthrough()
    })

    parser = StrOutputParser()

    rag_chain = parallel_chain | prompt | llm | parser

    return rag_chain

# =========================
# 🏁 MAIN EXECUTION
# =========================
if __name__ == "__main__":

    video_id = "2gKc1pIECHM"

    print("Fetching transcript...")
    transcript = get_transcript(video_id)

    print("Splitting text...")
    chunks = split_text(transcript)

    print("Creating vector store...")
    vector_store = create_vector_store(chunks)

    print("Building RAG chain...")
    rag_chain = build_rag_chain(vector_store)

        # Ask questions
    while True:
        question = input("\nAsk about the video (type 'exit' to quit): ")
        if question.lower() == "exit":
            break

        answer = rag_chain.invoke(question)
        print("\nAnswer:", answer)