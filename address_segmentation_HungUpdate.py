from trie_algorithm import Trie
import unidecode
import re

class addressSegmentation():
    def __init__(self, dataset) -> None:
        self.trie = self.createTrie(dataset)
        self.provinceCheck = ''
        self.districtCheck = ''
        self.wardCheck = ''

    def segment(self, address):
        self.provinceCheck = ''
        self.districtCheck = ''
        self.wardCheck = ''
        province, district, ward = '', '', ''
        breakFlag = False                         #new from Hung
        DistrictEqualWardFlag = False				#new from Hung
            
        inputAddress = self.preprocessing(address)
        inputAddressFIRST = inputAddress  #new from Hung
        NotFoundProvince, NotFoundDistrict = False, False #new from Hung
        
        # Search for province -> output: address without province part if found 
        # or address with N characters left out if not 
        # N is number of retry times for searching
        inputAddress1, search_result = self.findProvince(inputAddress)

        # Search for district -> output: address with district part being left out if found
        if self.provinceCheck != '':
            province = search_result[-1]
            inputAddress2, search_result = self.findDistrict(1, inputAddress1)
        else:
            # In case, if can't search for province, 
            # it will use each province in total to search for district 
            # with longer text
            NotFoundProvince = True  #note that's province is missing or not correct #new from Hung
            province_list = self.trie.list_children1()
            for item in province_list:   
                self.provinceCheck = item
                inputAddress2, search_result = self.findDistrict(2, inputAddress)
                #print(provinceCheck)
                if self.districtCheck != '':
                    province = search_result[0]
                    district = search_result[1]
                    break
            
            # If can't search for district, erase temp province value
            if self.districtCheck == '':
                self.provinceCheck = ''

        # Search for ward
        if self.provinceCheck == '' and self.districtCheck == '': #
            #Start new from Hung
            NotFoundDistrict = True
            province_list = self.trie.list_children1()
            quotient, remainder = divmod(len(inputAddress), 2)
            res_first = inputAddress[:quotient + remainder]
            for item in province_list:
                self.provinceCheck = item
                district_list = self.trie.list_children2(self.provinceCheck)
                for item1 in district_list:
                    self.districtCheck = item1
                    ward_list = self.trie.list_children3(self.provinceCheck, self.districtCheck)
                    inputAddress3, search_result = self.findWard(3, res_first)
                    if self.wardCheck != '':                      
                        if address.find(',,') != -1 or address.find(', ,') != -1:
                            province = search_result[0]
                            district = ''
                        else:
                            province = ''
                            district = search_result[1]
                        ward = search_result[2]
                        breakFlag = True
                        break
                if breakFlag == True:
                    break
            #End new from Hung
        elif self.districtCheck != '':
            district = search_result[-1]
            inputAddress3, search_result = self.findWard(1, inputAddress2)
            if self.wardCheck != '':
                ward = search_result[-1]
            #start new from Hung	
            else:  #tìm xã bằng chuỗi trước khi tìm huyện
                inputAddress3, search_result = self.findWard(1, inputAddress1)              
                if self.wardCheck != '':
                    ward = search_result[-1]  #lúc này huyện và xã cùng tên
                    DistrictEqualWardFlag = True
            #End new from Hung
        else:
            NotFoundDistrict = True # new from Hung
            district_list = self.trie.list_children2(self.provinceCheck)
            for item in district_list:
                self.districtCheck = item
                inputAddress3, search_result = self.findWard(2, inputAddress1)
                if self.wardCheck != '':
                    district = search_result[1]
                    ward = search_result[2]
                    break
        #start new from Hung     
        if NotFoundDistrict == True and NotFoundProvince == True:
            pass
        elif NotFoundProvince == True and NotFoundDistrict == False:
            temp = len(inputAddressFIRST) - (inputAddressFIRST.find(self.districtCheck) + len(self.districtCheck))
            if temp < 4:
               province = ''
        elif NotFoundProvince == False and NotFoundDistrict == True:
            temp = inputAddressFIRST.find(self.provinceCheck) - (inputAddressFIRST.find(self.wardCheck) + len(self.wardCheck))
            if temp < 4:
               district = ''
        if province == 'Hà Giang' and inputAddressFIRST.find('nongtruongvietlam') != -1: #case đặc biệt, tên quá dài nên hard code =))
            ward = 'Nông Trường Việt Lâm'           
        if DistrictEqualWardFlag == True:           #xã và huyện cùng tên, nếu có kí tự ,, or , , trong address thì tức huyện missing, xoá huyện đi           
            if address.find(',,') != -1 or address.find(', ,') != -1:
                district = ''   #xoá huyện
            else:
                ward = ''   #xoá xã
            #End new from Hung
        result = {
            "province": province,
            "district": district,
            "ward": ward
        }
        return result

    def preprocessing(self, text):
        """Remove redundant characters, lowercase text, and remove accent marks."""
        text = text.replace('\n','').lower()
        text = text.replace(',tph ','').replace(' tph ','').replace('tph.','').replace('tp.','').replace(',tp ','').replace(' tp ','').replace('thành phố','').replace('tỉnh','').replace(' t ','').replace(',t ','')  # new from Hung
        text = unidecode.unidecode(text)
        #text = text.replace('j','')
        text = text.replace('w','').replace('z','g')
        return re.sub('[^A-Za-z0-9]+', '', text) 

    def createTrie(self, dataset):
        trie = Trie()
        for address in dataset:
            parts = address.replace('\n','').split(',')
            list1 = [parts[0],parts[1],parts[2]]
            list2 = [parts[3],parts[4],parts[5]]
            trie.insert(list1, list2)
        return trie

    def findProvince(self, inputAddress):
        search_result = []
        positionMatch = 0

        retry_count = 16
        while retry_count > 0:
            if len(inputAddress) < 2:
                    break
            retry_count -= 1
            num_char_check = 0
            char_pos = len(inputAddress) - 1
            while num_char_check < 15:
                if len(inputAddress) < 2 or len(inputAddress) - num_char_check == 0:
                    break
                data = []
                if inputAddress[char_pos].isnumeric() != True:  #bỏ qua số trong tên tỉnh 
                    data.append(inputAddress[char_pos:len(inputAddress)])
                else:
                    inputAddress = inputAddress[0:char_pos] + inputAddress[char_pos+1:len(inputAddress)]
                    data.append(inputAddress[char_pos:len(inputAddress)])
          
                search_result = self.trie.search(data)
                #print('Tìm trong Trie: ',data , search_result)
                if search_result != False:
                    positionMatch = char_pos
                    self.provinceCheck = data[0]
                    break #không có tỉnh trùng hoặc tên tỉnh nằm trong tên tỉnh khác
                num_char_check += 1
                char_pos -= 1
            if self.provinceCheck != '':    
                inputAddress = inputAddress[0:positionMatch]
                #print(f'xoá phần tử {self.provinceCheck}, input còn lại: ',inputAddress)
                return inputAddress, search_result
            else:
                inputAddress = inputAddress[0:len(inputAddress)-1]
                #print('Không tìm thấy tỉnh nào, xoá phần tử cuối cùng khỏi input: ', inputAddress)
        return inputAddress, search_result

    def findDistrict(self, case, inputAddress):
        positionMatch = 0
        search_result = []

        retry_count = 0
        if case == 1:
            retry_count = 18 #change 16 to 18 # new from Hung
        elif case == 2:
            retry_count = 33 #change 31 to 33 # new from Hung

        while retry_count > 0:
            if len(inputAddress) < 2:
                break
            retry_count -= 1
            num_char_check = 0
            char_pos = len(inputAddress) - 1
            while num_char_check < 18: #change 16 to 18 # new from Hung
                if len(inputAddress) < 2 or len(inputAddress) - num_char_check == 0: # new from Hung ( correct last bug)
                    break
                data = []                       
                data.append(self.provinceCheck)
                # begin new from Hung
                if inputAddress[char_pos].isnumeric() != True:  #check kí tự khác số ?
                    data.append(inputAddress[char_pos:len(inputAddress)])
                else:
                    if inputAddress[char_pos-1].isnumeric() == True:
                        char_pos -= 1
                        data.append(inputAddress[char_pos:len(inputAddress)]) #tìm 2 số liên tiếp nếu có 
                    else:
                        data.append(inputAddress[char_pos:len(inputAddress)])  #ko có thì tìm bth
                #end new from Hung
                search_result = self.trie.search(data)
                #print('Tìm trong Trie: ',data , search_result)
                if search_result != False:
                    positionMatch = char_pos
                    self.districtCheck = data[1]
                    break 
                num_char_check += 1
                char_pos -= 1
            if self.districtCheck != '':    
                inputAddress = inputAddress[0:positionMatch]
                #print(f'xoá phần tử {self.districtCheck}, input còn lại: ',inputAddress)
                return inputAddress, search_result
            else:
                inputAddress = inputAddress[0:len(inputAddress)-1]
                #print('Không tìm thấy Huyện nào, xoá phần tử cuối cùng khỏi input: ', inputAddress)   
        return inputAddress, search_result

    def findWard(self, case, inputAddress):
        positionMatch = 0
        search_result = []

        retry_count = 0
        if case == 1:
            retry_count = 19  # new from Hung
        elif case == 2:
            retry_count = 49 # new from Hung
        elif case == 3: # new from Hung
            retry_count = len(inputAddress) # new from Hung
        while retry_count > 0:
            if len(inputAddress) < 2:
                break
            retry_count -= 1
            num_char_check = 0
            char_pos = len(inputAddress) - 1
            while num_char_check < 19: # new from Hung 19
                if len(inputAddress) < 2 or len(inputAddress) - num_char_check == 0:
                    break
                data = []
                data.append(self.provinceCheck)
                data.append(self.districtCheck)
                # start new from Hung
                if inputAddress[char_pos].isnumeric() != True:  #check kí tự khác số ?
                    data.append(inputAddress[char_pos:len(inputAddress)])
                else:
                    if inputAddress[char_pos-1].isnumeric() == True:
                        char_pos -= 1
                        data.append(inputAddress[char_pos:len(inputAddress)]) #tìm 2 số liên tiếp
                    else:
                        data.append(inputAddress[char_pos:len(inputAddress)])                
                #end new from Hung
                search_result = self.trie.search(data)
                #print('Tìm trong Trie: ',data , search_result)
                if search_result != False:
                    positionMatch = char_pos
                    self.wardCheck = data[2]
                    break 
                num_char_check += 1
                char_pos -= 1

            if self.wardCheck != '':    
                inputAddress = inputAddress[0:positionMatch]
                #print(f'xoá phần tử {self.wardCheck }, input còn lại: ',inputAddress) #thêm self.
                return inputAddress, search_result
            else:
                inputAddress = inputAddress[0:len(inputAddress)-1]
                #print('Không tìm thấy Xã nào, xoá phần tử cuối cùng khỏi input: ', inputAddress)  
        return inputAddress, search_result
