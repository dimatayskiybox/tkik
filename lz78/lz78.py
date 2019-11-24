def encodeLZ78(input):
    buffer = ""
    dict = {}
    ans = ''
    for i in range(len(input)):
        if dict.get(buffer + input[i]):
            buffer += input[i]
        else:
            if dict.get(buffer) == None:
                ans += '<0' + ', ' + str(input[i]) + '>\n'
            else:
                ans += '<' + str(dict.get(buffer)) + ', ' + str(input[i]) + '>\n'
            dict[buffer + input[i]] = len(dict) + 1
            buffer = ""
    if buffer:
        last_ch = buffer.peek()
        buffer.pop()
        ans += '<' + str(dict[buffer]) + ', ' + str(last_ch) + '>'
    return ans


def decodeLZ78(input):
    dict = []
    ans = ""
    print('Input string')
    for line in input.read().split("\n"):
        print(line)
        line = line.split(',')
        if len(dict) >= int(line[0]) and int(line[0]) != 0:
            word = dict[int(line[0]) - 1] + line[1]
        else:
            word = "" + line[1]
        ans += word
        dict.append(word)
    print('---------------------------------')
    return ans

### DECODE ###
print('Decoding')
s = open("lz78/decode.txt", "r+")
print('Result: \n' + decodeLZ78(s))
### END ###
print('\n')
print('Encoding')
### ENCODE ###
s = open("lz78/encode.txt").read()
print('Result: \n' + encodeLZ78(s))
### END ###
