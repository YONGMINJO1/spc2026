
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage,HumanMessage,AIMessage

from flask import Flask,request,jsonify, send_from_directory

app=Flask(__name__)
llm = ChatOpenAI(model="gpt-4o-mini")

@app.route('/api/name')
def name():
    prompt = [
    SystemMessage(content="You are a creative branding expert"),
    HumanMessage(content="What's a good company name that makes computer games. Do not give any explanation. Just give me the names"),
    ]
    result = llm.invoke(prompt)
    return jsonify({"result":"success","chatbot": result.content})

@app.route('/api/name', methods=['POST'])
def name2():
    data = request.get_json()
    product = data.get("product")
    user_prompt = f"What's a good conpany name that makes {product}. Do not give any explanation. Just give ne the names."
    print(user_prompt)
    prompt = [
    SystemMessage(content="You are a creative branding expert"),
    HumanMessage(content=user_prompt),
    ]

    result = llm.invoke(prompt)
    names - [line.strip() for line in result.content.split('\n')]
    return jsonify({"result":"success","chatbot": result.content})

@app.route('/api/dinner')
def dinner():
    prompt = [
    SystemMessage(content='당신은 경력 10년차 호텔 쉐프입니다..'),
    HumanMessage(content='오늘 저녁 추천해줘'),
    AIMessage(content='비빔밥은 어떠신가요?'),
    HumanMessage(content='아~ 좋아. 그걸 만들기 위한 재료는?'),
    ]

    result = llm.invoke(prompt)
    #print(result.content)
    return jsonify({"result":"success","chatbot": result.content})

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

if __name__=="__main__":
    app.run(debug=True)





