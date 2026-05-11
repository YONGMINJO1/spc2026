my_list = [1,2,3,4,5]

print(my_list)
print(len(my_list))

print(my_list[0]) # 모든 언어의 첫번째 멤버는 0번임
print(my_list[4]) # 4번이 다섯번째 멤버
# print(my_list[5]) # 5번이 다섯번째 멤버 코드 죽음

print(my_list[-1]) # 리스트 거꾸로 
print(my_list[-2]) # 뒤에서 두번째

print(my_list[1:3]) # 슬라이싱 [1]을 포함하고 [3]포함 안함
print(my_list[3:5])
print(my_list[:2])
print(my_list[2:])

# 원본 리스트에 멤버 추가하기
my_list.append(6)
print(my_list)

# 특정 위치 멤버 추가하기
my_list.insert(2, 99)

#  해당 값의 요소 삭제하기
my_list.remove(99)
print(my_list)

#특정 인텍스의 요소 삭제하기
my_list.pop(3)
print(my_list)

my_list.pop() # 아무것도 넣지 않으면 맨 뒤
print(my_list)

my_list.clear() # 리스트 전체 삭제
print(my_list)

my_list = [4,1,6,3,5,7,2,8,9]
print(my_list)

my_list.sort() # 정렬을 하는데 , 원본값을 변경하는 함수
print(my_list)

new_list = sorted(my_list) # 원본을 유지하고 복사본을 생성
print(my_list)
print(new_list)

# 리스트 컴프리헨션 ( 어려운데 사용하면 편함)
print('-' * 30)
numbers = [x for x in range(1,10)]
print(numbers)

numbers = [x for x in range(5)]
print(numbers)

numbers = [x**2 for x in range(5)] # 이전값을 제곱
print(numbers)

numbers = [x for x in range(1,10) if x % 2 == 0] # 짝수
print(numbers)

numbers = [x for x in range(1,10) if x % 2 == 1] # 홀수
print(numbers)

list1 = [1,2,3]
list2 = [4,5,6]

list12 = list1 + list2
print(list12)
print(list1 *3)