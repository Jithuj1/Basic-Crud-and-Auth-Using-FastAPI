
Ballot = {
    "Jithu": 5,
    "mariya":12,
    "manuval":8,
    "salmon":12
}

def Vote(name):
    for key in Ballot:
        if key.lower() == name.lower():
            Ballot[key] +=1
            return True
    return False


def print_function():
    m = 0
    for key, value in Ballot.items():
        c = m
        m = max(m, value)
        if c != m:
            name = key
    print("\n", name)


def print_count():
    vote = [ Ballot[i] for i in Ballot]
    m = max(vote)
    if vote.count(m) > 1:
        for key, value in Ballot.items():
            if value == m:
                print("\n", key)
     


name = input('Enter your candidate name :')

print(Vote(name))

print_count()

print_function()
