---
layout: post
title:  "那些密码学基于的数学难题 — Hardness Assumptions"
date:   2019-11-12 12:00:00 +0000
author: Jamie
---

## Integer Factorization

> **Integer factorization** is the decomposition of a [composite number](https://en.wikipedia.org/wiki/Composite_number) into a product of smaller integers. [[wikipedia]](https://en.wikipedia.org/wiki/Integer_factorization#cite_note-rsa768-1)

当我们需要分解的整数足够大的时候，没有有效的、非量子的整数因式分解算法。

我们所了解到的是，因数分解目前还没有多项式时间内的有效解法，通常我们认为不存在PPT解法，因此，因式分解问题通常被认为是NP问题，但是我们无法证明其是 NP-complete 的。研究人员不认为因式分解算法是 NP-complete。

目前最有效解法（GNFS）的时间复杂度，对于一个 $n$ 比特的数字 $n$ 来说:
$$
\text{exp}\left(\left(\sqrt[3]{\frac{64}{9}}+o(1)\right)(\text{ln}\;n)^{\frac{1}{3}}(\text{ln}\;\text{ln}\;n)^{\frac{2}{3}}\right)
$$
对于量子攻击算法 Shor' algorithm （7个qubits）来说的话，解决问题仅仅需要 $O(b^3)$ 时间复杂度以及 $O(b)$ 空间复杂度。

## DL; Discrete Logarithm

> For a suitable cyclic group $G=\langle g\rangle$, take $y\in G$ of order $m$, The **DL** is to find an interger $x\in\mathbb{Z}_m$ such that $g^x=y$.

**No proof that DL is hard**. In general, the number of steps necessary to find a solution is super-polynomial in the size of the group element.

$$\text{DDH}\leq\text{CDH}\leq\text{DL}$$

## CDH; Computation Diffie-Hellman

> Given a cyclic group $G=\langle g\rangle$ of order $m$, $g^a,g^b$ where $a,b\gets\mathbb{Z}_m$, the **CDH** is to compute $g^{ab}$


## DDH; Decisional Diffie-Hellman

> Given a group $G=\langle g\rangle$ of order $m$, $g^a,g^b, g^c$ where $a,b,c\gets\mathbb{Z}_m$, the **DDH** is to decide whether $c=ab$ or $c\gets\mathbb{Z}_m$.

Informally, DDH assumes that it is difficult to distinguish between tuples of the form $\langle g,g^a,g^b,g^c\rangle$, where $g$ belongs to a multiplicative group and $a,b$ and $c$ are randomly chosen exponents.

The group generator **GGen** is said to satisfy the ***decisional Diffie-Hellman assumption*** provided the following probability ensembles $\{\mathcal{D}_\lambda\}_{\lambda\in\mathbb{N}}$ and $\{\mathcal{R}_\lambda\}_{\lambda\in\mathbb{N}}$ are computationally indistinguishable:
$$
\mathcal{D}_\lambda:=\{\langle G,m,g\rangle\gets \text{GGen}(1^\lambda);a,b\gets \mathbb{Z}_m:(G,m,g,g^a,g^b,g^{ab})\}
$$

$$
\mathcal{R}_\lambda:=\{\langle G,m,g\rangle\gets \text{GGen}(1^\lambda);a,b,c\gets \mathbb{Z}_m:(G,m,g,g^a,g^b,g^{c})\}
$$

where $m=\text{order}(g)$.

Equivalently, if $\mathcal{A}$ is a statistical test bounded by probabilistic polynomial-time, it holds that
$$
\text{Adv}^{\mathcal{A}}(1^\lambda)=\Delta_\mathcal{A}[\mathcal{D}_\lambda, \mathcal{R}_\lambda]\leq\text{negl}(1^\lambda)
$$
$\text{Adv}^{\mathcal{A}}$ is called the **advantage** of $\mathcal{A}$.

## ECDLP; Elliptic Curve Discrete Logarithm Problem

>  Let $E$ be an elliptic curve over a finite field $\mathbb{F}_q$, where $q=p^n$ and $p$ is prime.  Given points $P,Q\in E(\mathbb{F}_q) $ to find an integer $a$, if it exists, such that $Q=aP$.

椭圆曲线是有限域上的平面曲线，满足下列方程：
$$
y^2=x^3+ax+b
$$
椭圆曲线以及椭圆曲线上定义的加法以及乘法构成了一个 Abelian group。

## SVP; Shortest Vector Problem

> For a real number $p ≥ 1$, the p-norm or $L^p$-norm of $x$ is defined by $\|x\|_p=(\|x_1\|^p+\|x_2\|^p+...+\|x_n\|^p)^{1/p}$

Assume we are given with a basis in vector space $V$ and a norm $N$ (Ususally L2-norm). Let $\lambda(L)$ be the length of shorted non-zero vector in the lattice $L$, that is,
$$
\lambda (L)=\min_{v\in L\setminus \{\mathbf {0} \}}\|v\|_{N}
$$

## RLWE; Ring Learning with Errors

> An important feature  is  that the solution to the RLWE problem may be  reducible to the [NP-hard](https://en.wikipedia.org/wiki/NP-hard) [shortest vector problem](https://en.wikipedia.org/wiki/Shortest_vector_problem) (SVP) in a lattice.[[1\]](https://en.wikipedia.org/wiki/Ring_learning_with_errors#cite_note-:0-1)

RLWE问题给予在有限域内的多项式问题，首先，多项式的定义为：
$$
a(x)=a_0+a_1x+a_2x^2+...+a_{n-2}x^{n-2} + a_{n-1}x^{n-1}
$$
多项式可以进行数字运算，多项式的相加或者相乘可以通过参数进行相应运算来实现（可以参考MPC中的BGW协议），即
$$
a(x)\cdot b(x)\quad a(x)+b(x)
$$
In the RLWE context the coefficients of the polynomials and all operations involving those coefficients will be done in a finite field, typically the field $$\mathbf{Z}/q\mathbf{Z} = \mathbf{F}_q$$ for a prime integer $q$.  

The set of polynomials over a finite field with the operations of addition and multiplication forms an infinite polynomial ring ($\mathbf{F}_q[x]$).  

The RLWE context works with a finite quotient ring of this infinite ring.  

The quotient ring is typically the finite Quotient ring/quotient (factor) ring formed by reducing all of the polynomials in $\mathbf{F}_q[x]$ modulo an irreducible polynomial $\Phi(x)$.  This finite quotient ring can be written as $\mathbf{F}_q[x]/\Phi(x)$ though many authors write $\mathbf{Z}_q[x]/\Phi(x)$