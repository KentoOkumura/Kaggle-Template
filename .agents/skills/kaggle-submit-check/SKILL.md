---
name: kaggle-submit-check
description: "Kaggle 提出前に、提出物と notebook metadata を検証し、問題を切り分けて記録する。`submission.csv`、zip された予測ファイル、Kaggle Notebook output、`kernel-metadata.json`、`sample_submission` 互換性、hidden test 対応、行数、重複 ID、欠損、internet/GPU metadata、オフライン実行前提を確認する。Kaggle submit 直前、notebook output の検証、提出失敗時に使う。"
---

# Kaggle 提出チェック

ローカルで、アップロードしない事前チェックを実行する。このスキルはsubmit、push、uploadを行わない。

## 手順

1. 対象を特定する。
   - CSV ファイル、zip ファイル、notebook フォルダ、またはプロジェクトルート。
   - 指定がなければ、`submission.csv`、`*.zip`、`kernel-metadata.json`、`sample_submission.csv` などの候補を探す。

2. リポジトリでは正のCSV validatorを実行する。`EXP`を指定した場合は、PASS/FAIL、行数、重複ID数、欠損数、infinite value数、target統計、submission SHAが同じ実験の`metrics.json`へ自動保存される。対象実験を特定できない場合は`EXP`を省略し、別実験へ推測で保存しない。

同梱の `scripts/validate_submission.py` は、固定行数の数値予測CSVを対象とする。sampleを指定すると行数・IDの一致を検査するため、予測件数が可変の提出へそのまま適用しない。可変行数のコンペを導入するときは、公式の出力単位・行数制約・IDの参照整合性に合わせて正のvalidatorを実装・更新してから使う。sampleやIDの検査を無効化しただけで、コンペ固有の検証を満たしたPASSとして扱わない。

```bash
task submit-check EXP=expXXX_title SUBMISSION=/tmp/kaggle-output/expXXX_title/inference/submission.csv
```

`task`が利用できない場合は、同じ引数で`make submit-check`を使う。CSV以外のzip、notebook folder、`kernel-metadata.json`もまとめて調べる必要がある場合だけ、補助checkerを追加実行する。補助checkerはCSV部分を正のCSV validator、Notebook packageを`scripts/validate_kaggle_metadata.py`へ委譲する。Notebook検証の対象は`prepare-kaggle-notebooks`が生成したpackage全体であり、`project.yml`、bootstrapを含むNotebook、同梱sourceを一緒に指定する。metadataだけを切り出したコピーはPASSにしない。複数CSVから提出ファイルを選べない場合や検査対象がない場合はFAILとし、対象ファイルを明示して再実行する。

```bash
uv run python .agents/skills/kaggle-submit-check/scripts/check_submission.py PATH --sample sample_submission.csv
```

`--sample`はsample fileが存在する場合だけ使う。リポジトリ外へcheckerだけをコピーして使わず、正のvalidatorと`project.yml`を含むリポジトリルートから実行する。提出の行単位・ID規則・行数制約はコンペ公式仕様と`project.yml`を確認する。固定行数の予測コンペだけsampleとの1対1整列を要求し、予測件数が可変の提出では上記のvalidator更新後にsampleを列schemaの照合に使う。

3. スクリプトだけでは証明できない warning を手で確認する。
   - CV は test で想定される grouping/time split と一致しているか。
   - 固定行数の予測コンペでは、出力は `sample_submission.csv` の行順を保っているか。予測件数が可変の場合は、コンペ固有の行単位・ID規則・入力単位の網羅を満たすか。
   - Kaggle のオフライン環境で依存関係を利用できるか。
   - ルールで許可されていない限り、internet が無効になっているか。
   - Kaggle Notebook の実行時間とメモリ制限に収まる推論になっているか。
   - code competition では公開 `test/` と `sample_submission.csv` が hidden test 用に差し替えられても動作するか。公開 test 固有の ID、行数、ファイル名、SHA、予測値に依存していないか。
   - hidden test の入力と保存済み model manifest / model 生成物だけで推論が完結するか。実行時のsampleとのIDによる1対1整列は固定行数の予測コンペで確認する。

4. 結果を報告する。
   - `PASS`: チェックした範囲からは提出してよい。
   - `WARN`: ユーザーがリスクを受け入れる場合のみ提出してよい。
   - `FAIL`: 提出しない。正確な修正方法を示す。

## リポジトリ内の提出フロー

Kaggle 実験リポジトリ内で作業する場合:

1. `project.yml` に提出設定があることを確認する。sample file、id column、target columns を含む。
2. inference notebook の生成、push、Kaggle 実行は `kaggle-review-exp` と `kaggle-platform` に委譲する。このスキルでは、生成済み notebook と `kernel-metadata.json` を検証する。slug は 50 文字以内、`id` と `title` 由来 slug は一致、accelerator / internet / competition source は意図どおりであることを確認する。

3. `kaggle-platform` の手順で取得された Kaggle output がある場合、Kaggle 上で生成された `submission.csv` を手順2のコマンドでsample submissionに対して検証する。ローカル実験ディレクトリに提出CSVを常設しない。

4. PASS / WARN / FAIL と`metrics.json`へ保存した証拠を報告する。code competitionでは、Kaggle outputに存在する提出ファイル名（通常`submission.csv`）も引き渡し情報として明記する。実際のsubmitは`AGENTS.md`の承認条件と`kaggle-platform`の操作手順へ委譲する。submit後の監視は`kaggle-submit-monitor`に委譲する。

5. submit が行われてスコアが分かったら、リポジトリに記録する。

```bash
task record-exp EXP=expXXX SUBMISSION_REF=12345678 CV=0.1234 PUBLIC_LB=0.1200 EXTRA_ARGS="--submission-status complete"
task record-submission EXP=expXXX SUBMISSION=/path/to/submission.csv SUBMISSION_REF=12345678 EXTRA_ARGS="--notes baseline"
```

`record-exp`にsubmission refを渡し、先に`metrics.json.submissions[submission_ref]`へ当該提出の値を記録する。この操作では実験の代表CV/LBと実験statusを上書きしない。`record-submission`はCV/LBの引数を受け取らず、同じrefの値を読み、`SUBMISSIONS.md`へ記録する。同じrefを再指定すると既存行を更新するため、Private LB判明後も新しい行を追加しない。同じスコアを複数のコマンドへ手入力しない。実験の代表値を変える場合は、submission refなしの`record-exp`で明示的に更新する。

code competitionでKaggle outputをローカル取得していない場合は、`kaggle kernels files`またはUIで対象kernel versionの`submission.csv`を確認したうえで、ローカルファイル証拠を未取得として記録する。

```bash
task record-submission EXP=expXXX SUBMISSION=submission.csv SUBMISSION_REF=12345678 EXTRA_ARGS="--allow-missing-file --notes 'Kaggle output not downloaded'"
```

記録先の役割は`AGENTS.md`を正とする。`EXP`付きの`submit-check`は検証結果とsubmission SHAを対象実験の構造化された証拠へ保存する。提出コマンド、scoring経過、結果の解釈は同じ実験の正本へ分担して追記し、ここでは別の分担規則を定義しない。

確認項目:
- 固定行数の予測コンペでは行数が `sample_submission.csv` と一致している。予測件数が可変の場合は、公式仕様の行数制約と必要な入力単位の網羅を満たす。
- 必須列が存在し、想定外の追加列がある場合は意図的である。
- id column が設定されている場合、コンペ固有の一意性・参照関係を満たす。sampleとのIDの順序・内容の一致は固定行数の予測コンペだけで要求する。
- missing、NaN、infinite values がない。
- offline/notebook competition では、ルールで許可されていない限り `enable_internet` が false。
- code competition では、公開 test 固有値に依存せず hidden test に差し替え可能である。
- 保存済み model manifest / model 生成物だけで推論でき、コンペ固有の行単位とID規則を満たす。固定行数の予測コンペでは実行時のsampleにIDで完全整列する。

## 提出物の種類

- CSV: header、行数、重複 ID、空値/NaN/Inf、sample 互換性を検証する。
- Zip: member、hidden file、nested path、含まれる CSV があればその内容を検証する。
- Kaggle Notebook: 正のpackage validatorで`kernel-metadata.json`、Notebookの存在、bootstrapとsourceの整合性、internet/GPU flagsを検証する。期待するoutput fileの存在・内容はmetadataだけでは証明できないため、Kaggle実行後のfiles一覧・UIまたは取得済みoutputで別に確認する。

このスキルは提出前検証に集中する。アップロード済みの提出を監視する場合だけ `kaggle-submit-monitor` を使う。
