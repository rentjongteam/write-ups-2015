
content = open("meowmeow").read()
for i in range(8, 0, -1):
    a = "_" * i
    content = content.replace(a, str(i))

print ("0%x" % eval(content)).decode("hex")[::-1]


