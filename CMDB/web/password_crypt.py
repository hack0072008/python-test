#!/usr/bin/python
# _*_ coding:utf-8 _*_

from cryptography.fernet import Fernet


# key = base64.urlsafe_b64encode(os.urandom(32))  生成key


# 如果修改了 下面的密钥key 请同步修改一下  webssh/main.py 中的，不然无法解密。

def encrypt_p(password):
    f = Fernet('Ow2Qd11KeZS_ahNOMicpWUr3nu3RjOUYa0_GEuMDlOc=')
    try:
        p1 = password.encode()
        token = f.encrypt(p1)
        p2 = token.decode()
        return p2
    except Exception as e:
        return None


def decrypt_p(password):
    f = Fernet('Ow2Qd11KeZS_ahNOMicpWUr3nu3RjOUYa0_GEuMDlOc=')
    try:
        p1 = password.encode()
        token = f.decrypt(p1)
        p2 = token.decode()
        return p2
    except Exception as e:
        return None


if __name__ == '__main__':
    a = encrypt_p('123456')
    print(a)
    b = decrypt_p(
        'gAAAAABdOGY2JnH3r-z2o_niTNXyTgJuxk8OTAybLrvU8cV5v8FyVARRT-1wlGGWQ1IMcjATeNGHl3hON1Qu516-_n2dx-HTrw==')
    print(b)
