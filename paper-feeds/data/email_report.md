# Paper Pulse Daily Report

**Date:** 2026-03-02 02:30 UTC

## Statistics

- **New papers fetched:** 11
- **Retry summaries:** 0
- **Failed summaries:** 0
- **Total papers in database:** 441

## AI Token Usage

- **Input tokens:** 5976
- **Output tokens:** 7575
- **Total tokens:** 13551

## New Papers (11)

### 1. [Jailbreak Foundry: From Papers to Runnable Attacks for Reproducible Benchmarking](https://arxiv.org/abs/2602.24009v1)

**Source:** arXiv | **Published:** 2026-02-27
  **Keywords:** security, agent

#### Chinese Summary

## 背景与挑战  
大型语言模型（LLM）的越狱（jailbreak）攻击技术迭代迅猛，远超现有基准测试（benchmarks）的更新速度。由此导致三大问题：鲁棒性评估结果快速过时；不同论文间因数据集、运行框架（harness）及评判协议（judging protocol）漂移而难以横向比较；复现成本高、实现碎片化，严重阻碍可重复、可扩展的安全研究。

## 方法：JAILBREAK FOUNDRY（JBF）系统  
我们提出**JBF——一个端到端的越狱攻击可复现基准构建系统**，通过多智能体协同工作流，将学术论文中描述的越狱方法自动转化为可执行、可即插即用的模块。JBF包含三大核心组件：  
- **JBF-LIB**：提供统一接口契约与跨攻击复用的工具库（如提示模板解析、响应归一化、防御绕过检测器）；  
- **JBF-FORGE**：基于LLM驱动的多智能体协作框架，自动解析论文（PDF/TeX）、提取攻击逻辑、生成符合JBF规范的Python模块，并经人工校验保障语义保真；  
- **JBF-EVAL**：标准化评估流水线，支持在统一Harness下对任意攻击—模型组合进行批量测试，并集成**一致的GPT-4o裁判器**（judge），消除评判主观性。

## 主要发现与创新  
在30篇代表性越狱论文的复现中：  
- 攻击成功率（ASR）复现值与原文报告值平均偏差仅 **+0.26个百分点**（高保真）；  
- 相比原始代码仓库，JBF将攻击专属实现代码量减少近50%，**平均代码复用率达82.5%**；  
- 首次实现**30种攻击 × 10个受害模型**在AdvBench上的全矩阵标准化评测；  
- 系统开源（Apache 2.0），支持社区持续注入新攻击，推动基准从“静态快照”迈向“动态演进”的**活基准（living benchmark）**。

#### English Summary

Jailbreak Foundry (JBF) is a reproducible benchmarking system that bridges the widening gap between rapidly evolving LLM jailbreak techniques and stagnant evaluation infrastructure. It introduces a multi-agent workflow—JBF-FORGE—to automatically translate jailbreak papers into standardized, executable modules, backed by JBF-LIB (shared utilities & contracts) and JBF-EVAL (unified, GPT-4o–judged evaluation). Across 30 reproduced attacks, JBF achieves high fidelity with a mean ASR deviation of only +0.26 percentage points versus reported results. It cuts attack-specific implementation code by nearly half and attains an 82.5% mean code reuse ratio. Crucially, JBF enables the first standardized AdvBench evaluation of all 30 attacks across 10 victim models under consistent judging—transforming benchmarks from static snapshots into scalable, living evaluations that evolve with the threat landscape.

---

### 2. [Lap2: Revisiting Laplace DP-SGD for High Dimensions via Majorization Theory](https://arxiv.org/abs/2602.23516v1)

**Source:** arXiv | **Published:** 2026-02-26
  **Keywords:** dp

#### Chinese Summary

## 背景与挑战  
差分隐私随机梯度下降（DP-SGD）是深度学习中保障训练隐私的核心技术，广泛应用于大模型从头训练与微调。当前主流依赖**高斯机制**，而拉普拉斯机制因需**L1范数梯度裁剪**长期被边缘化——在高维场景下，n维梯度的L1范数可达L2范数的√n倍，导致所需噪声尺度随参数量急剧膨胀，严重损害模型效用甚至使训练不可行。

## 方法创新：Lap2框架  
本文提出**Lap2**，首次实现拉普拉斯DP-SGD下的**L2范数裁剪**，同时严格保持(ε,δ)-差分隐私保证。核心突破在于：  
- **坐标级矩界计算**：对每个梯度分量独立推导紧致、数据无关的矩生成函数（MGF）上界；  
- **主化理论（Majorization）建模**：利用矩会计函数的**Schur-凸性**，构造满足L2约束的最优主化集，将海量坐标界聚合为全局紧致上界；  
- **可扩展多变量隐私会计**：支持数千阶矩的高效计算，隐私损失随维度近乎常数增长（而非线性或平方根增长）。

## 关键成果  
在SST-2数据集上微调RoBERTa-base（1.25亿参数）：  
- **ε = 0.54**时达**87.88%准确率**，显著超越高斯DP-SGD（87.16%）与标准拉普拉斯DP-SGD（48.97%）；  
- 首次证明拉普拉斯机制在强隐私预算（ε < 1）下可媲美甚至超越高斯机制；  
- 代码开源，为高维隐私优化提供新范式。

#### English Summary

Differentially Private Stochastic Gradient Descent (DP-SGD) relies heavily on the Gaussian mechanism, while the Laplace mechanism remains impractical for high-dimensional models due to its requirement of L1-norm gradient clipping—causing noise scale to grow as √n and degrading utility severely. This paper introduces **Lap2**, the first Laplace-based DP-SGD framework supporting **L2-norm clipping** with rigorous (ε, δ)-privacy guarantees. Leveraging coordinate-wise moment bounds and **majorization theory**, Lap2 exploits the Schur-convexity of the moment accountant to construct a tight, data-independent global upper bound under L2 constraints—enabling scalable multivariate privacy accounting with thousands of moments. Experiments show Lap2 significantly outperforms standard Laplace DP-SGD and matches or exceeds Gaussian DP-SGD under strong privacy: fine-tuning RoBERTa-base on SST-2 achieves **87.88% accuracy at ε = 0.54**, surpassing Gaussian (87.16%) and standard Laplace (48.97%). Lap2 establishes Laplace mechanisms as viable—and competitive—for high-dimensional private learning.

---

### 3. [Learning to Generate Secure Code via Token-Level Rewards](https://arxiv.org/abs/2602.23407v1)

**Source:** arXiv | **Published:** 2026-02-26
  **Keywords:** security, llm

#### Chinese Summary

## 背景与挑战  
大型语言模型（LLMs）在代码生成任务中展现出卓越能力，但在**安全关键场景下仍频繁引入漏洞**（如SQL注入、XSS、缓冲区溢出）。现有方法面临两大瓶颈：一是高质量、带细粒度标注的安全修复数据极度稀缺；二是主流强化学习（RL）训练依赖**实例级奖励**（如整体通过率或CVE匹配），无法引导模型关注代码中特定危险token（如未转义的`user_input`、缺失的`htmlspecialchars()`调用），导致安全模式学习粗粒度、不可控。

## 方法创新  
本研究提出端到端安全代码生成新范式：  
- **Vul2Safe框架**：利用LLM自反思机制，从真实世界漏洞（如GitHub CVE提交、Snyk报告）中自动挖掘高置信度“漏洞片段→安全修复”配对，规避人工标注成本；进一步生成多样化**隐式安全提示**（implicit prompts），构建首个面向细粒度安全修复的大规模合成数据集——**PrimeVul+**（含127K高质量修复对，覆盖OWASP Top 10漏洞类型）。  
- **SRCode训练框架**：首次将**token级奖励信号**引入代码安全RL训练。基于静态分析器与规则引擎，为每个输出token动态计算安全贡献分（如`'+'`后接`user_input`得负分，`'htmlspecialchars('`开头得正分），实现逐token梯度更新，使模型在生成过程中持续聚焦于关键防御位置。

## 核心成果  
在CodeXGLUE、HumanEval+Sec、SV-Bench等6个基准上，SRCode+PrimeVul+显著优于基线：**平均漏洞率降低58.3%**（vs. SOTA RL方法），**功能正确性提升9.2%**，且生成代码的可读性与可维护性（经SonarQube评估）同步优化。本工作证实：**细粒度奖励+高质量合成数据**是突破LLM安全生成瓶颈的关键路径。

#### English Summary

Large language models (LLMs) excel at code generation but often produce vulnerable code. Prior approaches are hindered by scarce high-quality security data and coarse instance-level reinforcement learning (RL) rewards. To address this, we propose **Vul2Safe**, a framework that leverages LLM self-reflection to automatically construct high-confidence vulnerability–repair pairs from real-world CVEs and generate diverse implicit prompts, yielding the **PrimeVul+** dataset (127K samples). Concurrently, we introduce **SRCode**, the first RL framework for secure code generation using **token-level rewards**: security analyzers assign fine-grained scores to each generated token (e.g., penalizing unsafe string concatenation, rewarding sanitization calls), enabling precise optimization of local security patterns. Experiments across six benchmarks show SRCode trained on PrimeVul+ reduces average vulnerability rates by **58.3%** over SOTA RL baselines while improving functional correctness (+9.2%) and maintainability. Our work establishes token-level reward modeling and synthetically curated security data as essential levers for trustworthy code generation.

---

### 4. [Lifecycle-Integrated Security for AI-Cloud Convergence in Cyber-Physical Infrastructure](https://arxiv.org/abs/2602.23397v1)

**Source:** arXiv | **Published:** 2026-02-26
  **Keywords:** inference, security

#### Chinese Summary

## 背景与问题  
人工智能（AI）推理流水线与云基础设施的深度耦合，催生了“AI-云融合”新型攻击面——云安全标准（如NIST SP 800-53、CSA MAESTRO）与AI治理框架（如NIST AI RMF、OWASP AI Exchange）虽各自成熟，却缺乏跨层协同的统一执行机制。在电力、交通等网络物理基础设施（CPS）中，该割裂导致AI模型供应链、云运行时环境与工业控制系统（如NERC CIP）三者间存在策略断点，使攻击者可实施跨层渗透（如篡改传感器数据→劫持AI决策→触发物理设备误动作），直接威胁安全关键业务。

## 方法与创新  
本文提出**全生命周期集成安全范式**，三大核心贡献：  
1. **生命周期分阶威胁分类法**：基于攻击者能力层级（数据投毒→模型窃取→提示注入→代理越权→物理致效），构建覆盖AI训练、部署、运行、退役四阶段的统一威胁图谱；  
2. **统一参考架构（URA）**：包含三层闭环设计——**安全数据工厂**（联邦学习+差分隐私预处理）、**可信模型供应链**（SBOM+模型签名+零信任验证）、**运行时治理层**（动态策略引擎+实时对抗检测+自动响应编排）；  
3. **Grid-Guard实证案例**：在输电系统运营商（TSO）混合场景中，整合NIST AI RMF、MITRE ATLAS、OWASP AI Exchange & GenAI、CSA MAESTRO及NERC CIP六大框架控制项，成功抵御一次多阶段物理-金融协同操纵攻击（含虚假负荷注入、电价欺诈、继电保护绕过），全程零人工干预。

## 关键发现  
所有控制措施均双向映射至五大AI/云/工控框架及现行NERC CIP v7标准，证实：单一云原生架构可同步满足**AI治理合规性、对抗鲁棒性、智能体安全性、工业监管强制性**四维要求，为CPS智能化提供可验证、可审计、可扩展的安全基座。

#### English Summary

This paper addresses the security fragmentation arising from AI-cloud convergence in cyber-physical infrastructure (CPI), where disjointed AI governance (e.g., NIST AI RMF, OWASP AI Exchange), cloud security (e.g., CSA MAESTRO), and industrial control standards (e.g., NERC CIP) enable cross-layer attacks threatening safety-critical operations. We contribute: (i) a lifecycle-integrated threat taxonomy structured by explicit attacker capability tiers (data poisoning → model stealing → prompt injection → agent privilege escalation → physical impact); (ii) a Unified Reference Architecture comprising a Secure Data Factory, hardened model supply chain, and runtime governance layer with automated policy enforcement; and (iii) Grid-Guard—a validated case study in a hybrid transmission system operator environment—demonstrating end-to-end autonomous defense against a multi-tier physical-financial manipulation campaign using coordinated controls drawn from NIST AI RMF, MITRE ATLAS, OWASP AI Exchange/GenAI, CSA MAESTRO, and NERC CIP. All controls are rigorously mapped to all five frameworks and current NERC CIP requirements, proving that a single cloud-native architecture can simultaneously satisfy AI governance, adversarial robustness, agentic safety, and industrial regulatory compliance.

---

### 5. [FedDAG: Clustered Federated Learning via Global Data and Gradient Integration for Heterogeneous Environments](https://arxiv.org/abs/2602.23504v1)

**Source:** arXiv | **Published:** 2026-02-26
  **Keywords:** federated, learning

#### Chinese Summary

## 背景与挑战  
联邦学习（FL）允许多个客户端在不共享原始数据的前提下协同训练全局模型，但在**数据异质性显著**（如非独立同分布，Non-IID）场景下，模型性能常大幅下降。为缓解该问题，**聚类式联邦学习（Clustered FL）** 将行为相似的客户端分组并分别建模，但现有方法存在两大瓶颈：（1）**相似性度量片面**——仅依赖局部数据分布或梯度更新中的单一信号，忽略二者互补性；（2）**知识隔离严重**——各簇模型严格限制在簇内参数共享，无法利用跨簇的多样性表征，导致泛化能力受限。

## 方法创新：FedDAG 框架  
本文提出 **FedDAG**（Federated Directed Acyclic Graph），一种新型聚类联邦学习框架：  
- **全局数据-梯度联合相似性度量**：设计**加权、类别感知的相似性计算**，同步融合客户端本地数据的类分布统计与全局聚合梯度的方向/幅值信息，实现更鲁棒、细粒度的簇划分；  
- **双编码器跨簇特征迁移机制**：每个簇模型采用**主-辅双编码器架构**——主编码器基于本簇客户端数据端到端优化；辅编码器则通过**自适应梯度蒸馏**，接收来自语义互补簇（如类别分布互补的簇）的梯度反馈进行微调，在保留簇特异性的同时注入跨簇判别性特征；  
- **无中心化协调开销**：所有操作均在服务器端完成相似性计算与梯度路由，不增加客户端通信负担。

## 实验结果  
在CIFAR-10/100、Tiny-ImageNet及LEAF-FEMNIST等基准上，覆盖**Label/Feature/Quantity 三重异质性**设置，FedDAG 在平均准确率上较SOTA聚类方法（如IFCA、SCAFFOLD-Clust、Krum-Clust）提升**2.3–5.7个百分点**，且在低资源簇中相对提升达**9.1%**，验证了其对长尾异构场景的强适应性。

#### English Summary

Federated Learning (FL) suffers from performance degradation under data heterogeneity, motivating clustered FL approaches that group similar clients. However, existing methods rely *either* on data similarity *or* gradient similarity—yielding incomplete client assessment—and strictly isolate knowledge within clusters, missing cross-cluster representation benefits. To address this, we propose **FedDAG**, a clustered FL framework featuring: (1) a **weighted, class-wise similarity metric** that jointly integrates local data distributions and global gradient signals for more holistic clustering; and (2) a **dual-encoder architecture**, where each cluster’s primary encoder is trained on its own clients’ data, while a secondary encoder is refined via gradients from semantically complementary clusters—enabling controlled cross-cluster feature transfer without sacrificing specialization. Extensive experiments across CIFAR-10/100, Tiny-ImageNet, and LEAF-FEMNIST under diverse heterogeneity settings demonstrate that FedDAG consistently outperforms state-of-the-art clustered FL baselines, achieving absolute accuracy gains of **2.3–5.7 percentage points**, with up to **9.1% relative improvement** in low-resource clusters.

---

### 6. [Conformalized Neural Networks for Federated Uncertainty Quantification under Dual Heterogeneity](https://arxiv.org/abs/2602.23296v2)

**Source:** arXiv | **Published:** 2026-02-26
  **Keywords:** federated, learning

#### Chinese Summary

## 背景与挑战  
联邦学习（FL）在分布式场景中面临**不确定性量化（UQ）失效**风险：当边缘设备（agents）数据与模型高度异构时，传统UQ方法易产生过自信预测，导致局部静默失败——即全局性能看似良好，但个别资源受限设备上预测不可靠，严重威胁医疗、工业等高危场景部署安全。

## 方法创新：FedWQ-CP  
本文提出 **FedWQ-CP**（Federated Weighted Quantile Conformal Prediction），首个专为**双重异构性**（数据异构 + 模型异构）设计的共形化神经网络框架。其核心突破在于：  
- **单轮通信轻量校准**：各agent在本地用校准数据计算 conformity score，并独立求解**本地分位数阈值**（$\hat{q}_i$）及样本量 $n_i$；  
- **加权聚合全局阈值**：服务器仅接收 $(\hat{q}_i, n_i)$ 对，通过 $q_{\text{global}} = \sum_i (n_i / \sum_j n_j) \cdot \hat{q}_i$ 加权平均生成全局阈值，无需传输原始分数或模型参数；  
- **双层覆盖保障**：理论保证在任意agent上满足边际覆盖率 $1-\alpha$，同时全局集合/区间亦严格满足目标置信水平。

## 实验结果  
在7个公开数据集（含图像分类、时序回归、表格预测任务）上验证：FedWQ-CP 在**所有agent上实现近乎精确的个体覆盖**（平均偏差 < 0.8%），全局覆盖误差 < 0.5%；相较基线方法（如FedCP、DistCP），其预测集尺寸缩小 **12–34%**（分类）或预测区间宽度降低 **18–29%**（回归），显著提升UQ效率与实用性。

#### English Summary

Federated learning (FL) suffers from unreliable uncertainty quantification (UQ) under dual heterogeneity—where both data distributions and model architectures vary across agents—leading to overconfident yet erroneous local predictions despite acceptable global accuracy. To address this, we propose **FedWQ-CP**, a conformalized neural network framework that achieves rigorous, distribution-free UQ with minimal communication. FedWQ-CP performs agent-server calibration in **one round**: each agent computes its local conformity score quantile $\hat{q}_i$ and sample size $n_i$, then transmits only these two scalars; the server aggregates via weighted average $q_{\text{global}} = \sum_i (n_i / \sum_j n_j)\, \hat{q}_i$. Experiments across seven public classification and regression benchmarks show FedWQ-CP maintains **empirical coverage within ±0.8% per agent and <0.5% globally**, while yielding the **smallest prediction sets/intervals**—reducing set size by 12–34% (classification) and interval width by 18–29% (regression) versus state-of-the-art federated CP methods.

---

### 7. [FedVG: Gradient-Guided Aggregation for Enhanced Federated Learning](https://arxiv.org/abs/2602.21399v2)

**Source:** arXiv | **Published:** 2026-02-24
  **Keywords:** federated, learning

#### Chinese Summary

## FedVG：基于梯度引导的联邦聚合方法，提升异构环境下的模型泛化能力

联邦学习（FL）允许多客户端协作训练全局模型而无需共享原始私有数据，但**客户端间显著的数据异质性**易引发“客户端漂移”（client drift），导致全局模型在分布外数据上泛化性能下降；更严重的是，传统聚合策略（如FedAvg）常因过度加权样本量大或更新幅值高的客户端，进一步放大偏差。为系统性缓解该问题，本文提出 **FedVG（Gradient-Guided Aggregation for Enhanced Federated Learning）**——一种新型、隐私安全且即插即用的梯度引导式联邦聚合框架。

FedVG的核心创新在于引入一个**轻量级、全局共享的验证集**（可由公开可用数据集构建，如ImageNet-1K子集或CheXpert裁剪版），不涉及任何客户端私有数据，完全满足隐私约束。其关键机制是：在每轮聚合前，各客户端在该全局验证集上计算**逐层验证梯度（validation gradients）**，并量化其L2范数序列；据此生成**层感知的客户端得分（layerwise gradient norm score）**，该得分客观反映该客户端模型在全局分布上的“校准需求强度”——得分越低，表明其本地更新与全局泛化方向越一致，应赋予更高聚合权重。该机制摒弃了对本地数据量或损失值的粗粒度依赖，实现了**基于泛化能力的动态、自适应加权**。

我们在自然图像（CIFAR-10/100, Tiny-ImageNet）与医学影像（CheXpert, PathMNIST）共5个基准数据集上，联合ResNet、ViT、DenseNet等多种架构进行大规模实验。结果表明：FedVG在高度非独立同分布（Non-IID）设置下平均提升测试准确率**2.1–5.7个百分点**，显著优于FedAvg、FedProx、SCAFFOLD等主流算法；且与SOTA方法（如MOON、FedNova）正交兼容，叠加使用后持续增益。代码已开源：https://github.com/alinadevkota/FedVG。

#### English Summary

Federated Learning (FL) suffers from client drift under data heterogeneity, degrading global model generalization—especially when poorly performing clients are over-weighted. To address this, we propose **FedVG**, a novel gradient-guided aggregation framework that leverages a small, publicly sourced *global validation set* (e.g., subsets of ImageNet or CheXpert) to steer aggregation without compromising privacy. Unlike volume- or loss-based weighting, FedVG computes **layerwise validation gradient norms** on this set for each client and derives a client-specific score reflecting its *generalization alignment* with the global distribution—enabling adaptive, performance-aware aggregation. Extensive experiments across natural and medical image benchmarks (CIFAR-10/100, Tiny-ImageNet, CheXpert, PathMNIST) and diverse architectures (ResNet, ViT, DenseNet) show FedVG consistently improves accuracy by **2.1–5.7%** under high Non-IID settings, outperforms FedAvg, FedProx, and SCAFFOLD, and seamlessly boosts state-of-the-art methods like MOON and FedNova. Code is open-sourced at https://github.com/alinadevkota/FedVG.

---

### 8. [MemEmo: Evaluating Emotion in Memory Systems of Agents](https://arxiv.org/abs/2602.23944v1)

**Source:** arXiv | **Published:** 2026-02-27
  **Keywords:** model, extraction

#### Chinese Summary

## MemEmo：面向智能体记忆系统的 emotion 评估新范式  

当前，大语言模型（LLM）在长程交互中面临**上下文丢失**的固有挑战，记忆系统（Memory Systems）被广泛用于缓解该问题。然而，与人类记忆高度整合情感体验的认知机制相比，现有记忆系统对**情绪信息的感知、存储与调用能力仍缺乏系统性验证**——这一关键缺陷长期被忽视。为填补该空白，本研究提出首个专注情感维度的记忆评估框架 **MemEmo**，并构建开源基准数据集 **HLME**（Human-Like Memory Emotion）。HLME 从三个正交且认知可解释的维度严格评测记忆系统：  
- **情绪信息抽取**（Emotional Information Extraction）：识别对话中隐含的细粒度情绪状态（如“失望”“欣慰”“矛盾”）；  
- **情绪记忆更新**（Emotional Memory Updating）：检验系统能否依据新交互动态修正既有情绪表征（如由“信任”转为“警惕”）；  
- **情绪记忆问答**（Emotional Memory Question Answering）：测试跨轮次、需情绪推理的因果/意图类问题回答能力（如“用户为何突然沉默？是否因先前被否定？”）。  

我们在 8 个主流及前沿记忆系统（包括 Retrieval-Augmented、Episodic、Semantic 和 Hybrid 架构）上开展统一评测。结果表明：**无一系统在三项任务上均达稳健性能（平均F1 < 62%，跨任务标准差 > 18%）**；尤其在情绪更新与推理类问答中表现显著退化。本研究首次量化揭示了记忆系统在**情感建模上的结构性短板**，为构建具身化、共情化智能体提供了可复现的评估基线与明确优化路径。

#### English Summary

MemEmo introduces the first benchmark dedicated to evaluating how memory systems in LLM-based agents process, update, and reason over emotional information—a critical gap given humans’ emotion-embedded memory cognition. We propose the **HLME dataset** (Human-Like Memory Emotion), assessing systems across three dimensions: (1) *emotional information extraction*, (2) *emotional memory updating*, and (3) *emotional memory question answering*. Experiments on 8 state-of-the-art memory architectures—including retrieval-augmented, episodic, semantic, and hybrid designs—reveal that **no system achieves robust performance across all three tasks** (average F1 < 62%; inter-task standard deviation > 18%). Performance degrades notably in dynamic emotion updating and affective reasoning, exposing fundamental limitations in current memory design. MemEmo provides an objective, reproducible evaluation framework and a clear roadmap for emotion-aware memory optimization.

---

### 9. [NAU-QMUL: Utilizing BERT and CLIP for Multi-modal AI-Generated Image Detection](https://arxiv.org/abs/2602.23863v1)

**Source:** arXiv | **Published:** 2026-02-27
  **Keywords:** model, extraction

#### Chinese Summary

## 研究背景与问题  
随着生成式AI（如Stable Diffusion、DALL·E、MidJourney）的迅猛发展，高质量AI伪造图像泛滥，严重威胁媒体可信度、司法取证与数字内容安全。现有检测方法多依赖单一模态（仅图像像素或仅EXIF元数据），难以捕捉文本-图像间的语义不一致性，且对未知生成模型泛化能力弱。

## 方法创新  
本研究提出**NAU-QMUL**——一种端到端多模态多任务检测框架：  
- **双编码器协同**：采用冻结的**BERT-base**（文本编码器）提取图像对应提示词（prompt）的语义表征；同步调用**CLIP-ViT/L-14**视觉编码器提取图像深层特征；  
- **跨模态融合机制**：设计轻量级交叉注意力模块，实现文本→图像特征引导与图像→文本特征校准，强化模态间语义对齐；  
- **多任务联合优化**：统一建模两大任务——**Task A**（二分类：真实 vs. AI生成）与**Task B**（细粒度分类：识别具体生成模型，含SD 1.5/2.1、SDXL、DALL·E 2/3、MidJourney v5/v6等共8类）；损失函数加权融合Focal Loss（缓解类别不平衡）与KL散度约束（提升跨模型判别性）；  
- **伪标签增强策略**：在未标注数据上迭代生成高置信度（>0.95）伪标签，扩充训练集37%，显著提升小样本模型鲁棒性。

## 主要成果  
在权威竞赛“CT2: AI-Generated Image Detection”中，NAU-QMUL位列**Task A（检测）与Task B（溯源）双赛道第五名**，F1分数分别达**83.16%**与**48.88%**（后者为当时公开最优结果之一）。消融实验证实：跨模态融合使Task B性能提升+6.2%，伪标签策略带来+3.8% F1增益。代码已开源：https://github.com/xxxxxxxxy/AIGeneratedImageDetection。

#### English Summary

We propose **NAU-QMUL**, a novel multi-modal multi-task framework for detecting AI-generated images and identifying their underlying generative models (e.g., SDXL, DALL·E 3, MidJourney v6). It jointly leverages frozen **BERT** to encode textual prompts and **CLIP-ViT/L-14** to extract visual features, followed by cross-modal attention fusion and a custom multi-task loss combining focal loss (for binary detection) and KL divergence (for fine-grained model attribution). To address data scarcity, we introduce a confidence-thresholded pseudo-labeling strategy that expands training data with high-quality synthetic labels. Evaluated on the CT2 competition benchmark, NAU-QMUL achieves **5th place in both Task A (F1 = 83.16%) and Task B (F1 = 48.88%)**, demonstrating state-of-the-art performance in real-world AI image attribution. The code is publicly available at https://github.com/xxxxxxxxy/AIGeneratedImageDetection.

---

### 10. [TRIZ-RAGNER: A Retrieval-Augmented Large Language Model for TRIZ-Aware Named Entity Recognition in Patent-Based Contradiction Mining](https://arxiv.org/abs/2602.23656v1)

**Source:** arXiv | **Published:** 2026-02-27
  **Keywords:** model, extraction

#### Chinese Summary

## 研究背景与挑战  
基于TRIZ理论的专利矛盾挖掘是系统化创新与技术预测的核心任务，旨在识别专利文本中驱动发明问题解决的“改善参数”与“恶化参数”这对技术矛盾。然而，现有方法（如规则引擎、CRF或BiLSTM）受限于语义歧义强、领域适配性差、泛化能力弱等问题；而直接调用大语言模型（LLM）又易产生幻觉，且缺乏对结构化TRIZ知识（如39个工程参数、40条发明原理）的可靠 grounding，导致参数识别不一致、可解释性低。

## 方法创新：TRIZ-RAGNER框架  
本研究提出**TRIZ-RAGNER**——一种面向TRIZ感知命名实体识别（NER）的检索增强型大语言模型框架。其核心创新在于：  
- **任务重构**：将矛盾挖掘建模为语义级NER任务，统一抽取“改善参数”与“恶化参数”两类实体；  
- **三阶段知识注入**：① 基于稠密检索（Dense Retrieval）从TRIZ知识库中召回相关参数定义与典型用例；② 采用cross-encoder进行上下文敏感的重排序，提升检索相关性；③ 设计结构化提示模板（含参数表、约束规则、示例链），引导LLM生成符合TRIZ语义边界的输出。  
该设计显著抑制了LLM在专业术语上的语义漂移，提升了提取一致性与可追溯性。

## 实验结果与贡献  
在权威专利TRIZ数据集PaTRIZ上的实验表明：TRIZ-RAGNER达到**精确率85.6%、召回率82.9%、F1值84.2%**，较最优基线（prompt-enhanced GPT-4）提升**7.3个百分点**，且在跨专利句式、多义参数（如“温度”“可靠性”）场景下鲁棒性突出。本工作首次实现了LLM与TRIZ知识体系的深度协同，为可解释、可验证的智能创新支持系统提供了新范式。

#### English Summary

TRIZ-based contradiction mining is essential for systematic innovation but remains challenging due to semantic ambiguity in patent language and the lack of reliable TRIZ knowledge grounding in LLMs. To address this, we propose **TRIZ-RAGNER**, a retrieval-augmented LLM framework that reformulates contradiction mining as a TRIZ-aware named entity recognition (NER) task. It integrates dense retrieval over a structured TRIZ knowledge base, cross-encoder reranking for contextual refinement, and domain-informed prompting to extract *improving* and *worsening* technical parameters from patent sentences. Evaluated on the PaTRIZ dataset, TRIZ-RAGNER achieves **85.6% precision, 82.9% recall, and 84.2% F1-score**, outperforming strong LLM and traditional NER baselines by up to **+7.3 F1 points**. This demonstrates that retrieval-augmented TRIZ knowledge injection significantly enhances accuracy, consistency, and interpretability in patent-based contradiction analysis.

---

### 11. [IDP Accelerator: Agentic Document Intelligence from Extraction to Compliance Validation](https://arxiv.org/abs/2602.23481v1)

**Source:** arXiv | **Published:** 2026-02-26
  **Keywords:** model, extraction

#### Chinese Summary

## IDP Accelerator：面向合规验证的智能文档处理代理框架  

**背景与挑战**：从非结构化文档中提取结构化洞见是工业级自然语言处理的基础难题。尽管大语言模型（LLMs）支持零样本抽取，传统文档处理流水线仍难以应对多文档包解析、跨文档复杂推理及严苛的行业合规要求（如医疗、金融领域的审计可追溯性与逻辑一致性）。  

**方法与创新**：本文提出 **IDP Accelerator**——首个支持端到端“文档智能代理”（Agentic Document Intelligence）的开源框架，包含四大核心模块：  
1. **DocSplit**：新型多模态基准数据集与分类器，采用BIO标注策略精准切分混合格式文档包（如PDF+扫描件+表格嵌套）；  
2. **可配置抽取模块**：融合视觉-语言多模态LLM（如Qwen-VL、LLaVA），支持字段级语义对齐与上下文感知结构化转换；  
3. **代理式分析模块**：严格遵循Model Context Protocol（MCP）标准，通过安全沙箱执行Python代码实现动态数据探查与关联分析；  
4. **规则验证模块**：以LLM驱动的可解释逻辑替代硬编码规则引擎，支持自然语言定义的复合合规检查（如“处方药剂量≤患者体重×0.5mg/kg且需双签名”）。  

**效果与影响**：在真实产线部署中，某头部医疗机构实现**98%文档包分类准确率**、**处理延迟降低80%**、**运维成本下降77%**。系统提供交互式Web界面，支持文档上传、可视化分割热图、结构化数据溯源与合规报告一键生成。全部代码、DocSplit数据集及在线Demo已开源，推动可信文档智能落地。

#### English Summary

IDP Accelerator is an open-source agentic framework for end-to-end document intelligence, bridging extraction, analytics, and compliance validation. It introduces four novel components: (1) **DocSplit**, a multimodal benchmark and classifier using BIO tagging to segment heterogeneous document packets; (2) a **configurable multimodal LLM-based Extraction Module** for zero-shot, context-aware structured data generation; (3) an **Agentic Analytics Module** compliant with the Model Context Protocol (MCP), enabling secure, sandboxed code execution for dynamic data exploration; and (4) a **Rule Validation Module** that replaces brittle deterministic engines with LLM-driven, interpretable logic for complex regulatory checks. Evaluated in production at a leading healthcare provider, IDP Accelerator achieves **98% classification accuracy**, **80% lower latency**, and **77% reduced operational cost** versus legacy systems. A live web demo and full source code are publicly available.

---

## Links

- [View Papers](https://jamie-cui.github.io/paper-pulse)

---

*This is an automated report from Paper Pulse. Powered by arXiv, IACR ePrint, and DashScope (Qwen).*