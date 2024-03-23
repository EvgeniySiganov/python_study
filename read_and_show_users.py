
set_nicks = ()


def create_nick(words):
    index_of_second_part = 0
    result = words[0][index_of_second_part].lower() + words[1].lower()
    while result in uniq_nicks:
        index_of_second_part += 1
        result = words[0][:index_of_second_part + 1].lower() + words[1].lower()
    return result


def print_users(list_of_users):
    sorted_data = sorted(list_of_users, key=lambda x: (x[1], x[3]))
    name = "___________________"
    user_id = "______"
    username = "________"
    print("Name" + (" " * (len(name) - len("Name"))) + " " + "ID" + (" " * (len(user_id) - len("ID"))) + " Username")
    print(name + " " + user_id + " " + username)
    for i in sorted_data:
        n = i[1] + " " + i[3] + " "
        print(n + " " * (len(name) - len(n)) + " " + f"({i[0]}) " + i[5])


with open("MyZen.txt", "r") as r:
    l = r.readlines()
    ll = []
    uniq_nicks = {}
    for i in l:
        p = i.split(":")
        nick = create_nick([p[1], p[3]])
        p.append(nick)
        ll.append(p)
    print_users(ll)
