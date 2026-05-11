print("---if 구문---")

score = 88
if score >= 80:
    # print('성적은 A+ 입니다.')
    grade = 'A'
elif score >= 70:
    # print('성적은 B입니다.')
    grade = 'B'
elif score >= 60:
    # print('성적은 C입니다.')
    grade = 'C'
else:
    # print('성적은 F입니다.')
    grade = 'F'

print(f"이 학생의 점수는 {score}이고, 학점은 {grade} 입니다.")

month = 7
if month in [12,1,2]:
    # print('겨울입니다.')
    seasson = '겨울'
elif month in [3,4,5]:
    # print('봄')
    seasson = '봄'
elif month in [6,7,8]:
    # print('여름')
    seasson= '여름'
elif month in [9,10,11]:
    # print('가을')
    seasson= '가을'
else:
    seasson = '알수없는 계절'

print(f"{month}월은 {seasson} 입니다.")