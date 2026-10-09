---
name: kaggle-oof-readout
description: "Create repeatable Kaggle OOF error readouts by joining out-of-fold predictions with optional feature caches and summarizing overall, group, bucket, and feature-value errors. Use when analyzing where a Kaggle model is good or bad or when preparing evidence for a follow-up candidate to pass to `kaggle-strategy`."
---

# Kaggle OOF Readout

Use this skill to turn saved out-of-fold (OOF) predictions into a repeatable diagnostic. It creates analysis evidence; it does not update a route baseline, submit predictions, or edit `backlog/` directly.

## Workflow

1. Reuse existing data-exploration observations when the data version and scope match. If the question concerns raw inputs or label creation before predictions exist, use `kaggle-idea-forge` and its `references/data-exploration.md`; OOF is not a prerequisite for that work. Use `kaggle-review-exp` only when creating or changing an authorized experiment.
2. Read saved OOF predictions instead of retraining when possible.
3. Declare the evaluation unit, metric, and ID/group columns before choosing a helper. For row-level predictions, also declare target, prediction, bucket, and feature columns. Do not assume a competition schema or replace its metric with regression error.
4. Keep the split and preprocessing fold-safe. Any cache joined to OOF rows must have one row per declared ID unless the contract says otherwise.
5. Save source paths and SHA-256 values with the readout.
6. Record interpretation and non-use constraints in `result.md` or a completed report under `docs/surveys/`.
7. Pass any requested backlog change and its evidence to `kaggle-strategy`; do not edit backlog files from this skill.

## Preferred inputs

- OOF predictions containing an ID, target, and prediction.
- A group column when the validation split or test structure is grouped.
- Bucket columns that reflect the actual data contract, such as time ranges, length ranges, classes, or confidence ranges.
- Optional fold-level or averaged feature importance.
- Optional feature cache joined by ID, loading only the columns needed for analysis.

Ignore missing or zero-byte placeholders. Support both local artifact paths and Kaggle input paths through explicit command arguments or experiment config.

## Readout questions

- Which groups or buckets dominate absolute or squared error?
- Which feature-value ranges have higher error than the global average?
- Does a comparison prediction improve the overall metric while hurting specific groups?
- Is a follow-up change justified by enough rows and fold-safe evidence?

Feature importance or correlation alone is not evidence that a router, post-process, or submission should be adopted. Connect the observation to a comparison that preserves the proposed mechanism, including final selection or post-processing when relevant. Before adding another diagnostic, state which next action its result changes and which effects it cannot rule out. Follow the exploration and experiment principles in `AGENTS.md`; explaining every residual error is not required before proceeding.

## Bundled helper

The helper accepts explicit column names but computes regression diagnostics (RMSE, MAE, signed error, and squared error). Use it only when those quantities answer the question. For classification, ranking, detection, tracking, or another structured output, first use the competition's evaluator or a verified task-specific implementation. Preserve unknown labels and the metric's aggregation rules; do not treat unannotated items as negatives.

```bash
uv run python .agents/skills/kaggle-oof-readout/scripts/oof_readout.py \
  --oof experiments/<exp>/artifacts/oof.csv \
  --output-dir experiments/<readout-exp>/artifacts \
  --id-column id \
  --target-column target \
  --prediction-column prediction \
  --group-column group_id \
  --bucket-column length_bucket \
  --feature-column feature_a
```

Use `--compare-prediction-column` to compare two prediction columns. Use `--feature-cache` to join separately stored features by ID. The helper writes overall metrics, optional group and bucket summaries, feature quantile metrics, and a JSON summary with input SHA values.

## Comparing evaluated outputs

Use `task compare-evaluations` for two already evaluated per-unit metric tables. Follow [the comparison manifest and command reference](../../../docs/evaluation_comparison.md) to declare the evaluation conditions, input hashes, metric directions, and expected coverage. This supports task-specific metrics without embedding a particular competition in this skill. A mismatch is a reason to report the missing evidence, not to retrain automatically or silently compare only the intersection.

Report group differences and improvement/degradation counts alongside the scope of the evaluation. Per-unit means are diagnostic summaries, not automatically the official aggregate. For a change inside a multi-stage pipeline, compare the affected output and the final output when both are available; a local improvement may disappear during later selection or post-processing. This analysis does not replace any progression conditions in the experiment contract.

## Recording

- Separate diagnostic metrics from official CV and leaderboard scores.
- State row and group coverage, source artifact SHA values, and any missing subset.
- Do not update the experiment status to a user-decision state without the user's judgment.
- If the result becomes reusable analysis, update the relevant metadata-indexed report in `docs/surveys/` instead of creating one report per rerun.

When creating or changing formulas in documents or Notebook Markdown cells, follow the [math conventions and verification steps in AGENTS.md](../../../AGENTS.md#markdown-と-notebook-の数式) for the changed files.

## Validation

Analyzing already saved predictions does not require a new experiment or these execution checks. For an authorized readout experiment that needs Kaggle execution:

```bash
task validate-exp EXP=<exp>
task check-exp EXP=<exp>
task test-exp EXP=<exp>
task prepare-kaggle-notebooks EXP=<exp> EXTRA_ARGS="--notebook train --run-on-push"
```

Use the same-named Make target only when `task` is unavailable. After execution, confirm output presence and record rows, groups, elapsed time, source SHAs, and artifact SHAs.
