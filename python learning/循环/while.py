#!/usr/bin/env python

# -*- coding: UTF-8 -*-

age_of_crow = 22
count = 0
while count < 3:
    guess_age = int(input("guess age:"))
    if guess_age == age_of_crow:
        print("yes,all right")
        break
    elif guess_age > age_of_crow:
        print("smaller")
    else:
        print("bigger")
    count += 1
    if count == 3:
        countine_confirm = input("do u want to keeping guessing?")
        if countine_confirm != "n":
            count = 0