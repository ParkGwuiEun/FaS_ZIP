import sys
import argparse
import os
import zipfile
import struct

# zip 파일을 연다.
f = open("Park Gwui Eun.zip",'rb')

# 파일 개수를 파악하기 위해 End of Central Directory Record 부분의 Central Directory 개수를 나타내는 offset으로 이동
f.seek(-12,2)
file_count = f.read(2) # 파일 개수 나타내는 영역 2바이트
count = (int.from_bytes(file_count,byteorder="little")) # 해당 값을 10진수 값으로 바꿔준다.
print("file_count :", count, "개")

f.seek(0) # 파일의 시작점으로 이동

# 파일 정보 읽기 (하나씩 i에 담아지고 파일 개수만큼 실행됨.)
for i in range(0, count) :
    if i == 0:
        local_header = f.read(18) # 시작점부터 18바이트 떨어진 위치가 첫 번째 파일의 데이터 크기이다.

    if i != 0: # 2번째 파일이 존재할 경우와 아닐 경우를 나누어서 표현했다.
        file_local_signature = f.read(4) 
        #print("file", (i+1), "_local_signature :", file_local_signature.hex())

        if (file_local_signature[0]==0x50 and file_local_signature[1]==0x4B and 
            file_local_signature[2]==0x03 and file_local_signature[3]==0x04) :
            print("local signature인 504b0304값이 나왔으므로 ", (i+1), "번째 파일 존재") 
            # local signature 값이 나올 경우 다음 파일의 local file header임을 알 수 있다.

            local_header = f.read(14)
        else:
            #print("Central Directory로 이동")
            break  # 아닐 경우 Central Directory 영역으로 넘어간다.

    # 아까 18byte 떨어진 위치부터 4바이트가 data size를 나타낸다.
    file_compressed_size = f.read(4)
    data_size = (int.from_bytes(file_compressed_size,byteorder="little"))
    print("file_compressed_size :", data_size)
    file_uncompressed_size = f.read(4)

    # 그 다음 2바이트가 file name의 size를 나타낸다.
    file_name_size = f.read(2)
    name_size = (int.from_bytes(file_name_size,byteorder="little"))
    #print("file", (i+1), "_name_size :", name_size)
    #print("file",+ (i+1), "_name_size :", hex(name_size))

    # 그 다음 2바이트가 extra field의 size를 나타낸다.
    file_extra_field_size = f.read(2)
    extra_size = (int.from_bytes(file_extra_field_size, byteorder="little"))
    #print("file", (i+1), "_extra_field_size :", extra_size)

    # 그 다음 영역은 위의 file name의 size만큼 읽은 것이 file name을 나타낸다. 
    file_name = f.read(name_size)
    print("file", (i+1), "_name :", file_name)

    # file name 영역 바로 다음이 file data가 시작하는 offset을 나타낸다.
    file_data_start_offset = f.tell()
    print("file", (i+1), "_data_start_offset :", hex(file_data_start_offset))

    # 그 해당 offset부터 위의 data size만큼 읽을 때 해당 data를 나타낸다. 
    file_data = f.read(data_size)
    #print("file", (i+1), "_data :", file_data)

    # data영역이 끝난 후 해당 file의 extra field 영역을 나타낸다. 
    file_extra_field = f.read(extra_size)
    #print("file", (i+1), "_extra_field :", file_extra_field)

    print()
    print()


# 파일마다 해당 데이터 영역을 따로 저장
f.seek(0,0) # 파일 처음 부분
f.seek(46) # file 1의 데이터 시작 영역까지
first_file = f.read(15) # 그 위치부터 데이터 크기 만큼 읽는다.
file1 = open("FaS fighting.txt", 'wb')
file1.write(first_file)

# file 2도 위 구조와 동일
f.seek(0,0)
f.seek(102)
second_file = f.read(34)
file2 = open("Kookmin.txt", 'wb')
file2.write(second_file)

# file 3도 위 구조와 동일
f.seek(0,0)
f.seek(174)
third_file = f.read(25)
file3 = open("Math.txt", 'wb')
file3.write(third_file)