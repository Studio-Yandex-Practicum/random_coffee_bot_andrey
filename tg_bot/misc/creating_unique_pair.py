# from admin_panel.telegram.models import TgUser
# import random



def finding_coffee_partners(*args):
    args = list(set(args))
    result = []
    while True:
        if len(args) != 1:
            i = 0
            j = -1
            result.append((args[i], args[j]))
            args.pop(j)
            args.pop(i)
        else:
            break
    print(result)


finding_coffee_partners('a', 'b', 'c', 'd', 'e', 'f', 'g')

# print({'1','2','3','4','5','6','7','8','9'})

# def find_all_users():
#     users = TgUser.objects.filter(
#         bot_unblocked=True,
#         is_unblocked=True,
#         is_active=True
#     )
