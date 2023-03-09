str1 = "Participant Number:    8475"
str2 = "Alice finished university 1 years earlier, with an average grade of 3/4... Mindblowing!"

#extract one INT number 


def extract_the_num(text):
    digits = ['0','1','2','3','4','5','6','7','8','9','.',',']
    a_num = []
    i = 0
    while (i<len(text)):
        if text[i] in digits:
            a_num.append(text[i])
            #put each digit as a sepate digit in a list
            if i+1 < len(text):
                while text[i+1] in digits:
                    a_num.append(text[i])
                    if i+1 < len(text):
                        i = i + 1
                    else:
                        break
                #join all digits as a string
                for k in a_num:
                    print(a_num)
                #num = num + a_num[k]
              
                #convert string to int
                num = int(num)
                print('num = ',num)
        i=i+1
        
          
extract_the_num(str1)    
extract_the_num(str2) 
