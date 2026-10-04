# 調査レポート

完了した調査結果を探すときは、最初にこのファイルを参照します。対象は、実験構成・モデル説明、OOF／結果EDA、特徴量・failure mode、複数実験比較、論文・公開Notebook調査です。

## 保存ルール

- 人間が読む完了レポートは`docs/surveys/*.md`を正とします。
- 上位仮説を直接扱うレポートはfront matterの`hypotheses`に`HYP-YYYYMMDD-NN`を記録し、本文にも判断対象と結論を記載します。
- front matterの`experiments`は既存の短いID（例: `exp001`）と実験ディレクトリ名の両方を使えます。同じ番号のディレクトリが複数ある場合は、本文で参照する実験の完全な名前を記録します。例えば`exp007_baseline`と`exp007_feature_variant`は別項目として索引化し、両方を扱うレポートには両方を指定します。曖昧な`exp007`だけの指定は検証で拒否します。
- 調査コードと生の表・図は`studies/`、実験実装・実行記録・公式結果は`experiments/`に残し、レポートからリンクします。
- 同じテーマの追調査は原則として既存レポートを更新し、新しい問い・証拠範囲・結論になる場合だけ新しいレポートを作ります。

## レポートの状態

- `draft`: 調査中。placeholderを許可する。
- `final`: 現在参照する完了レポート。
- `superseded`: 後継レポートへ置き換えられた履歴。`superseded_by`に後継ファイル名を記録する。

## 作成・完了手順

1. 同じ問いの既存レポートをこの索引で確認し、新規作成が必要ならdraftを生成します。対象がある場合は`EXTRA_ARGS`に`--hypothesis HYP-YYYYMMDD-NN`、`--experiment expXXX_name`を追加します。複数件は各オプションを繰り返します。

```bash
task new-survey-report SURVEY_TITLE="調査タイトル" SURVEY_SLUG="report-slug" EXTRA_ARGS="--type survey --topic topic"
```

2. 生成されたレポートの本文を完成させ、front matterの`summary`を実際の結論へ置き換えます。本文・summaryのplaceholderをなくし、証拠へのリンクと判断できない範囲を確認します。`hypotheses`と本文の「対応する上位仮説」を一致させ、対象なしの場合は本文に`なし`を記録します。`experiments`も本文が参照する実験と一致させます。
3. 調査内容が完成してからfront matterを`status: final`へ変更します。これは調査レポートの完成を表し、実験や上位仮説の採否判断の代わりにはしません。途中で作業を止める場合は`draft`を維持します。
4. 索引を再生成し、完了検証を実行します。`validate-surveys`は未完了のdraftが残っている場合も失敗します。draftを含む作業途中の構造・索引確認には`validate-template`を使い、完了検証と区別します。

```bash
task update-survey-index
task validate-surveys
```

<!-- BEGIN AUTO SURVEY INDEX -->
## レポート一覧

| 日付 | レポート | 種類 | 上位仮説 | 実験 | トピック | 状態 | 後継 | 一行要約 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| - | - | - | - | - | - | - | - | - |

## 上位仮説別

| キー | レポート |
| --- | --- |
| - | - |

## 実験番号別

| キー | レポート |
| --- | --- |
| - | - |

## 種類別

| キー | レポート |
| --- | --- |
| - | - |

## トピック別

| キー | レポート |
| --- | --- |
| - | - |
<!-- END AUTO SURVEY INDEX -->
