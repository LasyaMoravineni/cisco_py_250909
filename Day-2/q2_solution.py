numbers=input("Integers separated by spaces: ")
numbers_list=[int(num_str) for num_str in numbers.split()]
sum_value =sum(numbers_list)

avg_value = sum_value/len(numbers_list)

file_name='numbers_data.txt'
with open(file_name,'w') as writer:
    writer.write(f'List: {numbers_list}\n')
    writer.write(f'Sum: {sum_value}\n')
    writer.write(f'Average: {avg_value}')


with open(file_name,'r') as reader:
    line_list=reader.readline()
    line_sum=reader.readline()
    line_avg=reader.readline()
    print(line_list)
    print(line_sum) 
    print(line_avg)