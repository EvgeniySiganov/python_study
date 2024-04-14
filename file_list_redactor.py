import os
import sys

operations = {"A": "[A]dd", "D": "[D]elete", "S": "[S]ave", "Q": "[Q]uit"}
list_lists_new = {}
list_lists_current = []
current_list = []
change_list = []
both_lists = []


def file_worker(list_name):
    global current_list
    if list_name in list_lists_current:
        with open("tmp/" + list_name, "r+") as rw:
            current_list = rw.readlines()
            show_items(current_list)
            if len(current_list) == 0:
                print("-- no items are in the list --")
                action = get_actions("AQ").upper()
            else:
                action = get_actions("ADQ").upper()
            if action == "A":
                add_list(list_name)
            elif action == "D":
                delete_item(list_name)
            else:
                sys.exit()
    elif list_name in list_lists_new:
        None
    else:
        add_list(list_name)
        print("-- no items are in the list --")
        action = get_actions("AQ")
        if action.upper() == 'A':
            add_item(list_name)
        elif action.upper() == 'Q':
            sys.exit(0)
        else:
            main()
    loop_actions(list_name)


def add_list(name, show=False):
    list_lists_new[name] = []
    if name in list_lists_current:
        list_lists_current.remove(name)
    both_lists = sorted(list_lists_current + list(list_lists_new.keys()), key=lambda x: x.lower())
    if show:
        show_items(both_lists)


def add_to_worker(current_list):
    current_list.append()


def add_item(name_of_list):
    item = input("Add item: ")
    list_lists_new[name_of_list].append(item)
    show_items(list_lists_new[name_of_list])


def delete_item(name_of_list):
    if list_lists_current.__contains__(name_of_list):
        list_lists_new[name_of_list] = current_list
    item = input("Delete item number (or 0 to cancel): ")
    if not item.isdigit() or int(item) < 0 or int(item) > len(list_lists_new[name_of_list]):
        print(f"ERROR: invalid choice--enter one of from 0 to {len(list_lists_new[name_of_list])}")
        delete_item(name_of_list)
    elif int(item) == 0:
        return
    else:
        del list_lists_new[name_of_list][int(item) - 1]
        show_items(list_lists_new[name_of_list])


def save_item(name_of_list):
    with open("tmp/" + name_of_list, "w+") as file:
        file.write(str(list_lists_new[name_of_list]))
    value = list_lists_new.pop(name_of_list)
    list_lists_current.append(name_of_list)
    current_list = value

def delete_list(list_name):
    list_lists_new[list_name].remove()


def show_items(list_items):
    ind = 1
    whitespaces = int(len(list_items) / 10)
    for i in list_items:
        print((" " * whitespaces) + str(ind) + ": " + i)
        ind += 1


def get_actions(available_actions):
    show_actions = ""
    aliases = ""
    for a in available_actions:
        show_actions += operations.get(a.upper()) + " "
        aliases += a.upper() + a.lower()
    result = input(show_actions.strip() + ": ")
    if result in aliases:
        return result
    else:
        print(f"ERROR: invalid choice--enter one of '{aliases}'")
        return get_actions(available_actions)



def main():
    global list_lists_current
    files = os.listdir("tmp/.")
    list_lists_current = list(filter(lambda x: x.endswith(".lst"), files))
    if len(list_lists_current) > 0:
        show_items(list_lists_current)
        item = input("Choise a number of list (or 0 to cancel): ")
        if not item.isdigit() or int(item) < 0 or int(item) > len(list_lists_current):
            print(f"ERROR: invalid choice--enter one of from 0 to {len(list_lists_current)}")
            main()
        elif int(item) == 0:
            sys.exit(0)
        else:
            file_worker(list_lists_current[int(item) - 1])
    else:
        filename = input("Choose filename: ") + ".lst"
        file_worker(filename)
    #[A]dd [D]elete [S]ave [Q]uit [a]:]: a


def loop_actions(list_name):
    action = get_actions("ADSQ")
    while action.upper() != "Q":
        if action.upper() == "A":
            add_item(list_name)
        elif action.upper() == "D":
            delete_item(list_name)
        elif action.upper() == "S":
            save_item(list_name)
        if action.upper() == "S":
            action = get_actions("ADQ")
        else:
            action = get_actions("ADSQ")
    if list_lists_new.keys().__contains__(list_name):
        yn = input("Save unsaved changes (y/n): ").lower()
        if yn in ["yes", "y"]:
            save_item(list_name)
        else:
            sys.exit(0)


if __name__ == "__main__":
    main()
