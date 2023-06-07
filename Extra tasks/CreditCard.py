
def Check(number):
    st = str(number)
    l = len(st)
    if 13 > l or 16<l:
        return False
    if len(st) == 13:
        if st[0] == '4' or st[0] == '5':
            pass
        else:
            return False
    if len(st) == 15:
        if st[0] != 6:
            return False
    if len(st) == 16:
        if st[0] + st[1] != 37:
            return False
    sum = 0
    
    for i in range(l-2, -1, -2):
        sum += 2* int(st[i])
    for i in range(l-1, -1, -2):
        sum += int(st[i])
    if sum % 10 == 0:
        return True
    else: 
        return False



card_number = int(input('Enter your credit card number :'))

result = Check(card_number)

if result:
    print('your credit card is valid')
else:
    print('your credit card is not valid')


