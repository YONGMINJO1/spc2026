import os
from dotenv import load_dotenv

from flask import Flask, request,jsonify, render_template

# 랭체인 기본 불러오기
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# 문서 파서 기본 불러오기 (PyPDFLoader)
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

load_dotenv()
# 1. 백터스토어 셋업
DB_DIR = "./chroma.db"
DATA_DIR = "./DATA"
COLLECTION_NAME = "my_rag"

os.makedirs(DATA_DIR,exist_ok=True)
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

store = Chroma(
    collection_name=COLLECTION_NAME,
    embedding_function=embeddings,
    persist_directory=DB_DIR
)

retriever =  store.as_retriever(search_kwargs={"k":3})


# 2. 랭체인 세업한다 (LCEL)
llm = ChatOpenAI(model="gpt-4o-mini")
prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 문서 기반 QA시스템입니다. 아래 문서만 참고해서 답변하시오.\n\n"
            "문서에 적합한 내용이 없으면, '모른다' 라고 답변하시오.\n"
            "문서:\n{context}\n"),
    ("user", "{question}")
])

def format_docs(docs):
    return "\n\n".join(d.page_content for d in docs)

chain = (
    RunnablePassthrough.assign(context=lambda x: format_docs(retriever.invoke(x["question"])))
    | prompt
    | llm
    | StrOutputParser()
)

#########################################

# Flask

##########################################

app = Flask(__name__)

@app.get('/')
def index ():
    return render_template('index.html')

def add_my_pdf_file(path):
    docs = PyPDFLoader(path).load()
    for d in docs:
        d.metadata["source"] = os.path.basename(path)
    chunks = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100).split_documents(docs)
    # print(chunks)
    store.add_documents(chunks)


@app.post('/upload')
def upload():
    return jsonify({"message":"업로드 완료"})

@app.post('/ask')
def ask():
    return jsonify({"asnwer":"답변 완료"})

if __name__ =="__main__":
    app.run(debug=True)