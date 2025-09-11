sentence=input("Sentence: ")
sentence_list=sentence.split()
sentence_tuple=tuple(word.upper() for word in sentence_list)

print(sentence)
print(sentence_list)
print(sentence_tuple)

file_name='sentence_data.txt'
with open(file_name,'w') as writer:
    writer.write(f'List: {sentence_list}\n')
    writer.write(f'Tuple: {sentence_tuple}')

with open(file_name,'r') as reader:
    line_list=reader.readline()
    line_tuple=reader.readline()
    print(line_list)
    print(line_tuple)

