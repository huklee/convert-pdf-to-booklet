from pypdf import PdfWriter, PdfReader
import sys

def generate_page_list(n, div=4):
    print (1, n,'pages')
    result = []
    for i in range(int(n/div + 1)):
        if 4*i > n: break
        result += generate_page_list_whole(4*i, min(n, 4*i + 4))
    return result

def generate_page_list_whole(start, end):
    n = end - start
    foo = []
    flag1 = n % 2
    # if n is an odd number, page n+1 is a BlankPage
    if flag1 == 1:
        n += 1

    a = start
    b = end - 1

    #4M or 4M+2 ?
    flag2 = n % 4
    if flag2 == 0: # n = 4M
        for i in range(n):
            flag = i % 4
            if flag == 0:
                foo.append(b)
                b -= 1
            elif flag == 1 or flag == 2:
                foo.append(a)
                a += 1
            elif flag == 3:
                foo.append(b)
                b -= 1
        if flag1 == 1:
            foo[foo.index(n - 1)] = 'b'
    else: #n = 4M+2
        for i in range(n + 2):
            flag = i % 4
            if flag == 0 or flag == 3:
                if i == 0 or i == 3:
                    foo.append('b')
                else:
                    foo.append(b)
                    b -= 1
            elif flag == 1 or flag == 2:
                foo.append(a)
                a += 1
        if flag1 == 1:
            foo[foo.index(n - 1)] = 'b'
    return foo


output = PdfWriter()
print("Filename: ", sys.argv[1])
try:
    pdf = PdfReader(open(sys.argv[1], "rb"))
except Exception as err:
    print ("ERROR: ", err)
    print ('No input file')
    print ('Usage:',sys.argv[0],'[input file]')
    sys.exit(1)
print ('proceeding..')

lastpage = pdf.pages[0]
width = lastpage.mediabox.width
height = lastpage.mediabox.height

for i in generate_page_list(len(pdf.pages)):
    if i == 'b':
        output.add_blank_page(width,height)
    else:
        output.add_page(pdf.pages[i])

print ('writing file...')
outputStream = open(sys.argv[1] + '_booklet.pdf', "wb")
output.write(outputStream)
outputStream.close()
print ("%s pages created." % len(output.pages))
