# 튜플 (읽기전용 리스트)
my_list = [1,2,3,4,5]
my_tuple = (1,2,3,4,5) # 읽기전용

print(my_list)
print(my_tuple)

print(my_list[2])
print(my_tuple[2])

my_list[2] = 99
# my_tuple[2] = 99 튜플 값은 사용 X

print(my_list[-1])
print(my_tuple[-1])

print(my_list[3:5])
print(my_tuple[3:5])

print(my_list[0:1])
print(my_tuple[0:1])

# 튜플을 받아왔는데 , 값을 사용하고 싶을때
my_newList = list(my_tuple)
print(my_newList)
my_newList[2] = 88
print(my_newList)
print(my_tuple)

my_newtuple = tuple(my_newList) # 쓰기가 불가능한 리스트
print(my_newList)
my_newList[2] = 77
print(my_newtuple)

print("-" *30)
a, b, c = (1,2,3)
print(a,c,b)

a_person = ("john", 23, "Student")
print(a_person)
name,age,occ = a_person
print(name)
print(age)
