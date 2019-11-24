import struct
import os
import sys
import re


def findMatching(s, pos, buff_size=5):
    buffer = s[max(0, pos - buff_size): pos]
    offset, length = 0, 0
    lastFound = []
    i = pos

    for i in range(pos, len(s)):
        find = list(re.finditer(s[pos:i + 1], buffer))

        if len(find) > 0:
            lastFound = find
        else:
            break

    z = 0
    #### check cycles in the END of buffer ####
    if len(lastFound) > 0 and lastFound[-1].end() == len(buffer):
        for j in range(i, len(s)):
            nextChar = buffer[lastFound[-1].start() + z % (len(buffer) - lastFound[-1].start()):
                              lastFound[-1].start() + 1 + z % (len(buffer) - lastFound[-1].start())]
            if s[j: j + 1] == nextChar:
                z += 1
            else:
                break

    if len(lastFound) > 0:
        offset = len(buffer) - lastFound[-1].start()
        length = len(s[pos:i + z]) if pos != i + z else 1

    return offset, length

def encodeLZ77(s):
    ans = []
    pos = 0
    while pos < len(s):
        offset, length = findMatching(s, pos)
        pos += length
        ans.append([offset, length, s[pos] if pos < len(s) else "end"])
        pos += 1
    return ans

def decodeLZ77(s):
    ans = ""
    start = 0
    for line in s.read().split("\n"):
        print(line)
        line = line.split(',')
        if int(line[1]) > 0:
            start = len(ans) - int(line[0])
            for i in range(int(line[1])):
                ans += ans[start + i]
        ans += line[2] if line[2] != 'end' else ''
    print(ans)


### DECODE ###
print('Decoding:')
s = open("lz77/decode.txt", "r+")
print('Input:')
decodeLZ77(s)
### END ###
print('\n')
### ENCODE ###
print('Encoding:')
string = open("lz77/encode.txt").read()
print('Input: \n' + string)
encodedString = encodeLZ77(string)
print("result:")
for node in encodedString:
    print(node)
### END ###

