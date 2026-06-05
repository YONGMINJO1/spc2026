import os
from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

DB_DIR = "./chroma_db"
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
llm = ChatOpenAI(model="gpt-4o-mini")

hbm_store = Chroma(
    collection_name="memory",
    embedding_function=embeddings,
    persist_directory=DB_DIR,
)

nvme_store = Chroma(
    collection_name="nvme",
    embedding_function=embeddings,
    persist_directory=DB_DIR,
)

hbm_retriever = hbm_store.as_retriever(search_kwargs={"k": 2})
nvme_retriever = nvme_store.as_retriever(search_kwargs={"k": 2})

def bulid_hbm_store():
    return "미구현"

def load_hbm_store():
    return "미구현"

def build_nvme_store():
    return '미구현'

def load_nvme_store():
    return '미구현'

def format_docs(docs):
    return "\n\n".join(d.page_content for d in docs)


prompt = ChatPromptTemplate.from_template("""

아래 문서를 참고하여 질문에 답하시오.

HBM 관련 문서:
{hbm_context}

NVMe 관련 문서:
{nvme_context}

질문:
{question}
""")

chain = (
    {
        "hbm_context": hbm_retriever | format_docs,
        "nvme_context": nvme_retriever | format_docs,
        "question": RunnablePassthrough(),
    }
    | prompt
    | llm
    | StrOutputParser()
)

question = "NVMe와 HBM의 차이점은 무엇인가요?"
print(f"질문: {question}")
print(f"답변: {chain.invoke(question)}")

print("\n ---  PDF 로더 테스트  ---")
pdf_loader = PyPDFLoader("./Javascript_Secure_Coding.pdf")
pdf_pages = pdf_loader.load()

print(f"PDF 페이지수: {len(pdf_pages)}")
for p in pdf_pages:
    if p.page_content.strip():
        print(f"첫 페이지 metadata: {p.metadata}")
        print(f"페이지 내용 (앞 200글자):\n{p.page_content[:200]}...")
        break
