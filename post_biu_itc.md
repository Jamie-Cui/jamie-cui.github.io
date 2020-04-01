---
layout: post
title:  "Information Theoretic Cryptography"
date:   2019-11-12 12:00:00 +0000
author: Jamie
---

**Definition 1 (Cryptography)**: *Communication* and *Computation* in the presence of adversary.

<img src="{{site.url}}{{site.baseurl}}/assets/img/biu_itc_1.png" alt="Drawing" style="width: 600px;"/>

## 1. Computation & Information Theoretic Cryptography

- *Computation Cryptography* exploits **computational limitation** to achieve privacy/authenticity/…
- *Information Theoretic Cryptography* exploits **information gaps** to achieve privacy/authenticity/…

也就是说 Computation Cryptography 假设了 poly-bounded adversary，而 Information Theoretic Cryptography 假设了 Computationally unbounded Adversary

我们在下表中对双方做一个浅显的比较。

| Computational Cryptography | IT Cryptography                           |
| -------------------------- | ----------------------------------------- |
| Comp-limited adversary     | Comp-unbounded adversary                  |
| Unproven assumptions       | Unconditional (no assumptions)            |
| Composability issues       | Good closure properties                   |
| Complicated def’s          | Easy to define and work with (concretely) |
| Allows magic (PRG/PKC/OT/) | No magic (useless w/o information gaps)   |
| Short keys                 | Long keys/large communication             |
| May be comp. expensive     | Typically fast (for short messages)       |

## 2. The Crypto Tower

大致了解到上述概念之后，我们回到常用密码学 primitives 的 Assumption 难度：

| Primitives            | Assumption   | Examples                  |
| --------------------- | ------------ | ------------------------- |
| Obfustopia            | Obsfuscation | MMAPS-based obfuscation   |
| Secure Computation    | OT           | GMW-MPC, GMW-ZK, Yao-GC   |
| Public-Key            | RSA          | FDH-RSA, RSA-OAEP, DDH-KA |
| Symmetric             | AES          | HILL, GL, GGM             |
| Information Theoretic | One-time pad |                           |

（破解难度是越靠下越高）

## 3. Case Study

### 3.1. Perfect Encryption 

> 完美加密，来源于 [Shannon 48]

我们先来看一下Shannon加密解密流程，图中 $M\in\\{0,1\\}^n$ 代表 $n$ bit 的输入数据，$\mathbf{K}$ 为密钥空间，$K$为密钥。

<img src="{{site.url}}{{site.baseurl}}/assets/img/biu_itc_2.png" alt="Drawing" style="width: 600px;"/>

这是一个标准的加密解密流程，Shannon formalize 了加密解密的安全，将加解密算法的不同安全模型转换成以下公式，首当其冲的就是“完美安全”。

#### 3.1.1 Perfect Secrecy & Statistical Secrecy & Computational Secrecy

**Definition (Perfect Encryption/Secrecy):** *For every $X,Y\in\\{0,1\\}^n$, where $K\in_R \mathbf{K}$*

$$
E_K(X)\equiv E_K(Y)
$$

我们怎么来理解完美安全中的 $E_K(X) \equiv E_K(Y)$ 呢？Intuitively，我们可以认为在任意合法密钥下，adversary 无法 distinguish 两条不同的、合法 message 所加密出的 cipher。从概率角度来说，

$$
\forall C, Pr[E_K(X)=C]=Pr[E_K(Y)=C]
$$

那么也就是说，我们要证明某加密解密算法满足 Perfect Secrecy 时，需要选取极端条件下的 $C$，将 $X,Y$ 作为随机变量进行概率求解，在证明时加密属于随机事件。

完美安全的定义是十分严苛的，在实际应用中完美安全的加解密算法会有性能上的牺牲（例如OPT密钥过长），因此我们也需要弱化的安全定义“统计安全”来满足实际的应用。

**Definition (Statistical Secrecy):** *For every $X,Y\in\\{0,1\\}^n$, where $K\in_R \mathbf{K}$*

$$
E_K(X)\approx E_K(Y)
$$

同样从概率/统计的角度来解释的话，那就是 $\forall$ set of cipher $S, Pr[E_K(X)=S] \approx_\delta Pr[E_K(Y)=S]$，当然在这个共始终对 $\approx$ 并没有解释，因此在此基础上统计安全又有了进一步的定义：

$$
\forall \text{ unbounded }Adv, |Pr[Adv(E_K(X))=1]-Pr[Adv(E_K(Y))=1]|\leq\delta
$$

当然，在统计安全中我们需要注意，我们假设依然是 unbounded $Adv$，这在现实生活中也是，因此又衍生出了更加弱化，但是更加贴近实际的“计算安全”。

**Definition (Computational Secrecy)[GM’82]:** *For every $X,Y\in\\{0,1\\}^n$, where $K\in_R \mathbf{K}$*

$$
E_K(X)\approx E_K(Y)
$$

其假设了有限攻击资源的供给者，因此计算安全的进一步的定义为：

$$
\forall \text{ comp-unbounded }Adv, |Pr[Adv(E_K(X))=1]-Pr[Adv(E_K(Y))=1]|\leq\delta
$$

#### 3.1.2 Example: Prove OTP is Perfectly Secure

> 下面，我们来证明一下 OTP是满足 Perfect Secrecy 的（即 $\forall X,Y, E_K(X)\equiv E_K(Y)$）

首先，我们定义OPT加密算法的 message space 为 $G$。将 $K$ 作为随机变量，对于任意选取的合法 $C,X$，我们选取的 $X$ 恰好加密为 $C$ 的概率就为 $1/G$，即 $\forall C,X, Pr[E_K(X)=C]=1/\|G\|$

这时，我们可以发现，随机变量 $K$ 组成的映射 $K\mapsto E_K(X)$ 是由 Random Space 映射到 Ciphertext Space 的双射/非退化线性映射 （bijection/non-degenerate linear mapping），（$X,Y,C $ 的取值不影响 $K\mapsto E_K(\cdot)$ 映射的概率分布）

#### 3.1.3 Efficient Measures

我们已经知道了加密属于 Message Space $\mathcal{M}$ 到 Ciphertext Space $\mathcal{C}$ 的映射，通常来说映射需要是一个双射，换句话说也就是$\|\mathcal{M}\|<\|\mathcal{C}\|$（因为我们需要保证加密解密的顺利进行）。那么 Key Space $\mathcal{K}$ 呢？

事实上，我们可以通过特殊的构建方法，使得存在一个 Subset $S\subseteq\mathcal{K}$，并且 $K_1,K_2...,K_n\in S$，其中对于任意 $m\in\mathcal{M}$，有$Enc_{K_1}(m)=Enc_{K_2}(m)=....=Enc_{K_n}(m)$ ，就构成了 Broadcase Encryption 的关键组成原理。[Fiat-Naor94]（如图所示）

<img src="{{site.url}}{{site.baseurl}}/assets/img/biu_itc_3.png" alt="Drawing" style="width: 600px;"/>


### 3.2 Error Correction/Detection 

> 纠错码/检错码，来源于 [Hamming47, Shannon48]

<img src="{{site.url}}{{site.baseurl}}/assets/img/biu_itc_4.png" alt="Drawing" style="width: 600px;"/>

最初的纠错码使用了随机线性映射（Random Linear Mapping），不通过加密的方式，因此十分容易遭到攻击。

我们重新来看 Distributed Storage 这个例子，我们首先假设 Adversary passively corrupts servers，呢么我们可以通过 Secret Sharing 的方法进行加密存储。

<img src="{{site.url}}{{site.baseurl}}/assets/img/biu_itc_5.png" alt="Drawing" style="width: 600px;"/>

问题1：如果有 Cloud Server 掉线怎么办？我们有 **Threshold Secret Sharing**，并有在 $T_{active},T_{erasure}, T_{passive}$ 不同模型下的协议。其中我们需要重点关注 Upper-Bound 和 Lower-Bound 的问题。

后面还有PIR、Secure Computaion 以及 Consensus，之后的章节再做介绍。

## Reference

- [Shannon 48] Shannon, C.E. (1948), A Mathematical Theory of Communication. Bell System Technical Journal, 27: 379-423. doi:[10.1002/j.1538-7305.1948.tb01338.x](https://doi.org/10.1002/j.1538-7305.1948.tb01338.x)
- [GM' 82] S. Goldwasser and S. Micali. Probabilistic encryption and how to play mental poker keeping secret all partial information. In Proceedings of the Fourteenth Annual ACM Symposium on Theory of Computing, 5-7 May 1982, San Francisco, California, USA, pages 365–377. ACM, 1982.
- [Fiat-Naor94] B. Chor, A. Fiat and M. Naor, Tracing traitors, Advances in Cryptology - Crypto’94, Lecture Notes in Computer Science No. 839, Springer Verlag, 1994, 257–270.



 




