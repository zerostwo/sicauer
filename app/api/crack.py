with open('./user_id', 'r') as f:
    users = f.readlines()
with open('./finish', 'r') as f:
    finish = f.readlines()

print(len(users), len(finish))
for i in users:
    if i in finish:
        users.remove(i)
print(len(users), len(finish))
