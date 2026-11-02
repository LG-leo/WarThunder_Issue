# TNVT(RNVT):randomly number variable tactics

## Theory/Tactics from where?-- KD

- KD for players (3D KD for 2D beings/2D humans) is defined as tens of thousands of random numbers, requiring a key to calculate K, calculate to D, and cancel out a K.
-
- So That:For players, KD is a set of tens of thousands of random numbers. When player A inserts a key of a few hundred characters into these tens of thousands of random numbers, once the key of a few hundred characters is triggered, it will produce a valid key (K) and an invalid key (D).
-
- So the player just needs to increase the distribution of K (the valid key) across the entire trigger key. That is, if the total number of trigger key occurrences stays the same, K becomes relatively more frequent, and D becomes relatively less frequent.
-
- KD is usually determined by the 'first move, encounter enemy, techniqce'. Behavior patterns can solve the first two.

## Theory/Tactics from where?-- minimax(simple)

-definition:Minimize the Maximum Loss

In zero-sum games, **Minimax(Minimize the Maximum Loss) and Maximin(Maximize the Minimum Gain)** are equivalent (the Minimax theorem says max min = min max). That is why I choose it to be the base of the Tactics.

Which means that, in the worst events, **it can force equality between people with low skills and those with high skills extremely.** 

**BUT**, it cannot completely close the gap.

## environment reason

In a brutal adversarial environment, whether you’re facing the overwhelming experience of a top-tier player or the system’s dynamic punishments, Von Neumann’s Minimax Theorem and Nash Equilibrium reveal a single survival law: in confrontation, the only strategy that guarantees you won’t be exploited by your opponent is the mixed strategy.

1. Why pure strategies are doomed?
In game theory, if you always stick to a fixed approach (pure strategy, e.g., a minimalistic fixed camping spot, memorizing points by rote calculation, or reckless charging), against a highly experienced opponent your moves become predictable. Once your pattern is read by the opponent, they can create a perfect counter-strategy to fully exploit you. Your KD, win rate, and overall gaming experience will be harvested like a lamb ready for slaughter.

- it also is the why in WarThunder, we have lots of counter-strategy

2. The core of the Minimax Theorem: securing the lower bound
The core idea of the Minimax Theorem is: in a zero-sum game, I must consider the worst-case scenario when my opponent responds optimally to me and base my decisions on that. I don’t gamble on whether today’s opponent is clueless, or whether the system will deal me good cards. I only calculate: how to make the "highest chance of me being killed" as low as possible. As long as I’m not easily eliminated, the enemy’s gains are locked at a lower bound.

3. Mixed strategy’s dimensional reduction strike: unpredictable variables
To achieve this minimax value, you have to use a mixed strategy. That is: you can’t always be at Point A, nor always at Point B, and you definitely can’t follow a fixed path all the way. You need to use controlled random variable assignments between multiple "expected value points" according to the situation.

## Tactics

So, just assess the risks each time before taking action:

1. Will I die?
2. Could I encounter enemies?
3. Where might I encounter enemies?
4. Where might enemies appear?
5. Is the risk of my action worth it?
6. Does the reward outweigh the risk?

Before each action, evaluate and assign weights.

Move when the weight is high, and 'defend' when the weight is low.

Also, when deciding the 'weight' each time, ignore all past history and only consider the current optimal solution (Markov Chain).

---
---
---
---
---

## Theory from where?-- minimax(for whole):

---

"Minimax" is not a single concept. It has different focuses in game theory, mathematical optimization, and statistical decision theory, but its core logic is always about **finding the best solution in the 'worst-case scenario'**. Below are more precise definitions in both Chinese and English for these three fields.

In zero-sum games, Minimax and Maximin are equivalent (the Minimax theorem says max min = min max).

---

### 🎲 Minimax (and Maximin) in Game Theory


For a two-player zero-sum game, let player 1’s payoff function be $g(i,j)$, where $i \in I$ is player 1’s strategy and $j \in J$ is player 2’s strategy. Player 1 seeks to maximize $g$, while player 2 seeks to minimize it. The **maximin value** $\underline{v}$ and **minimax value** $\overline{v}$ are defined as：

$$
\underline{v} = \sup_{i \in I} \inf_{j \in J} g(i,j), \qquad 
\overline{v} = \inf_{j \in J} \sup_{i \in I} g(i,j).
$$

$\underline{v}$ is the **highest payoff that player 1 can guarantee** regardless of player 2’s action; $\overline{v}$ is the **lowest payoff that player 2 can guarantee** regardless of player 1’s action. In general, $\underline{v} \le \overline{v}$. When equality holds, the game is said to have a **value**, and the common value is the rational outcome of the zero-sum game (von Neumann’s minimax theorem).

In a more general (non-zero-sum) game, the minimax value can also be understood as: **the highest payoff you can guarantee when the other players don't know your actions**; equivalently, it's **the lowest payoff that the other players can force you to accept once they know your actions**.

$underline{v}$ is the highest payoff that player 1 can guarantee themselves without knowing what the other will do; $overline{v}$ is the lowest payoff that player 2 can guarantee without knowing what the other will do (basically pushing player 1’s payoff as low as possible). Generally, we have $underline{v} le overline{v}$. When the two are equal, the game is said to have a value, which is the rational outcome of a zero-sum game (von Neumann’s minimax theorem). In general non-zero-sum games, the minimax value is also often interpreted as: the largest of the smallest possible payoffs a player can get when the opponent knows everything and acts in the most unfavorable way (or equivalently, the smallest of the largest possible losses).

---

### 📐 Minimax Problems in Mathematical Optimization

In optimization theory, minimax refers to a type of mathematical programming problem where you first let an "opponent" maximize the objective function over some variable, and then the decision-maker chooses the variable to minimize this already maximized result.
A **minimax problem** is an optimization problem of the form

$$
\min_{x \in X} \; \max_{y \in Y} \; f(x,y),
$$

where $f: X \times Y \to \mathbb{R}$ is the objective function, and $X, Y$ are the feasible sets for the minimizing and maximizing variables respectively. Equivalently, the minimax problem seeks a decision $x$ that minimizes the worst-case value (over $y$) of $f(x, \cdot)$. Because the inner maximization generally destroys differentiability, minimax problems are typically **nonsmooth optimization problems**, even when $f$ itself is smooth. A point $(x^*, y^*)$ is a **saddle point** if $f(x^*, y) \le f(x^*, y^*) \le f(x, y^*)$ for all $x,y$; saddle points provide a classical route to solving minimax problems.

---

### 📊 Minimax Decision Rule in Statistical Decision Theory

In statistical decision theory, minimax is a **robust decision criterion**: it doesn't assume a prior distribution, but directly uses the **maximum risk** to evaluate a decision rule.

Let $\Theta$ be a parameter space, $\mathcal{D}$ a decision space, and $R(\theta, \delta)$ the **risk function** of a decision rule $\delta$. A decision rule $\delta_0$ is called a **minimax rule** if it minimizes the **maximum risk**：

$$
\sup_{\theta \in \Theta} R(\theta, \delta_0) = \inf_{\delta} \sup_{\theta \in \Theta} R(\theta, \delta).
$$

Thus a minimax rule is chosen by judging each rule by its **worst-case performance** over the parameter space, and then selecting the rule whose worst-case risk is smallest.

---

### 💎 The core that connects the three: the Minimax Theorem

The definitions in the above game theory and optimization are closely linked through the **von Neumann minimax theorem**: in a two-player zero-sum game, if mixed strategies are allowed,then:

$$
\max_{x \in \Delta(I)} \min_{y \in \Delta(J)} \mathbb{E}[g(i,j)] 
= \min_{y \in \Delta(J)} \max_{x \in \Delta(I)} \mathbb{E}[g(i,j)],
$$

That is, **the maximin value equals the minimax value**, so a zero-sum game always has a 'value' under mixed strategies. This theorem also provides the theoretical foundation for linear programming duality, the existence of saddle points, and many minimax formulations in robust optimization.

**In short**: In game theory, minimax describes **guaranteed gains in adversarial situations**; in optimization, minimax is a **mathematical programming structure of 'max first, then min'**; in statistical decision-making, minimax is a **robust decision criterion based on the worst-case risk**. All three share the same logical form—**choose the best response after your opponent or uncertainty picks the worst-case scenario**.

