import imaplib
import os
from email.mime.text import MIMEText

from dotenv import load_dotenv

load_dotenv()

IMAP_SERVER = 'imap.naver.com'
IMAP_PORT = 993

NAVER_ID = os.getenv('NAVER_MAIL_ID')
NAVER_PASSWORD = os.getenv('NAVER_MAIL_APP_SECRET')
NAVER_EMAIL = f'{NAVER_ID}@naver.com'

mail = imaplib
mail_ids = messages[0],split()

# 메일 데이터 본문 파싱
# for response_part in msg_data:
#     if isinstance(response_part, tuple):
#         # 메일 제목 디코딩
#         subject, encoding = decode_header(msg["Subject"])[0]
#         if isinstance(subject,bytes):
#             subject = subject.decode(encoding if encoding else "utf-8")

#         print("메일 제목: " subject)
#         # 메일 데이터 디코딩

#         # 메일 본문 추출
#         if msg.is_mutipart():
#             print('멀티파트는 지금은 생략')