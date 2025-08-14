names=["amir","mehdi","hossein","hamid"]

new=[name if name != "amir" else "jafar" for name in names]
print(new)







#
# new=[name.upper() for name in names if "a" in name]
# print(new)



# new=["hello" for x in range(10) if x<5]
# print(new)




#
# newlist=[name for name in names if "a" in name]
#
# print(newlist)

# numbers=[1,2,3,4,5,6,7,8,9]
#
# new=[number * 2 for number in numbers]
#
# print(new)