---
layout: default
---

# Cryptology；

古典密码学最早追溯于很久很久之前...

现代密码学起源于1970年代，首先随着RSA加密算法的出现，引出了公私钥（非对称）密码学。

- 古典密码学，移位，乱序，但是可以通过频率分析等方法在有限时间内破解
- 对称密码学，例如AES、DES具有很高的保密性，但是需要较长的密钥长度，以及加密解密使用的相同密钥，不能保证安全的特异性。
- 非对称密码学，引出了数字签名、零知识证明、不经意传输等等现代密码学的building block。

在现代密码学开始阶段，密码学协议基于常用的数学难题：离散对数问题、因式分解问题。由于上世纪末出现了Shor算法使得传统的因式分解问题在量子计算机下不再安全。在下面列举了我比较喜欢的几个参考资料，如果喜欢的话，请访问下面链接：

- [Boneh Dan et.al. --- "A Graduate Course in Applied Cryptography“](https://crypto.stanford.edu/~dabo/cryptobook/BonehShoup_0_4.pdf)
- [Boneh's Introcution to Cryptography](https://crypto.stanford.edu/pbc/notes/crypto/)

> 16/08/2019 by Jamie

[番外：那些密码学基于的数学难题 Cryptographic Hardness Assumptions](./hard_problems.html)

[1.1 Encryption; 加密](./encryption.html)