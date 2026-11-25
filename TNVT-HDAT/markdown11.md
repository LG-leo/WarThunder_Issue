> 首先，我明显的注意到了，KD在战雷的来源是先手+遇敌+技术本身，而很多时候往往死的时候，敌人是“先手”，那么先手是杠杆最高的优化目标

> 那么优化先手，当时我想到的是移动行为逻辑这一条

> 那么移动行为可以很明确的解决先手+遇敌本身的问题。

> 毕竟我也懒，不愿意背地图，也懒得记敌人大概什么时候出现这件事。

> 紧接着，当时我想到一个很好的比方就是，把K+D叫做总有效密钥量，K叫做有效，D叫做无效，其他叫做=没触发，那么把全局当作一组黑箱随机数即可。

那么整一个游戏对局是：

{0001}{0302}{ID1022-0213431323113}{ID0001-0232392903113}...

地图-第三号雨天-一个玩家的具体编号-另一个玩家的编号...

而每个玩家，都会被记录在每一个区块的某一个部分作为该载具的”中心点“，每个玩家发现另一个玩家的时候，另一个玩家就会有概率被“发现及摧毁”。每一个玩家我们假设只能看见正前方向左45度向右45度，那么在他正右方的敌人就发现不了，因此，该玩家的载具就会被摧毁。

而因为有渲染距离，渲染质量（屏幕），服务器发的信息，注意到的内容等的具体区别，造成每个玩家看到的对局都是半个不透明。

所以叫做黑箱，是因为每个玩家只能做其中的一小部分

当你正好作为{ID1022-0213431323112}去用{125-I}成功打到了{ID0001-1613431323213}的敌人的{320mm}区域的的时候，会出现4种不同的结果，而这一部分取决于载具和玩家水平。如果你成功击杀了，那么就是触发了K密钥，如果没有，那可能不触发（被队友K头了/你跑路了），也有可能触发D密钥。

> 那么基于上述内容，接下来就是移动行为...

每个玩家的决策的来源信息是

- $I_{\textsf{minimap}}(t)$：小地图此刻能告诉你多少（几个点、在哪、动没动）；
- $I_{\textsf{screen}}(t)$：屏幕上此刻能看见多少（视野里有几辆车、朝向）；
- $I_{\textsf{audio}}(t)$：此刻能听到多少（引擎声、炮声、方位）；
- $I_{\textsf{historydata}}(t)$：你**之前**知道多少（30 秒前他在左边）。

而历史会过期，但不是突然作废，是慢慢变淡

$I_{\textsf{historydata}}(t)=I(t_0)\,e^{-\lambda(\Delta t)}$

因此，进入到整个决策的信息的公式是

$\tilde I(t)=\alpha(t)\cdot I_s(t)\cdot \rho$

- $\tilde I(t)$我实际读取的多少
- attention=$\alpha$
- 真实性=$\rho$
- $I_s$=信息的选择

> 这里的公式带$I_s$是因为人的注意力是有限的，分给这个就少了那个

而人们的判断通常类似于

$$
b_{t+1}=f\big(b_t,\ w_t,\ \tilde I_t\big)
$$

- $b$指的是判断
- 而$w$指的是你的位置
- 而$\tilde I_t$则是信息
- 而判断规则改变的是$f{}$函数

而每个人的具体的$f{}$理论上是不可复制的，每一个人的$f{}$都会有细小的区别

> 再回到之前的“全局”是一组黑箱随机数的角度下，验证一下战雷陆战历史是不是POMDP

POMDP：

① 状态存在，但不可全观测 如果玩家能全知，就不会被“看不见的人”打死。

② 观测是部分的、有噪声的，也就是会有错误信息的。

③ 转移是随机的 如果结果确定。其他玩家的行为不可预测。

④ 动作集有限 你能做的只有：走、停、开炮、撤、看。

*我建模的是决策点，不是连续操作。

> 那么战雷的陆战历史的确从某种意义上是符合POMDP家族的。

那么根据在有限两人零和博弈中，冯·诺依曼极小极大定理表明：参与人若要保证自己的期望收益不被对手压到博弈值以下，应采用极小极大策略；当不存在纯策略鞍点时，这要求使用混合策略。在两人零和博弈中，纳什均衡策略与极小极大策略重合，因此纳什均衡中的策略是不可剥削的；

- 但该结论不能直接推广到非零和或多人博弈。

零和定理在战雷里不适用，所以 minimax 从‘保证’降级为‘启发式’，

因为胜负由团队票数和占点决定，个人收益 ≠ 团队收益

意味着很多时候如果只按照最小化最大伤害执行，会造成非常大的问题，对局环境不是零和博弈。

因为 minimax 在非零和下不再给出保证，所以必须显式引入风险偏好——而$a$和$maximax$最大化最大收益就是那个偏好

加上maximax因为你总是会遇到以下类型的对局：

1. 队友是草履虫
2. 对面是草履虫
3. 对面50%都开了的对局
4. 队友开了还没打过的对局
5. 队友全退了
6. 敌人全退了

> 我不知道上一期的小伙伴们 ，到底有没有发现一点，我当时讲的参考公式：$H=a*minmax+(1-a)*maximax$ 其实并不准确，在那个战术上里严格意义上是 $\max\ (1-a)\,u_{maximax}\quad\text{满足于}\quad u_{minimax}\ge L_{\max}(a)$

- $L_{\max}$ 是目标最坏值，也就是可接受最大伤害，而不是实际最大伤害。

但是？上期讲的就是真的对吗？

- >（link_to_3edition2）


> 当POMDP遇到多人：三种基本模型

| 模型 | 核心特征 | 适用的多人游戏类型 | 求解目标 |
|---|---|---|---|
| **POMDP**（单智能体视角） | 只对一个智能体的信念状态建模，把其他玩家视为环境的一部分 | 对手策略相对固定或可估计的场景（如针对特定打法的扑克对局） | 对该智能体而言的最优响应（best-response） |
| **Dec-POMDP** | 多个智能体，**共享同一个奖励函数**，各自只有局部观测 | **纯合作**游戏（如桥牌、Hanabi、协作类桌游） | 最大化团队联合策略的期望回报 |
| **POSG** | 多个智能体，**各自有独立的奖励函数**，可以是零和、竞争或混合动机 | **竞争**（如星际争霸1v1）或**混合动机**（既有合作又有对抗）游戏 | 寻找纳什均衡或其他博弈解概念 |

所以最优解是POMDP+POSG。Dec-POMDP理论可靠，实际不可行，POSG好像也有点不太适合，POMDP没能把敌人预测

$$
T(s'\mid s,a)=\int_{a^{opp}}T(s'\mid s,a,a^{opp})\;P\big(a^{opp}\mid g(a)\big)\;da^{opp}
$$

**注意那个 $g(a)$——足迹。**

![alt text](<截屏2026-11-25 21.13.33.png>)

![alt text](<picture/截屏2026-11-25 21.18.50.png>)

![alt text](<picture/截屏2026-11-25 21.22.39.png>)

---
---
---
---

## 0. 记号

| 符号 | 含义 |
|---|---|
| $t\in\{0,1,\dots,T\}$ | 决策步（非帧，取"决策点"） |
| $i\in\mathcal{N}$ | 玩家编号；$\mathcal{N}$ 为对局参与者集合 |
| $s_t\in\mathcal{S}$ | 真实状态 |
| $a_t\in\mathcal{A}$ | 动作 |
| $o_t\in\mathcal{O}$ | 观测 |
| $h_t\in\mathcal{H}$ | 隐藏环境变量（匹配、时段、网络、队友质量等） |
| $y_t\in\mathcal{Y}$ | 结果事件，$\mathcal{Y}=\{\mathsf{K},\mathsf{D},\varnothing\}$ |
| $b_t$ | 信念（对状态的分布） |
| $\pi$ | 策略 |

状态分解：
$$
s_t \;=\; \big(s_t^{\text{self}},\, s_t^{\text{opp}},\, s_t^{\text{env}},\, h_t\big)
$$

---

## 1. POSG 形式化

$$
\mathcal{G}=\Big\langle \mathcal{N},\ \mathcal{S},\ \{\mathcal{A}^i\}_{i\in\mathcal{N}},\ \{\mathcal{O}^i\}_{i\in\mathcal{N}},\ T,\ \{R^i\}_{i\in\mathcal{N}},\ \gamma \Big\rangle
$$

- 转移：$T(s_{t+1}\mid s_t,\ a_t^1,\dots,a_t^{n})$
- 观测：$o_t^i \sim \mathcal{O}^i(\cdot \mid s_t,\ a_{<t})$
- 策略：$\pi^i(a_t^i\mid b_t^i)$
- 信念更新：$b_{t+1}^i=\tau\big(b_t^i,\ a_t^i,\ o_{t+1}^i\big)$

**关键**：对手的观测 $\mathcal{O}^{opp}$ 依赖于我方的动作足迹（见 §5），因此**对手不是"环境"**。

### 1.1 POMDP 是 POSG 的退化情形

若把对手动作边缘化（即承认"我不建模对手的策略"），则

$$
T(s_{t+1}\mid s_t,a_t)=\int_{\mathcal{A}^{opp}} T(s_{t+1}\mid s_t,a_t,a_t^{opp})\;P\big(a_t^{opp}\mid \mathcal{O}^{opp}(s_t,f(a_t))\big)\;da_t^{opp}
$$

**这就是 BS-PI 模型的准确身份**：它是 POSG 的**单智能体投影**。
→ 它丢掉的正是"对手会读我"这一项，而该项由 $f(a)$ 承担。

---

## 2. KD 作为结果泛函

结果序列 $y_{0:T}$，定义

$$
\mathrm{KD}\;=\;\Phi\big(y_{0:T}\big)\;=\;\frac{\sum_{t}\mathbb{1}[y_t=\mathsf{K}]}{\max\big(1,\ \sum_{t}\mathbb{1}[y_t=\mathsf{D}]\big)}
$$

性质：

1. **不可直接观测**：$\Phi$ 需要完整 $y_{0:T}$，而玩家只观测到 $o_{0:T}$；
2. **延迟**：$y_t$ 与 $a_t$ 之间隔着一个未观测的采样过程；
3. **小样本**：$\#\{t: y_t\neq\varnothing\}\ll T$。

形式化表述：

$$
\mathrm{KD}\ \text{对玩家而言是}\ \Phi\big(\text{对不可完全观测状态的部分采样}\big)
$$

---

## 3. 动作 = 条件分布算子

动作不是结果映射，而是**分布算子**：

$$
a_t:\quad P(\cdot\mid s_t)\ \longmapsto\ P(\cdot\mid s_t,a_t)
$$

玩家实际面对的是对 $h$ 边缘化后的分布：

$$
P(s_{t+1}\mid s_t,a_t)=\int_{\mathcal{H}}P(s_{t+1}\mid s_t,a_t,h)\,P(h\mid \mathcal{F}_t)\,dh
$$

及

$$
P(s_{t+1}\mid s_t,a_t)
=
\mathbb{E}_{h\sim P(h\mid\mathcal{F}_t)}
\Big[P(s_{t+1}\mid s_t,a_t,h)\Big]
$$

### 3.1 五个可干预维度

把 KD 分解为五个乘数型因子：

| 因子 | 含义 | 主要由什么动作干预 |
|---|---|---|
| $\lambda_E$ | 遭遇率 | 路线、区域选择 |
| $\lambda_F$ | 先手率 | 掩体、视线、停走节奏 |
| $\lambda_X$ | 交换率（对枪胜率） | 距离、角度、是否 1v1 |
| $\lambda_S$ | 生存率 | 退路、撤退时机 |
| $\lambda_C$ | 复利项（连续多杀） | 位置延续性、补给 |

近似：

$$
\mathbb{E}[\mathrm{KD}]\ \approx\ \lambda_E\cdot\lambda_F\cdot\lambda_X\cdot\lambda_S\cdot\lambda_C
$$

**核心主张（可检验）**：$\lambda_E$ 与 $\lambda_F$ 的方差贡献显著大于 $\lambda_X$（技术项）。

---

## 4. 控制 = 对分布的部分干预

定义控制动作集合 $\mathcal{A}^{c}\subset\mathcal{A}$，其干预目标为地图控制相关维度：

$$
\big(\text{敌方可选路线},\ \text{支援距离},\ \text{撤退自由度},\ \text{信息覆盖}\big)
$$

干预是"部分"的，因为四类不可控项：

1. 对手有限理性但会反制；
2. $h$ 不可观测；
3. 队友不是执行器（$\mathcal{A}^{ally}\neq$ 我方动作）；
4. 干预留下足迹。

---

## 5. 足迹与反制

动作同时产生两件事：

$$
a_t\ \longrightarrow\ P(s_{t+1}\mid s_t,a_t)
\qquad\text{且}\qquad
a_t\ \longrightarrow\ f(a_t)\in\mathcal{F}
$$

对手观测：

$$
o_t^{opp}=\mathcal{O}^{opp}\big(s_t,\ f(a_t)\big)
$$

对手反制分布：

$$
P\big(a_t^{opp}\mid o_t^{opp}\big)
$$

**干预幅度越大 → 分布改造越大，但足迹越大 → 反制分布越集中。**

---

## 6. 控制的净收益（BS-PI 核心公式）

$$
\boxed{
\mathcal{J}(a)=\underbrace{\mathbb{E}_{s'\sim P(\cdot\mid s,a)}\big[u(s')\big]-\mathbb{E}_{s'\sim P(\cdot\mid s)}\big[u(s')\big]}_{\text{分布改造收益 }\Delta_{T}(a)}
\;-\;
\underbrace{\mathbb{E}_{a^{opp}\sim P(\cdot\mid o^{opp})}\big[\,u(s)-u(s\mid a^{opp})\,\big]}_{\text{反制成本 }\Delta_{R}(a)}
}
$$

**结构性结论**：

$$
\frac{\partial \Delta_T}{\partial \|a\|}>0,\qquad
\frac{\partial \Delta_R}{\partial \|a\|}>0
\;\Longrightarrow\;
\exists\,a^{*}:\ \mathcal{J}'(a^{*})=0
$$

→ **控制存在最优点，不是越多越好。** 这就是"控制也有性价比"的形式化。

---

## 7. 优化问题

$$
\max_{\pi}\ \mathbb{E}_{\pi}\big[\Phi(y_{0:T})\big]
$$

约束：

$$
\begin{aligned}
&\mathbb{E}[\text{loss}]\le L_{\max} &&\text{（死亡成本不破下限）}\\
&P(\text{退路}\neq\varnothing)\ge p_0 &&\text{（退路不断）}\\
&P(\text{支援距离}\le d_0)\ge p_1 &&\text{（支援可达）}\\
&\mathbb{E}[\Delta_R(a)]\le R_{\max} &&\text{（反制成本可接受）}\\
&\text{randomize}(a)\ \Rightarrow\ \mathbb{E}[u(a)]>0 &&\text{（随机化只用于正期望）}
\end{aligned}
$$

---

## 8. HDAT：Hurwicz 参数化

### 8.1 准则

$$
H(a)=a\cdot u^{-}(a)+(1-a)\cdot u^{+}(a)
$$

其中
$$
u^{-}(a)=\min_{s'\in \mathcal{S}_{\text{worst}}(a)} u(s'),\qquad
u^{+}(a)=\max_{s'\in \mathcal{S}_{\text{best}}(a)} u(s')
$$

$a\in[0,1]$ 是"最坏情况"的权重。

### 8.2 两档离散化

$$
a_t\in\{0,1\}:\quad
a_t=1\ \text{保命档},\qquad a_t=0\ \text{收人档}
$$

**离散化的理由**：决策时间 $\Delta t$ 有限，连续 $a$ 的求解成本 $\gg$ 收益。即

$$
a^{\text{exec}}=\arg\min_{a\in\{0,1\}}\ \big|\,\mathcal{J}(a)-\mathcal{J}(a^{\text{cont}})\,\big|\quad\text{s.t.}\quad \text{decide}(a)\le \Delta t
$$

### 8.3 切换规则（"输得起吗"的形式化）

$$
a_t=\begin{cases}
1, & \text{VaR}_{\epsilon}\big(L(s_t)\big)>\bar{L}\ \ \text{或}\ \ \text{信息不足}\\ 
0, & \text{否则且}\ \mathbb{E}[u(a=0)]>0
\end{cases}
$$

其中 $\mathrm{VaR}_\epsilon$ 为损失的风险价值（分位数），$\bar L$ 为可承受阈值。

**默认 $a=1$。** 切换是例外，不是常态。

### 8.4 动态性

$$
a_{t+1}\neq a_t \iff \text{信念更新量}\ \|b_{t+1}-b_t\|>\delta
$$

→ "每时每刻重新估"的精确含义。

---

## 9. 命题（附证明要点）

**P1（不可观测性）**
若 $\mathcal{O}$ 非单射，则 $\mathrm{KD}$ 不可由 $o_{0:T}$ 唯一确定。
*证*：存在 $s\neq s'$ 使 $\mathcal{O}(s)=\mathcal{O}(s')$，而 $\Phi$ 对 $s$ 敏感。∎

**P2（分布性）**
动作只改变 $P(s_{t+1}\mid s_t,a_t)$，不直接改变 $y_t$。
*证*：$y_t$ 由 $(s_t,s_{t+1})$ 采样产生，$a_t$ 仅在 $T$ 中出现。∎

**P3（控制的边际收益递减）**
若 $\Delta_T$ 凹、$\Delta_R$ 凸，则 $\mathcal{J}$ 有唯一内点最优。
*证*：$\mathcal{J}''<0$。∎

**P4（两档最优性）**
给定决策预算 $\Delta t$，二值离散化在"可执行策略类"中损失最小。
*证*：人类的决策粒度在压力下退化为二元（chunking），连续策略不可执行，故在约束集内取端点。∎

**P5（随机对手下的退化）**
若对手策略与 $f(a)$ 无关（完全随机），则 $\Delta_R\equiv 0$，最优策略退化为

$$
\pi^{*}=\arg\min_{\pi}\ \mathbb{E}[\text{暴露时长}]
$$

→ **在随机对手环境中，"减少暴露"是唯一有效的优化方向。**
这也解释了为什么"敌人越随机，移动越重要"。

---

## 10. 可检验预测

| 编号 | 预测 | 检验方式 |
|---|---|---|
| H1 | $\lambda_E,\lambda_F$ 对 KD 的解释力 > $\lambda_X$ | 多因素回归 / 分箱对比 |
| H2 | 足迹 $\|f(a)\|$ 与对手反制率正相关 | 同一位置停留时长 vs 被针对概率 |
| H3 | $\mathcal{J}(a)$ 在某个干预强度处取最大 | 控制强度与胜率的关系曲线 |
| H4 | 两档 $a$ 优于单档 | 强制 a=1 / 强制 a=0 / 动态 a 的三组对照 |
| H5 | 路线数 $\le 2$ 时，移动策略增量趋零 | 小图（单通道）与大图的对比 |

---

## 11. 适用边界

$$
\text{方法适用}\iff
\begin{cases}
\text{信息非完全（}\mathcal{O}\ \text{非单射）}\\
\text{可选路线数}\ \ge 3\\
\text{对手非最优（否则退化为 minimax 定理）}\\
\text{执行精度足够（误差}\le\varepsilon）
\end{cases}
$$

**唯一能动摇体系的批评**：路线数 $\le 2$ 时，"选择"退化为"执行"，理论增量趋零。

---

## 12. 一句话形式化总结

$$
\boxed{
\begin{aligned}
&\text{KD}=\Phi\big(\text{部分采样}\big),\qquad
\text{控制}=\text{对 }P(s'\mid s,a)\text{ 的部分干预}\\
&\text{张力}=\Delta_T(a)-\Delta_R(a)\\
&\text{策略}:=\pi\big(a_t\,|\,b_t\big),\quad a_t\in\{0,1\}
\end{aligned}
}
$$

> **你能改的是条件分布，不是 KD；你能做的是部分干预，不是完全控制。**