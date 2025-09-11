numbers= input("Sequence of numbers: ")
num_list=[int(num) for num in numbers.split()]
min_value=min(num_list)
max_value=max(num_list)


file_name='minmax_data.txt'
with open(file_name,'w') as writer:
    writer.write(f'List: {num_list}\n')
    writer.write(f'Min: {min_value}\n')
    writer.write(f'Max: {max_value}')

with open(file_name,'r') as reader:
    names_list=reader.readline()
    print(num_list)
    print(min_value)
    print(max_value)