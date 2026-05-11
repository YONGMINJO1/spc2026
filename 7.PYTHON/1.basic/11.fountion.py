def add_numbers(a,b):
    """   두 수의 합을 반환하는 함수입니다."""
    result = a+b
    return result

sum = add_numbers(3,4)
print(f"두 수의 합은 {sum} 입니다.")

def add_numbers2(a,b):
    return a,b, a+b

input1, input2, sum = add_numbers2(3,4)
print(f"인자1는 {input1}, 인자2는 {input2}, 두수의 합은 {sum} 입니다.")

print("-" *30)

def create_profile(name,age,city="서울",job="학생"):
    profile = f"이름: {name}, 나이: {age}, 지역: {city}, 직업: {job}"
    return profile

print(create_profile('홍길동',23))
print(create_profile('김길동',25 ))
print(create_profile('박길동',30))