import random
def test_thirds(ran):
    a=range(ran)
    random.shuffle(a)

    c=0
    for i,el in enumerate(a):
        if i<ran/3 and el<ran/3 or i>=ran/3 and el>=ran/3:
            c+=1

    return c*1./ran


from collections import defaultdict
def test_thirds2(ran):
    a=range(ran)
    random.shuffle(a)
    a_score=defaultdict(int)

    b=range(ran)
    random.shuffle(b)
    b_score=defaultdict(int)
    c=0
    for i in range(ran/3):
        a_score[a[i]]=1
        b_score[b[i]]=1

    for i in range(ran):
        if a_score[i]==b_score[i]:
            c+=1

    return c*1./ran

print test_thirds(10000)

print test_thirds2(1000)

print 5./9