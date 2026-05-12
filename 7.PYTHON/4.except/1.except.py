
try:
    result = 10 / 0 
except ZeroDivisionError :
    print("0으로 나눌 수 없습니다.")
except:
    print("알수없는 오류입니다")

print("다음 코드 진행")

try:
    number = int("hello")
except ValueError:
    print("숫자가 아닙니다.")