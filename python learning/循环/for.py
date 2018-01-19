for i in range(3):
    print('loop',i)
for i in range(0,6,2):
    print("loop",i)


age_of_crow = 22
count= 0

for i in range(3):
    guess_age = int(input("guess age:"))
    if guess_age == age_of_crow:
        print("yes,all right")
        break
    elif guess_age > age_of_crow:
        print("smaller")
    else:
        print("bigger")
else:
    print("you have tried too many times")