# 나만의 데이터로 모델 추가 학습하기 (fine-tuning)
# pip install transformers torch datasets

import numpy as np
from transformers import (
    AutoModelForZeroShotImageClassification, AutoTokenizer,Trainer, TrainingArguments
)
from datasets import Dataset

train_data = {
    "text": [
        "이 영화 정말 재미있어요",
        "정말 최악이네요",
        "오늘 기분이 너무 좋아요",
        "너무 실망스러워요",
        "이 제품은 정말 훌륭합니다",
        "다시는 이용하지 않을 거예요",
        "완전 만족합니다",
        "정말 싫어요"
    ],
    "label": [1, 0, 1, 0, 1, 0, 1, 0]
}

eval_data = {
    "text": [
        "오늘 하루가 행복해요",
        "서비스가 형편없네요",
        "기대 이상으로 좋았습니다",
        "생각했던 것보다 별로예요"
    ],
    "label": [1, 0, 1, 0]
}


model_name = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)

def tokenize(batch):
    return tokenizer(batch['text'],padding="max_length",truncation=True)

train_ds = Dataset.from_dict(train_data).map(tokenize, batched=True)
eval_ds = Dataset.from_dict(eval_data).map(tokenize, batched=True)
