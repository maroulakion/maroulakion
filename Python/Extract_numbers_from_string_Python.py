text1 = "X-DSPAM-Confidence:    8475"
text2 = "At 23 he finished college with 97/100 grade"

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
        
          
extract_the_num(text1)    


            

#extract all INT numbers and put them in a list