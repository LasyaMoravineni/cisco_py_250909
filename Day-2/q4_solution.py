names= input("Names list: ")
names_list=names.split()
names_list.sort()

print(names)
print(names_list)

file_name='names_data.txt'
with open(file_name,'w') as writer:
    writer.write(f'List: {names_list}\n')

with open(file_name,'r') as reader:
    names_list=reader.readline()
    print(names_list)