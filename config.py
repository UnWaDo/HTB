SECRET_KEY = 'ItIsTheMostSecuredSecretKey'

f = open("web/data.txt", 'r')
users = f.readline().split(" ")
ALLOWED_USERS = [int(user) for user in users]
f.close()
