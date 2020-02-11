import paramiko
import re

# 创建一个ssh的客户端
ssh = paramiko.SSHClient()
# 创建一个ssh的白名单
know_host = paramiko.AutoAddPolicy()
# 加载创建的白名单
ssh.set_missing_host_key_policy(know_host)
# 连接服务器
ssh.connect(
    hostname="172.16.32.210",
    port=22,
    username="root",
    password="Test123456!"
)

shell = ssh.invoke_shell()
shell.settimeout(1)

# command = input(">>>"+"\n")
# shell.send('')
is_show = True
while True:
    try:
        recv = shell.recv(512).decode()
        
        if recv:
            if is_show:
                # print(recv,222)
                rec = re.sub(b'\x1b'.decode()+r'.+?m','', recv)
                # aa=re.findall(r'\?.+?m',recv)
                print(rec, end='')
                # print('_'*30)
                # print(aa)
            is_show = True
        else:
            print(recv,112)
            continue
    except Exception as e:
        if e is KeyboardInterrupt:
            break
        try:
            command = input() + "\n"
        except KeyboardInterrupt:
            shell.send('exit\n')
            recv = shell.recv(512).decode()
            if recv:
                rec = re.compile(r'\?\[.+?m').sub('', recv)

                print(rec, end='')
            else:
                continue
            break

        shell.send(command)
        is_show = False

        if command == 'exit\n':
            recv = shell.recv(512).decode()
            if recv:
                rec = re.compile(r'\?\[.+?m').sub('', recv)

                print(rec, end='')
            else:
                continue
            break
ssh.close()  # 关闭连接
