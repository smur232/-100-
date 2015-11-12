import re
from random import sample

# 00
reversed_word = 'stressed'[::-1]
print(reversed_word)

# 01
str =  u'パタトクカシーー'[::2]
print(str)

# 02
str1 = u'パトカー'
str2 = u'タクシー'

print(''.join([a + b for a, b in zip(str1, str2)]))

# 03

str3 = "Now I need a drink, alcoholic of course, after the heavy lectures involving quantum mechanics."
str3.replace(',', '')
str3.replace('.', '')
print([len(x) for x in str3.split()])

str4 = "Hi He Lied Because Boron Could Not Oxidize Fluorine. New Nations Might\
 Also Sign Peace Security Clause. Arthur King Can.".split()

# 05

word_index = {1, 5, 6, 7, 8, 9, 15, 16, 19}

result = dict()
str4_length = len(str4)

for i in range(str4_length):
    cutoff = 1 if i in word_index else 2
    result[str4[i][:cutoff]] = i

print(result)

# 05

def ngram(string_to_ngram, n):
    input_len = len(string_to_ngram)
    shift_amount = n-1
    input_array = [x for x in string_to_ngram]
    result = []

    new_gram = ''.join(input_array[:shift_amount])

    for i in range(shift_amount, input_len):  # O(m) m = input length
        new_gram += input_array[i]
        result.append(new_gram)
        new_gram = new_gram[1:]  # O(n)

    return result

print(ngram("I am an NLPer", 4))

# 06

bigram1 = set(ngram("paraparaparadise", 2))
bigram2 = set(ngram("paragraph", 2))
print('union: ', bigram1|bigram2) # 和集合
print('intersection: ', bigram1&bigram2) #  積集合
print('difference: ', bigram1-bigram2) # 差集合
print('se' in bigram1)
print('se' in bigram2)

# 07

def show_temperature(x,y,z):
    return u"{0}時の{1}は{2}".format(x,y,z)

print(show_temperature(12, u'気温', 22.4))

# 08

def cipher(string_to_encode):
    encoded_input = ''
    for char in string_to_encode:
        if char.islower():
            encoded_input += chr(219 - ord(char))
        else:
            encoded_input += char
    return encoded_input

print(cipher('Hello World! Today is November 12, 2015.'))

# 09

def shuffle_word(word):
    word = list(word)
    return word[0] + ''.join(sample(word[1:-1], len(word)-2)) + word[-1]

def typoglycemia(string_to_randomize):
    input_array = re.split('(\W+)', string_to_randomize)
    print(input_array)
    output_string = ''
    for word in input_array:
        if len(word) > 3:
            output_string += shuffle_word(word)
        else:
            output_string += word
    return output_string

print(typoglycemia("I couldn't believe that I could actually understand what I was reading : the phenomenal power of the human mind ."))
