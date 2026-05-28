from dotenv import load_dotenv

from langchain_core.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    FewShotPromptTemplate
)

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

examples = [
    {"sentence": " 오늘 정말 최고의 하루였어! " , "result": "감정: 긍정 / 점수 : 9"},
    {"sentence": " 여기 진짜 별로네요, 시간 낭비였습니다. " , "result": "감정: 부정 / 점수 : 2"},
    {"sentence": " 그냥 평범했습니다. 특별히 좋지도 나쁘지도 않았네요. " , "result": "감정: 중립 / 점수 : 5"},
    {"sentence": " 와 진짜 감동이에요. 눈물이 날 정도였어요! " , "result": "감정: 긍정 / 점수 : 9"},
    {"sentence": " 기대했던 것보다는 별로였지만, 그래도 쓸만했어요 " , "result": "감정: 중립 / 점수 : 6"},
]

example_prompt = PromptTemplate(
    input_variables=["sentence", "result"],
    template="문장: {sentence}\n 분석: {result}"
)

fewshot_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt = example_prompt,
    prefix="다음은 문장의 감정을 분석한 예시입니다.. \n 같은 형식으로 다음 문장을 분석하세요. \n\n =====예시 시작 ======",
    input_variables=['sentence'],
    example_separator="\n------\n"
)

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 한국어 감정 분석가 입니다. 예시와 같은 형태로 답변하세요"),
    ("user", "{fewshot_text}")
])

llm = ChatOpenAI(model="gpt-4o-mini")
chain = chat_prompt | llm | StrOutputParser()

# 최종 분석할 문장
target = "오랜만에 만난 친구랑 좋은 시간을 보냈어요. 다음에도 또 보고싶네요."
fewshot_text = fewshot_prompt.format(sentence=target)

# print(fewshot_text)
result = chain.invoke({"fewshot_text" : fewshot_text})
print("문장: ", target)
print("결과: ", result)

#######################################################

# 만약 우리가 퓨삿을 안했다면? 그냥 했다면...
plain_chain = (
    ChatPromptTemplate.from_messages([
        ("system","당신은 한국어 감정 분석가 입니다."),
        ("user","다음 문장의 감정을 분석하세요: {sentence}"),
    ])
    | llm
    | StrOutputParser()
)

print(plain_chain.invoke({"sentence" : target }))