# TNVT(RNVT): Random Number Variable Tactics

## Theory/Tactics from where?-- KD

- For players, KD is a black-box statistical output. For the server, it is generated step by step from a large number of combat events under hidden rules. Players cannot observe all rules; they can only influence the conditional probability distribution of “encounter — first move — fight — loss” through adjustable parameters.
- This document uses “valid key K / invalid key D” as a **mental model**, not as a server-mechanism definition:
  - **Valid key K**: an observable condition combination that raises expected net utility, e.g. “first move + favorable terrain + teammate support + sufficient HP/ammo.”
  - **Invalid key D**: a condition combination that lowers expected net utility or makes risk uncontrollable, e.g. “no information + exposed route + no retreat + teammate out of position.”
  - **Inserting the key**: not inserting into a random number, but using action planning to move the current state toward a more favorable condition distribution.
- KD is usually determined by “first move, encounter enemy, technique.” Behavior patterns can influence the first two; the third is constrained by aim, information, team, and resources.
- The key metaphor is useful for memory and review, but it must be falsifiable: it should map to encounter rate, first-move rate, combat win rate, death cause, route/position distribution, and retreat success rate. Otherwise it becomes an unfalsifiable explanation.

## Theory/Tactics from where?-- minimax(simple)

- **Definition**: Minimax chooses a strategy that maximizes the worst-case outcome under the assumption that the opponent/environment responds in the least favorable way:
  $$
  \max_s \min_o U(s,o)
  $$
  Under zero-sum, finite-strategy, and comparable-utility assumptions, Minimax and Maximin are equivalent. This document uses it as a **risk-averse lower-bound heuristic**: avoid being exploited unilaterally, do not gamble on good matchmaking, and do not chase “blood profit.”
- **Boundary conditions**:
  - It guarantees the lower bound **inside your model**, not the real system’s lower bound.
  - Team FPS/battle royale is not strictly zero-sum; matchmaking is not a rational opponent.
  - It can reduce the degree of being crushed. Empirically, in some matches it may offset roughly **50–70%** of a skill/information gap, but it cannot fully equalize top players and low-skill players, nor remove aim, team, network, and matchmaking gaps.
  - Top players do not reject risk management; they reject sacrificing upside for a pure lower bound. They use “utility maximization subject to a lower-bound constraint,” not pure Minimax.
- **Environment factors** should be modeled separately:
  - **Opponent**: a boundedly rational adversary who reads patterns and counters, but is not always optimal.
  - **System**: SBMM/EOMM/MMR, group bias, time-of-day, unpopular modes, mixed squads, etc. These are **environment non-stationarity and hidden variables**, not a Nash-equilibrium rational opponent.
  - **Team and objectives**: non-zero-sum cooperation with objective score, resource exchange, sacrifice roles, and time pressure.

## environment reason

In a brutal adversarial environment, whether you face a top-tier player’s experience advantage or the system’s dynamic matchmaking effects, the practical survival rule is not “mixed strategy is the only law.” A more accurate statement is: **mixed strategy reduces predictability and narrows the counter-strategy window; risk constraints secure the lower bound; the two together improve survival and utility stability.**

1. **Why pure strategies are doomed?**  
   If you always stick to a fixed approach — a minimalistic fixed camping spot, memorized points, a fixed route, fixed timing, or reckless charging — your behavior becomes predictable. Once an opponent reads your pattern, they can build a low-cost counter-strategy and exploit your KD, win rate, and game experience.  
   This is also why counter-strategy is common in games such as War Thunder. But counter-strategy is not useful only because “most players charge blindly”: any predictable pattern can be countered, including a top player’s default tempo. In public matches, counter-strategy is cost-effective because most players have narrow behavioral distributions, low self-correction, and low counter-cost. In high-level play, counter-strategy still exists, but the counter window is smaller and depends more on information, tempo, and team coordination.

2. **The core of the Minimax Theorem: securing the lower bound**  
   The core idea is: in a zero-sum game, consider the worst case when the opponent responds optimally to you, and base decisions on that. Do not gamble on whether today’s opponent is clueless, or whether the system will deal you good cards. Calculate how to make “the high probability of being killed” as small as possible. As long as you are not easily eliminated, the enemy’s gains are locked at a lower bound.  
   But this is a model-level lower bound. It does not guarantee “no loss” in real matchmaking, and it does not guarantee equalizing skill gaps.

3. **Mixed strategy’s dimensional-reduction strike: unpredictable variables**  
   To approach the Minimax value, use a mixed strategy: do not always be at Point A, do not always be at Point B, and do not follow a fixed path all the way. Allocate controlled random variable assignments among multiple **positive-expected-utility** actions/points according to the situation.  
   Requirements:
   - Do not randomize uniformly; allocate frequency by expected net utility.
   - Set minimum/maximum frequencies so no action is overused or underused.
   - Avoid fixed cycles, or the “randomization” becomes a new readable pattern.
   - Mix only among positive-expected-utility actions; negative-EU actions are not legitimized by randomness.
   - Defense can also be a high-EU action. Therefore, do not judge only by “high weight vs. low weight”; judge whether the weight is utility or risk.

## Tactics

Define **weight as expected net utility**, not pure risk. For action \(a\), an approximate expected utility is:

$$
EU(a)=\sum_s P(s)\Big[
P(\text{encounter}\mid a,s)\big(
P(\text{first move}\mid a,s)W_{\text{win}}
+(1-P(\text{first move}\mid a,s))W_{\text{lose}}
\big)
-C_{\text{death}}
-C_{\text{exposure}}
-C_{\text{time}}
-C_{\text{retreat}}
\Big]
$$

Decision rule:

- High positive expected net utility and acceptable risk → move/attack.
- Negative expected utility or risk above threshold → defend/retreat/change route.
- Defense itself may be a high-EU action, so do not look only at “weight high/low”; look at whether the weight represents utility or risk.
- Among multiple positive-EU actions, use controlled mixed randomization.

Before each action, assess:

1. Will I die? How large is the death loss?
2. Could I encounter enemies? How high is the encounter probability?
3. Where might I encounter enemies? Where might enemies appear?
4. If I encounter them, can I win? What are first-move probability, win rate, HP, ammo, skills, and items?
5. Is there a retreat route? What is the retreat cost?
6. Can teammates support? Are they out of position?
7. Is map control and information sufficient? Does sound information support the action?
8. Do time/resource objectives allow me to play safe, or must I take risk?
9. How large is the exposure cost? How easily can I be countered afterward?
10. Is the risk worth it? Does the reward cover the risk?

Use the first six items as a minimum risk screen; full decisions must also include the reward side and state side.

Decision state:

- Use an **approximate Markov decision process**: the state should include currently observable teammate positions, resources, objectives, HP/ammo, map control, sound information, known enemy positions, and time pressure.
- If the state is complete enough to compress the history needed for the decision, it can be treated as an approximate MDP.
- If the state is incomplete, explicitly treat it as a **short-horizon heuristic or partially observable decision process (POMDP)**, not a strict Markov chain.
- “Ignore history and only consider the present” is not Markov property. Markov property requires the current state to contain the necessary historical information.
- Also, when deciding the 'weight' each time, ignore all past history and only consider the current optimal solution (Markov Chain).

Tactical loop:

1. Collect current state: teammates, resources, objectives, HP/ammo, map control, sound, known enemy information.
2. Generate candidate actions: push, defend, rotate, retreat, trade resources, wait for teammates.
3. Estimate encounter probability, first-move probability, combat win rate, death/exposure/time/retreat costs for each action.
4. Compute expected net utility and apply risk thresholds.
5. Among multiple positive-EU actions, randomize frequency in a controlled way.
6. Execute and record: pre-decision state, action, result, death cause, route/position.
7. Review with small-sample A/B tests, and calibrate parameters locally by map, mode, rank, time of day, and squad situation.

Testable metrics:

- Encounter rate, first-move rate, combat win rate.
- First-death rate, death-cause distribution.
- Route/position distribution, repetition rate of fixed patterns.
- Retreat success rate, post-exposure survival rate.
- Objective contribution, resource-control time.
- Opponent strength / teammate quality / squad situation across consecutive matches.
- Correspondence between pre-decision state and outcome.

Local calibration:

- Principles are general; parameters are not. Encounter probability, first-move probability, combat win rate, and retreat cost differ by map, mode, rank, time of day, and squad situation. Calibrate with local data; do not apply one map’s weights to all maps.

Limitations:

- It cannot eliminate skill gaps or guarantee no loss.
- It cannot guarantee “forced equalization” between top players and low-skill players; it can only secure a model-level lower bound and, empirically, offset part of the gap.
- Team objectives may require taking risk; pure survival play can lose the objective.
- Top-level play requires information warfare, tempo pressure, dynamic exploitation, and team coordination on top of the lower bound.
- Matchmaking should be treated as environment non-stationarity; it cannot explain all fluctuations.
- The “key” is a mental model, not a server mechanism.

**Summary:** Secure the lower bound, reduce predictability, and do not gamble on blood profit. Principles are general; parameters are locally calibrated. The key is a metaphor; the theorem is a boundary.
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

