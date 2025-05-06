print("hola")

#dictionary with 5 data for a student
student = {
    "name": "Luis",
    "age": 20,
    "gender": "male",
    "height": 1.80,
    "weight": 800
}

print(student)

print(student["name"])

for key in student:
    print(key, " es el key y ", student[key], " es el value")

    