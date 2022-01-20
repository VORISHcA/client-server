import codecs
import subprocess
#Если честно, я не очень понял, зачем каждое слово
word1 = 'разработка'
word2 = 'сокет'
word3 = 'декоратор'
word1_1 = '\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430'
word2_1 = '\u0441\u043e\u043a\u0435\u0442'
word3_1 = '\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440'
print(type(word1))
print(type(word1_1))
print(word1_1)

print('----1')

word1 = b'class'
word2 = b'function'
word3 = b'method'

print(type(word1))
print(word1)
print(len(word1))

print('----2')

word1 = b'attribute'
#word2 = b'класс'
#word3 = b'функция'
print('класс, функция SyntaxError: bytes can only contain ASCII literal characters.')

print('----3')

word1 = 'разработка'
word2 = 'администрирование'
word3 = 'protocol'

print(word1.encode('utf-8'))
print(word1.encode('utf-8').decode('utf-8'))
print(word3.encode('utf-8'))
print(word3.encode('utf-8').decode('utf-8'))

print('----4')

args = ['ping', 'youtube.com']
subproc_ping = subprocess.Popen(args, stdout=subprocess.PIPE)
for line in subproc_ping.stdout:
    line = line.decode('cp866').encode('utf-8')
    print(line.decode('utf-8'))

args = ['ping', 'yandex.ru']
subproc_ping = subprocess.Popen(args, stdout=subprocess.PIPE)
for line in subproc_ping.stdout:
    line = line.decode('cp866').encode('utf-8')
    print(line.decode('utf-8'))


print('----5')

with open('test.txt', 'r', encoding='utf-8') as file_t:
    for line in file_t:
        print(line)

print('----6')





