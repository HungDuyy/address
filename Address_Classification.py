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
    runtime = 0
    while provinceCheck == '':
        if len(inputAddress) < 2:
                break
        runtime += 1
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
           break
        else:
           inputAddress = inputAddress[0:len(inputAddress)-1]
           #print('Không tìm thấy tỉnh nào, xoá phần tử cuối cùng khỏi input: ', inputAddress)
        if runtime > 15:
            break
    return inputAddress
def Find_District(case,inputAddress):
    global districtCheck
    global positionMatch
    global addressFull
    positionMatch = 0
    runtime = 0
    while districtCheck == '':
        if len(inputAddress) < 2:
            break
        runtime += 1
        i = 0
        j = len(inputAddress) - 1
        while i < 15: #tìm huyện 20 kí tự đổ lại
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
        if runtime > 30 and case == 2:
            break
        elif runtime > 15 and case == 1:  
            break
        if districtCheck != '':    
           inputAddress = inputAddress[0:positionMatch]
           #print(f'xoá phần tử {districtCheck}, input còn lại: ',inputAddress)
           break
        else:
           inputAddress = inputAddress[0:len(inputAddress)-1]
           #print('Không tìm thấy Huyện nào, xoá phần tử cuối cùng khỏi input: ', inputAddress)   
    return inputAddress

#def Find_District_Fast(inputAddress):
   
def Find_Ward(case,inputAddress):
    global wardCheck
    global positionMatch
    global addressFull
    positionMatch = 0
    runtime = 0
    while wardCheck == '':
        if len(inputAddress) < 2:
            break
        runtime += 1
        i = 0
        j = len(inputAddress) - 1
        while i < 15: #tìm xã 15 kí tự đổ lại
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
                #print('ket qua addressFull:',addressFull)
                break 
            i += 1
            j -= 1
        if runtime > 45 and case == 2:
            break
        elif runtime > 15 and case == 1:  
            break
        if wardCheck != '':    
           inputAddress = inputAddress[0:positionMatch]
           #print(f'xoá phần tử {wardCheck}, input còn lại: ',inputAddress)
           break
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

  def search_node1(self, findtext, node1):
    current = self.root
    current = current.children[node1]
    if findtext not in current.children:
        return False
    current = current.children[findtext]
    return current.is_word
    
  def list_children1(self):
    current = self.root
    return list(current.children.keys())
  
  def list_children2(self, node2):
    current = self.root
    current = current.children[node2]
    return list(current.children.keys())
    
  def list_children3(self, node2, node3):
    current = self.root
    current = current.children[node2]
    current = current.children[node3]
    return list(current.children.keys())
 
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
    addressProvince = ''
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
    inputAddress1 = Find_Province(inputAddress)
    #tìm huyện  
    if provinceCheck != '':
        inputAddress2 = Find_District(1,inputAddress1)
        addressProvince = addressFull
    else:
        listProvince = trie.list_children1()
        for item in listProvince:         
            addressFull = ''
            provinceCheck = item
            inputAddress2 = Find_District(2,inputAddress)
            #print(provinceCheck)
            if districtCheck != '':
                break
        if districtCheck == '':
            provinceCheck = ''
    #tìm xã
    if provinceCheck == '' and districtCheck == '':
        pass
    elif districtCheck != '':
        inputAddress3 = Find_Ward(1,inputAddress2)
    else:
        listDistrict = trie.list_children2(provinceCheck)
        for item in listDistrict:
            districtCheck = item
            addressFull = ''
            inputAddress3 = Find_Ward(2,inputAddress1)
            if wardCheck != '':
                break
                
    if addressFull != '':
        print(addressFull)   
    if provinceCheck == '':
        print('"province": ""')
    if addressFull == '' and provinceCheck != '':
        print(addressProvince)
    if districtCheck == '':
        print('"district": ""')
    if addressFull == '' and districtCheck != '':
        print(f'"district": ""')    
    if wardCheck == '':
        print('"ward": ""')
#listDistrict = trie.list_children2('hanoi')
#listWard = ['hanoi',]
#print(listDistrict)
#for item in listDistrict:
  #  print(item)
   # listWard = trie.list_children3('hanoi',item)
   # print(listWard)