def ignor_octothorpe(text):
    #通过遍历每一行 返回#号前面的数据
    for i,item in enumerate(text):
        if item=="#":
            return text[:x]
        pass
    return text

user_list=[]

file=open("baseftp.ini",encoding="utf-8")
# 读取每行的配置文件

while 1:
    line=file.readline()
    # 通过返回字符的行数来判断该行是否为空
    if len(ignor_octothorpe(line))>3:
        user_list.append(line.split())
    if not line:
        break

# 验证时候通过解包把值解出来并动态添加到权限列表去
for user in user_list:
    name,passwd,permit,homedir=user
    try:
        authorizer.add_user(name,passwd,homedir,perm="elradfmw")
    except:
        print("配置文件错误请检查是否正确匹配了相应的用户名、密码、权限、路径")
        print(user)