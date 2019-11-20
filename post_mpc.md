---
layout: post
title:  "多方安全计算 --- Secure Multiparty Computation"
date:   2019-11-20 12:00:00 +0000
author: Jamie
---

- Awesome List: [Github: rdragos/awesome-mpc](https://github.com/rdragos/awesome-mpc)
- Book: [A Pragmatic Introcution to Secure Multi-Party Computation](https://securecomputation.org/)

| Protocols | \# Parties | \# Rounds     | \# Circuit            |
| --------- | ---------- | ------------- | --------------------- |
| Yao       | 2          | Constant      | Boolean               |
| GMW       | $\geq$ 3   | Circuit depth | Boolean or arithmetic |
| BGW       | $\geq$ 3   | Circuit depth | Boolean or arithmetic |
| BMR       | $\geq$ 3   | Constant      | Boolean               |
| GESS      | 2          | Constant      | Boolean *formula*     |

## 1. Yao/Garbled Circuit

> A. C. Yao.  Protocols for secure computations.  In23rd FOCS, pages 160–164, 1982

Yao's protocol is usually seen as best-performing, and many state-of-art protocols build on Yap's GC. 那么通常来说，使用姚式电路意味着比较低的通信复杂度（固定轮数通信）。

### Protocol；简化版本协议

**Step 1: Assume we want to evaluate $\mathcal{F}(x,y)$, where party $P_1$ holds $x\in X$ and $P_2$ holds $y\in Y.$**

我们首先将函数$\mathcal{F}(x,y)$想象成一个查表算法（对于较小的$X,Y$来说）。那么 $P_1$ 可以生成Table  $T_{x,y} = \langle \mathcal{F}(x,y)\rangle$ 。$P_1$ will then encrypt $T$ by assigning a randomly-chosen strong key to *each* possible input $x$ and $y$. That is, for each $x\in X$ and each $y \in Y$, $P_1$ will randomly choose $k_x\in_R \{0,1\}^k$ and $k_y\in_R \{0,1\}^k$.

**Step 2: $P_1$ will send the encrypted (and permuted!) table $\langle Enc_{k_x, k_y}(T_{x,y})\rangle$ to $P_2$ and $k_x$.** 

现在 $P_2$ 就拥有了 $\langle Enc_{k_x, k_y}(T_{x,y})\rangle$、$y$、$k_x$，那么仅仅缺少正确的 $k_y$ 就可以正确还原出查表的结果了。当然， $k_y$ 的获取不可以通过明文传输的形式，因为映射 $\mathcal{R}: y\to k_y$ 是由$P_1$ 生成，因此在获取$k_x$ 的过程中使用了 1-out-of-|Y| OT协议。

**Step 3: $P_2$ obtains $k_y$ using $\text{OT}^1_{\|Y\|}$**

获取到 $k_x, k_y$ 后 $P_2$ 会针对 $T$ 的每一行进行解密，只有一行会解密成功并得到计算结果。

### Protocol；完整协议

**Step 1: Assume we want to evaluate $\mathcal{F}(x,y)$, where party $P_1$ holds $x\in X$ and $P_2$ holds $y\in Y.$**

**Step 2: $P_1$ will send the encrypted (and permuted!) table $\langle Enc_{k_x, k_y}(T_{x,y})\rangle$ to $P_2$ and $k_x$.** 

**Step 3: $P_2$ obtains $k_y$ using $\text{OT}^1_{\|Y\|}$**

### Optimaization；优化

**1. $P_2$ 如何判断哪一行是正确结果呢？（假设解密函数不会返回ERROR）**

最简单的办法是让 $P_1$ 在 $T$ 的明文末尾加入0，这样的话对于 $P_2$ 来说只有解密后结果末尾为0的才是正确结果（效率比较低下）。

**（优化后的高效方法）Point-and-Permute：** Interpret part of the key as a pointer to the permuted table $T$. It means on receivingg $k_x, k_y$, $P_2$ can efficiently use the first  $\lceil log\|X\|\rceil$ bits of $k_x$ and $\lceil log\|Y\|\rceil$ bits of $k_y$ to locate one row in $T$. Besides, key size must be maintained t o achieve the corresponding level of security.

**2. 如何有效减少 $T$ 的大小？**

Before optimazation size of $T$ scales linearly with the domain size of $\mathcal{F}$. Boolean circuit has domain size of 4, so we need to represent $\mathcal{F}$ as Boolean circuit $\mathcal{C}$.

Each cell of the look-up table encrypts the *label corresponding to the output computed by the gate.* 那么，对于一个布尔电路的 $\mathcal{C}$ 的一个 Gate（input wires: $w_i,w_j$, output wire: $w_t$）来说:

$$T_{G}= \begin{bmatrix} \text{Enc}_{k_i^0,k_j^0}(k_t^{G(0,0)}) \\ \text{Enc}_{k_i^0,k_j^1}(k_t^{G(0,1)}) \\ \text{Enc}_{k_i^1,k_j^0}(k_t^{G(1,0)}) \\ \text{Enc}_{k_i^1,k_j^1}(k_t^{G(1,1)}) \end{bmatrix}$$ if G is AND, then $$T_{G}= \begin{bmatrix} \text{Enc}_{k_i^0,k_j^0}(k_t^{0}) \\ \text{Enc}_{k_i^0,k_j^1}(k_t^{0}) \\ \text{Enc}_{k_i^1,k_j^0}(k_t^{0}) \\ \text{Enc}_{k_i^1,k_j^1}(k_t^{1}) \end{bmatrix}$$

在这种情况下（Boolean），我们只需要 1bit 的Point-and-Permute就可以成功定位了。

**3. 恶意安全模型？**

At an intuitive level, it is easy to see that this circuit-based construction is secure under semi-honest adversary.

**Security against malicious $P_1$ is easy**, (we exclued OT, which has been fully studied) since it reveives no messages from $P_2$. 

**Security against malicious $P_2$**, security boils down to the observation that the **evaluator $P_2$ never sees both labels for the same wire.** 

To simulate $P_2$'s view, the simulator $Sim_{P_2}$ chooses random active labels for each wire, simulates the three "inactive" ciphertexts of each garbled gate as dummy cipher texts, and produces decoding information that decodes the active output wires to the function's output.

## 2. GMW Protocol

> O. Goldreich, S. Micali, and A. Wigderson.  How to play any mental game or A completenesstheorem for protocols with honest majority.  In19th STOC, pages 218–229, 1987.

GMW适用于布尔电路和运算电路。使用正常的Secret Sharing，并使用 Beaver's Multiplication Triples 去解决乘法问题以及AND门问题，下面使用运算电路进行举例。

- Addition gates: $[x]+[y]$
- Multiplication gates: $[x]\cdot[y]$
- Multiplication-by-constant gates: $[x]\cdot c$

### ADD Gate

For addition gate, consider input wires $\alpha, \beta$ and output wires $\gamma$. And consider the case we want to secure perform:

$$f_\text{add}([\upsilon_\alpha],[\upsilon_\beta])=[\upsilon_\alpha+\upsilon_\beta]$$

Wire $\alpha$ shares its value with $x_{\alpha1}$ and $x_{\alpha2}$.
Wire $\beta$ shares its value to $x_{\beta1}$ and $x_{\beta2}$.

Wire $\alpha$ computes $(x_{\alpha1}+x_{\beta1})$

Wire $\beta$ computes $(x_{\alpha2}+x_{\beta2})$

### MUL Gate

For multiplication gate, consider input wires $\alpha, \beta$ and output wires $\gamma$. And consider the case we want to secure perform:

$$f_\text{mul}([\upsilon_\alpha],[\upsilon_\beta])=[\upsilon_\alpha\times\upsilon_\beta]$$

Wire $\alpha$ shares its value with $x_{\alpha1}$ and $x_{\alpha2}$.
Wire $\beta$ shares its value to $x_{\beta1}$ and $x_{\beta2}$.

为了成功计算MUL门，我们需要一个semi-honest并且不会合谋攻击的第三方生成并秘密共享$(a,b,c)$， 其中 $c=a\cdot b$

Wire $\alpha$ computes $(x_{\alpha1}+a_1)$, $(x_{\beta1}+b_1)$; Wire $\beta$ computes $(x_{\alpha2}+a_2)$, $(x_{\beta2}+b_2)$

执行一次秘密重构，那么双方就均持有 $(x_{\alpha}+a)$ 和  $(x_{\beta}+b)$

Wire $\alpha$ computes $(x_{\alpha}+a)(x_{\beta}+b) + x_{\beta1}(x_{\alpha}+a) + x_{\alpha1}(x_{\beta}+a) + c_1$

Wire $\beta$ computes $x_{\beta2}(x_{\alpha}+a) + x_{\alpha2}(x_{\beta}+a) + c_2$

## 3. BGW Protocol

> Completeness theorems for non-cryptographic fault-tolerant distributed computation, Ben-Or, Goldwasser, and Wigderson, 1988

BGW协议是最先被提出的多方安全计算协议[1]，一些细节信息如下所示：
The BGW protocol can be used to evaluate an **arithmetic circuit over a field $\mathbb{F}$**.

- Addition gates: $[x]+[y]$
- Multiplication gates: $[x]\cdot[y]$
- Multiplication-by-constant gates: $[x]\cdot c$

该协议使用 shamir 秘密共享(Shamir, 1979)，并利用了其某些同态性质。下列公式为 shamir 秘密共享的方式，假设我们想针对秘密 $s$ 进行秘密分享，那么我们令 $a_0:=s$, $a_1\cdots a_t\leftarrow^r\mathbb{Z}_q$

$$p(X)=a_0+a_1X+...+a_{t-1}X^{t-1}\text{ for all }a_i\in\mathbb{Z}_q$$

If we know $t$ points $(x_1,y_1), ...,(x_t,y_t)$, we can build the system on:

$$\begin{bmatrix}1 & x_0 & ... &x_0^{t-1} \\\vdots &\vdots & ... &\vdots \\1 & x_{t-1} &... & x_{t-1}^{t-1}\end{bmatrix}\begin{bmatrix}a_0 \\\vdots \\a_{t-1} \end{bmatrix}=\begin{bmatrix}y_0 \\\vdots \\y_{t-1} \end{bmatrix}\text{ mod }q$$

If the determinant of $X$ is nonzero, we can solve $A=X^{-1}Y$ and find the coefficients of $p(X)$ using Lagrange interpolation.

### ADD Gate

For addition gate, consider input wires $\alpha, \beta$ and output wires $\gamma$. And consider the case we want to secure perform:

$$f_\text{add}([\upsilon_\alpha],[\upsilon_\beta])=[\upsilon_\alpha+\upsilon_\beta]$$

we assume wire $\alpha$ shares its value with $(x_{\alpha1},p_{\alpha}(x_{\alpha1}))$ and $(x_{\alpha2},p_{\alpha}(x_{\alpha2}))$.
Wire $\beta$ shares its value to $(x_{\beta1},p_{\beta}(x_{\beta1}))$ and $(x_{\beta2},p_{\beta}(x_{\beta2}))$.

Then after sharing, wire $\alpha$ has
$$(x_{\alpha1},p_{\alpha}(x_{\alpha1})), (x_{\beta1},p_{\beta}(x_{\beta1}))$$

And wire $\beta$ has
$$(x_{\alpha2},p_{\alpha}(x_{\alpha2})), (x_{\beta2},p_{\beta}(x_{\beta2}))$$

How  about adding them together  as we did in GMW?
Defineing a new polynomial $p_{\gamma}(x)=p_{\alpha}(x)+p_{\beta}(x)$, then we'll find the above result is 

$$(x_{\alpha1}+x_{\beta1},p_{\gamma}(x_{\alpha1}+x_{\beta1}))$$

$$(x_{\alpha2}+x_{\beta2},p_{\gamma}(x_{\alpha2}+x_{\beta2}))$$

which results in a valid polynimial $p_{\gamma}(x)$ and revealing $[\upsilon_\alpha+\upsilon_\beta]$

### MUL Gate

For multiplication gate, consider input wires $\alpha, \beta$ and output wires $\gamma$. And consider the case we want to secure perform:

$$f_\text{mul}([\upsilon_\alpha],[\upsilon_\beta])=[\upsilon_\alpha\times\upsilon_\beta]$$

## 4. BMR Protocol

> D. Beaver,  S. Micali,  and P. Rogaway.  The round complexity of secure protocols.  In22ndSTOC, pages 503–513, 1990.

将 Yao 电路（双方安全计算）扩展成为多方安全计算。Perform a **distributed** GC generation, so that no single party knows the GC gneration secrets - the label assignment and correspondence.

GC generation is *independent* of the depth of the computed circuit $\mathcal{C}$. Therefore, $\mathcal{C}_{GEN}$ is constantly-depth for all compued circuits.

GC evaluation may be delivered to a designated player who will then evaluate it similarly to Yao's GC.

