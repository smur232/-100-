import sys

# 10
# wc -t hightemp.txt
def line_count(filename):
    with open(filename, 'r') as f:
        return sum(1 for _ in f)
line_count("hightemp.txt")

# 11
# sed -e s/$'\t'/' '/g hightemp.txt

with open("hightemp.txt", 'r') as file:
    print("Tab replaced: \n", file.read().replace('\t', ' '), sep='')

# 12
# cut -f 1 hightemp.txt (for first column)

with open("hightemp.txt", "r") as hightempfile, open('col1.txt', 'w') as col1file, open('col2.txt', 'w') as col2file:
    col1 = ""
    col2 = ""
    for line in hightempfile:
        col_separated = line.split()
        col1 += col_separated[0] + '\n'
        col2 += col_separated[1] + '\n'
    col1file.write(col1)
    col2file.write(col2)

# 13
# paste col1.txt col2.txt
with open("col1.txt", "r") as col1, open("col2.txt", "r") as col2, open("merged.txt", "w") as mergedfile:
    two_columns = ""
    for col1line, col2line in zip(col1, col2):
        two_columns += col1line.strip() + '\t' + col2line
    mergedfile.write(two_columns)

# 14
# head -n hightemp.txt

def first_n_lines(n):
    print("first", n, "lines: ")
    with open("hightemp.txt", "r") as hightempfile:
        for i in range(n):
            print(hightempfile.readline(), end='')

first_n_lines(5)

# コマンドライン引数
# with open(sys.argv[1], "r") as hightempfile:
#     n = sys.argv[2]
#     for i in range(n):
#         print(hightempfile.readline(), end='')

# 15
# tail -n hightemp.txt

def last_n_lines(n):
    print("last", n, "lines: ")
    with open("hightemp.txt", "r") as hightempfile:
        all_lines = hightempfile.readlines()
        for line in all_lines[-n:]:
            print(line, end='')
last_n_lines(3)

# 16
# ファイルをn分割する：　file の行数がnで割り切れない場合は、
#　分離されたファイルの行数が１行以上は変わらないようにしました。


def split_to_n_files(n, filename):
    with open(filename) as f:
        tota_line_count = line_count(filename)
        lines_in_file = tota_line_count // n
        num_files_with_extra_line = tota_line_count % n
        lines_in_file_with_extra = lines_in_file + 1
        read_until = num_files_with_extra_line * lines_in_file_with_extra

        file_num = 1
        next_output = []
        for line_num, line in enumerate(f):  #iterator を使うように気をつけたのですが、もう少しスピード・メモリーを
                                                #　効率良くする方法があれば、教えていただきたいです
            if line_num < read_until:
                next_output.append(line)
                if len(next_output) == lines_in_file_with_extra:
                    print(next_output)
                    with open('split_file_{0}'.format(file_num), 'w') as fout:
                        fout.writelines(next_output) # writelines takes a sequence and writes it in each line
                    next_output = []
                    file_num += 1
            else:
                next_output.append(line)
                if len(next_output) == lines_in_file:
                    with open('split_file_{0}'.format(file_num), 'w') as fout:
                        fout.writelines(next_output) # writelines takes a sequence and writes it in each line
                    next_output = []
                    file_num += 1

split_to_n_files(6, 'hightemp.txt')

# 17


def set_of_prefectures(filename):
    prefecture_set = set(extract_col1(filename))
    for prefecture in prefecture_set:
        print(prefecture)


def extract_col1(filename):
    col1_list = []
    for line in open(filename, 'r'):
        col1_list.append(line.split()[0])
    return col1_list

print('\nSet of prefectures: ')
set_of_prefectures('hightemp.txt')

# 18


def sorted_by_temperature(filename):
    with open(filename, 'r') as input_file:
        all_lines = input_file.readlines()
        sorted_lines_by_temp = sorted(all_lines, key=lambda x:x.split()[2], reverse=True)
        for line in sorted_lines_by_temp:
            print(line, end='')
print('\nSorted by temperature: ')
sorted_by_temperature('hightemp.txt')


# 19
from collections import Counter

def sort_by_most_common(filename):
    pref_by_most_common = Counter(extract_col1(filename)).most_common()
    for prefecture in pref_by_most_common:
        print(prefecture[0])

print('\nSorted by most common occurence: ')
sort_by_most_common('hightemp.txt')