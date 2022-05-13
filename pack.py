import io
import zlib
import sys

if (len(sys.argv) < 2):
    print('Expected argument\nUsage: "python pack.py xmlFileName"')
    exit()

file = io.open(sys.argv[1], 'r')
data = file.read()
file.close()

replacements = 0
startIndex = 0
endIndex = 0
luaName = ''
start = ''
end = ''

while startIndex != -1:
    startIndex = data.find('${')
    if startIndex > -1:
        endIndex = data.find('}', startIndex)
        luaName = data[startIndex + 2 : endIndex]
        print(f'Reference found: \'{luaName}\'')

        try:
            luaFile = io.open(f'Lua/{luaName}', 'r')
            luaScript = luaFile.read()
            luaFile.close()
        except:
            print(f'Unable to open file \'{luaName}\'')
            print('Could not complete packing! Closing...')
            exit()

        start = data[0 : startIndex]
        end = data[endIndex + 1 :]
        data = f'{start}<![CDATA[{luaScript}]]>{end}'
        replacements += 1

print(f'Total replacements: {replacements}')

buildName = 'Build/' + sys.argv[1][0:-3] + 'tosc'

byteData = data.encode('UTF-8')
compressed = zlib.compress(byteData)

file = io.open(buildName, 'wb')
file.write(compressed)
file.close()