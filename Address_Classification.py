import re

s1 = u'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ'
s0 = u'AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYy'

def remove_accents(input_str):
	s = ''
	#print input_str.encode('utf-8')
	for c in input_str:
		if c in s1:
			s += s0[s1.index(c)]
		else:
			s += c
	return s

def Find_Province(inputAddress):
    global provinceCheck
    global positionMatch
    global addressFull
    positionMatch = 0
    while provinceCheck == '':
        if len(inputAddress) < 2:
                break
        i = 0
        j = len(inputAddress) - 1
        while i < 15: #tìm tỉnh 15 kí tự đổ lại
            if len(inputAddress) < 2 or len(inputAddress) - i == 0:
                break
            data = []
            if inputAddress[j].isnumeric() != True:  #bỏ qua số trong tên tỉnh 
                data.append(inputAddress[j:len(inputAddress)])
            else:
                inputAddress = inputAddress[0:j] + inputAddress[j+1:len(inputAddress)]
                data.append(inputAddress[j:len(inputAddress)])
                
            search_result = trie.search(data)
            #print('Tìm trong Trie: ',data , search_result)
            if search_result != False:
                positionMatch = j
                provinceCheck = data[0]
                addressFull = search_result
                break #không có tỉnh trùng hoặc tên tỉnh nằm trong tên tỉnh khác
            i += 1
            j -= 1
        if provinceCheck != '':    
           inputAddress = inputAddress[0:positionMatch]
           #print(f'xoá phần tử {provinceCheck}, input còn lại: ',inputAddress)
        else:
           inputAddress = inputAddress[0:len(inputAddress)-1]
           #print('Không tìm thấy tỉnh nào, xoá phần tử cuối cùng khỏi input: ', inputAddress)
    return inputAddress
def Find_District(inputAddress):
    global districtCheck
    global positionMatch
    global addressFull
    positionMatch = 0
    while districtCheck == '':
        if len(inputAddress) < 2:
            break
        i = 0
        j = len(inputAddress) - 1
        while i < 20: #tìm huyện 20 kí tự đổ lại
            if len(inputAddress) < 2 or len(inputAddress) - i == 0:
                break
            data = []
            data.append(provinceCheck)
            data.append(inputAddress[j:len(inputAddress)])
            search_result = trie.search(data)
            #print('Tìm trong Trie: ',data , search_result)
            if search_result != False:
                positionMatch = j
                addressFull = search_result
                districtCheck = data[1]
                break 
            i += 1
            j -= 1
        if districtCheck != '':    
           inputAddress = inputAddress[0:positionMatch]
           #print(f'xoá phần tử {districtCheck}, input còn lại: ',inputAddress)
        else:
           inputAddress = inputAddress[0:len(inputAddress)-1]
           #print('Không tìm thấy Huyện nào, xoá phần tử cuối cùng khỏi input: ', inputAddress)   
    return inputAddress
    
def Find_Ward(inputAddress):
    global wardCheck
    global positionMatch
    global addressFull
    positionMatch = 0
    while wardCheck == '':
        if len(inputAddress) < 2:
            break
        i = 0
        j = len(inputAddress) - 1
        while i < 20: #tìm xã 15 kí tự đổ lại
            if len(inputAddress) < 2 or len(inputAddress) - i == 0:
                break
            data = []
            data.append(provinceCheck)
            data.append(districtCheck)
            data.append(inputAddress[j:len(inputAddress)])
            search_result = trie.search(data)
            #print('Tìm trong Trie: ',data , search_result)
            if search_result != False:
                positionMatch = j
                addressFull = search_result
                wardCheck = data[2]
                break 
            i += 1
            j -= 1
        if wardCheck != '':    
           inputAddress = inputAddress[0:positionMatch]
           #print(f'xoá phần tử {wardCheck}, input còn lại: ',inputAddress)
        else:
           inputAddress = inputAddress[0:len(inputAddress)-1]
           #print('Không tìm thấy Xã nào, xoá phần tử cuối cùng khỏi input: ', inputAddress)  
    return inputAddress
 
class TrieNode:
  def __init__(self):
    self.children = {}
    self.is_word = ''

class Trie:
  def __init__(self):
    self.root = TrieNode()

  def insert(self, data, codau):
    current = self.root
    i = 0
    for part in data:
        if part not in current.children:
            current.children[part] = TrieNode()
        current = current.children[part]
        current.is_word = codau[i]
        #print('current.is_word = ', codau[i])
        i += 1
  def search(self, data):
    current = self.root
    temp = ''
    i = 0
    for part in data:
        if part not in current.children:
            return False
        current = current.children[part]
        if i == 0:
            temp = temp + '\n"province": "' + current.is_word + '"'
        elif i == 1: 
            temp = temp + '\n"district": "' + current.is_word + '"'
        else:
            temp = temp + '\n"ward": "' + current.is_word + '"'
        i += 1
    return temp
 
#==============================================MAIN========================================================================== 
# Create a Trie object
trie = Trie()
provinceCheck = ''
districtCheck = ''
wardCheck = ''
addressFull = ''
positionMatch = 0

Lines = open('D:/Address_Classification_database.txt', encoding="utf8").readlines()  # modify the path
for line in Lines:
    line = line.replace('\n','')
    parts = line.split(',')
    list1 = [parts[0],parts[1],parts[2]]
    list2 = [parts[3],parts[4],parts[5]]
    trie.insert(list1, list2)
Lines = open('D:/inputThay.txt', encoding="utf8").readlines()   # modify the path

for line in Lines:
    provinceCheck = ''
    districtCheck = ''
    wardCheck = ''
    addressFull = ''
    line = line.replace('\n','')
    datatest = line
    datatest = datatest.lower()
    datatest = remove_accents(datatest)
    #datatest = datatest.replace('j','')
    datatest = datatest.replace('w','')
    datatest = datatest.replace('z','g')
    inputAddress = re.sub('[^A-Za-z0-9]+', '', datatest) 
    print('\nInput RAW : ',line)
    print('Input light : ',inputAddress)
    #tìm tỉnh
    inputAddress = Find_Province(inputAddress)
    #tìm huyện
    inputAddress = Find_District(inputAddress)
    #tìm xã
    inputAddress = Find_Ward(inputAddress)
    if addressFull != '':
        print(addressFull)   
    if provinceCheck == '':
        print('"province": "')
    if districtCheck == '':
        print('"district": "')
    if wardCheck == '':
        print('"ward": ""')

