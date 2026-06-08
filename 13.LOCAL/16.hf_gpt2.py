from transformers import pipeline
from transformers import AutoTokenizer

# GPT-2 모델
model_name = "gpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)

text_generator = pipeline("text-generation", model=model_name)

result = text_generator("Once upon a time", max_length=50, truncation=True)[0]

print(result["generated_text"])