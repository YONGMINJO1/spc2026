from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter

loader = TextLoader("./hbm.txt", encoding="utf-8")
documents = loader.load()

contents = documents[0].page_content
print(f"원본 글자수: {len(contents)}")

# 일반적으로, 1000:200 / 1500:300 / 2000: 500 정도 내외로, 실제 짤린 내용을 보고 판단함.
char_splitter = CharacterTextSplitter(
    separator="\n\n", # 이것을 목표로 하는데, 이게 안될 수 있으니.
    chunk_size=500,     # 위에 조작이 작으면, 최대 500개가 될때까지 합침
    chunk_overlap=100, # 문장 중간에 짤리면 의미가 사라지니 겹치게 짜름
)

chunk_char = char_splitter.split_documents(documents)
print(f"[CharSplitter] {len(chunk_char)}")
print(f"첫 청크 글자수: {len(chunk_char[0].page_content)}")


###########################################################################3

recur_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap=100
)

chunk_recur = recur_splitter.split_documents(documents)
print(f"[CharSplitter] {len(chunk_recur)}")
print(f"첫 청크 글자수: {len(chunk_recur[0].page_content)}")
