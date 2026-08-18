---
name: llm-as-a-verifier
description: >
  Verification as a scaling axis. Score candidate solutions/trajectories with
  continuous, probabilistic feedback (expectation over score-token logprobs)
  instead of discrete 1-5 judge integers, then select/rank/track via the
  llm-verifier API (select, compare, track). Use for best-of-N selection,
  code review ranking, pairwise comparison, and progress tracking on
  long-horizon tasks.
---

# LLM-as-a-Verifier

General-purpose verification framework (arXiv 2607.05391, llm-as-a-verifier.com). The core claim: generation is not the bottleneck — *verifying which candidate is correct* is. Agents often already know how to solve a task (100 sampled trajectories can nearly solve Terminal-Bench); they fail at picking the correct one, especially on long-horizon tasks. Standard LLM-as-a-Judge is too coarse — coarse 1-5 scoring produces ~27% ties on Terminal-Bench V2. This skill replaces discrete judging with probabilistic, continuous scoring.

## Core Idea

Instead of prompting an LLM for a single integer score, extract the **probability distribution over all score tokens** (`<score_A>` / `<score_B>` tags) and take the **expectation**. This yields a continuous reward with variance you can shrink, plus a preference probability for pair-wise decisions. It requires **no additional training**.

The score is averaged over three dials:

```
reward(τ) = mean over  criteria C ×  repeated evals K ×  score granularity G
             of p_θ(v_g | x, c, τ) · φ(v_g)   (prob of token × token's scalar)
```

Scaling each axis improves verification accuracy:

| Axis | Effect | Evidence |
|---|---|---|
| **Granularity** G | Finer score space (1-20) gives the decoder room to separate correct vs incorrect | 73.1% (G=1) → 77.5% (G=20) |
| **Repeated eval** K | Monte Carlo averaging; variance drops as O(1/K) | 74.7% (K=1) → 77.4% (K=16) |
| **Criteria decomposition** C | Ensemble of sub-criteria beats a monolithic rubric | any single 75.2-76.4% → ensemble 78.3% |

## API (pip install llm-verifier)

Three entry points cover the practical uses:

| Call | Purpose |
|---|---|
| `llm_verifier.select(task, cands)` | **Best-of-N selection** — score N candidates, return the best (test-time scaling in one call). |
| `llm_verifier.compare(task, a, b)` | **Pairwise comparison** — score two candidates head-to-head with fine-grained preference. |
| `llm_verifier.track(task, traj)` | **Progress tracking** — temporally aligned progress score over a rollout, for monitoring or RL. |

## Workflow

### 1. Best-of-N Selection (test-time scaling)
For any task where you can generate many candidate answers/solutions:
1. Generate N candidates (this is the cheap part — agents already know how to solve it).
2. `best = select(task, cands)` to pick the winner.
3. For cost-sensitive runs, use **Probabilistic Pivot Tournament (PPT)** under the hood — cuts cost from O(N²) to O(Nk).
   - **Ring pass**: score each adjacent pair on a random Hamiltonian cycle so every candidate appears once in the "A" slot and once in "B" — cancels the model's positional bias.
   - **Pivot selection**: rank by ring-pass scores, keep the top-k as pivots.
   - **Pivot tournament**: score non-pivot-vs-pivot and pivot-vs-pivot pairs, concentrating budget on the uncertain top.
   - **Selection**: aggregate weights w_i and counts c_i; return the candidate with highest normalized w_i/c_i.

### 2. Pairwise / Code Review
Use `compare(task, a, b)` when reviewing two implementations (e.g. yours vs a reference, or two PR approaches) and you need a defensible, tie-free verdict.

### 3. Progress Tracking
Use `track(task, traj)` during long multi-step refactors or rollout tasks. High correlation between chronological step progress and verifier score (Spearman VOC 0.966 vs 0.877 for a fine-tuned robot reward model) makes it a reliable canary: a stagnating/flat line means the trajectory is off-course.

## Scoring Prompt Pattern

When hand-rolling a prompt (e.g. in a test harness), follow the letter-based scheme — letters not digits, so logprobs are extractable:

```
You are an expert [domain] reviewer. You will see a task description and two trajectories.
Evaluation Criteria: [domain specific criteria]
Task: {task prompt}
Trajectory A: {A} Trajectory B: {B}
Carefully analyze each trajectory, then provide your final scores:
<score_A> INTEGER_1_TO_20 </score_A>
<score_B> INTEGER_1_TO_20 </score_B>
Rating Rules: Rate correctness on a 1-20 scale (1 = incorrect, 10 = borderline, 20 = correct)
```

Read the logprobs from the `<score_A>` / `<score_B>` tags and take the expectation — do **not** collapse to a single sampled integer.

## Logit-Restricted Frontier Models

Frontier models (GPT-5.5, Claude Opus) sometimes withhold token-level logprobs. Workaround — two-stage split:
1. **Closed model** supplies domain reasoning (it's good at that).
2. **Open verifier** (e.g. Gemini 2.5 Flash) supplies the calibrated probability distribution it withholds.

Evidence: routing GPT-5.5's reasoning through Gemini 2.5 Flash on Terminal-Bench V2 recovered +5.2 accuracy over using the closed model's integer scores (80.1% vs 74.9%) and eliminated its 10.9% tie rate entirely — with no access to the frontier model's logits.

## Pitfalls

- **Tie collapse**: never report a single integer verdict from a judge. Take the logprob expectation; ties should be ~0, not 27%.
- **Positional bias**: when comparing pairs, ensure each candidate appears in both the A and B slot (the ring pass does this) — otherwise the verdict is contaminated.
- **Monolithic rubric**: decompose into sub-criteria (e.g. Specification, Output, Errors) rather than one vague "is this correct".
- **Cost blow-up**: naive all-pairs comparison is O(N²). Use PPT / the `select` API's built-in pivot tournament for large N.
- **Don't fine-tune**: this is training-free. If you feel the need to train a reward model, you've left the framework's design envelope.

## Key Principles

- Verification is a **scaling axis** — throw verifier compute at correctness before throwing more generation compute at candidates.
- **Continuous over discrete**: expectations of distributions over integers; granularity and repetition buy accuracy cheaply.
- **Decompose criteria**: an ensemble of simple sub-rubrics beats one complex one.
- **Training-free**: works on any moderately capable model; no fine-tuning required.
- **Multi-domain**: proven on coding (Terminal-Bench V2 86.5%, SWE-Bench Verified 78.2%), robotics (RoboRewardBench 87.4%), and medical (MedAgentBench 73.3%).

## Extensions & Deployment

- **Claude Code / Codex extensions** are provided upstream — wire `track`/`select` into agent progress and candidate selection rather than hand-rolling.
- As a **dense RL reward**: SLM-as-a-Verifier scores are a drop-in dense reward — ~1.8× sample efficiency over sparse rewards on LIBERO (SAC) and ~1.1× on MATH (GRPO).

## Related

- `ruby-on-rails/SKILL.md` — invokes this for automatic code review ranks and long-refactor progress tracking.
- `verify-findings` — the Hermes-side checklist that pairs with this scoring method.
