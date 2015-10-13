import requests

def simulate(age, firstans):

    print "Age ", age, " ans = ", firstans

    s = requests.Session()

    a = s.get('http://mbti.asis-ctf.ir/')

    f1 = len(a.content)
    print "First page",  f1

    name = 'ASIS'

    a = s.post('http://mbti.asis-ctf.ir/', data={'name':name, 'start': 'Start!', 'age': age})

    f2 = len(a.content)
    print "Start ", f2
    prevlen = f2

    for i in range(0, len(firstans)):
        print i
        f = firstans[i]
        a = s.post('http://mbti.asis-ctf.ir/', data={'answer': f})
        if i==24:
            print a.content
        f3 = len(a.content)        
        print "Ans ", f,'=', f3
        print "DIFF ", f3-prevlen
        fdiff = f3-prevlen
        prevlen = f3
    return fdiff


# for i in ['0', '1', '2', '3']:
#     for j in ['0', '1', '2', '3']:
#         print "SIM ", simulate(i, j)
# exit(0)

#d = [86,-58, 85, -39, 16, -10, -30, 3, 45, -29, -26, 63, -68, -20, 39, -7, -5, 32,  -64, 70, -16, -14, -47, -1, -659, 0]

d = [51, -91 , -6 , 100 , 26 , -35 , -62 , 46 , -41 , 57 , -17 , 43 , -38 , -50 , 39 , -66 , 33 , -24 , 96 , -104 , 7 , 54 , -20 , -19 , -668, 0]


# a = []
# a = ['1', '3', '0', '2', '0', '1', '2', '1', '0', '2', '0', '3', '2', '2', '1', '3', '3', '3', '0', '2', '2', '0', '2', '2']
a = ['1', '0', '1', '1', '3', '1', '1', '0', '3', '3', '3', '3', '1', '2', '1', '0', '2', '1', '1', '1', '3', '0', '1', '3']

#a = ['1', '0', '1', '1', '3', '1', '1', '0', '3', '3', '3', '0', '1', '2', '1', '0', '2', '1', '1', '1', '3', '0', '1', '3']
#a = []

n = len(a)

while True:
    answers = []
    for j in ['0', '1', '2', '3']:
        tmp = a + [j]
        if simulate('1', tmp)==d[n]:
            print "OK for n = ",n, "ans is ", j
            answers.append(j)
    if len(answers)==1:
        print "only 1 answer", answers
        a.append(answers[0])
    else:
        print "more than 1", answers
        a.append(answers[0])
    n += 1
    print 'current ', a
