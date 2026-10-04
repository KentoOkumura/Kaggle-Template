# 検証方針

実験テンプレートが読む fold 数、seed、metric、共通 validation 方針は `project.yml` を正とします。このファイルは設計意図とリークチェックの運用メモです。

## CV 設計

- Fold 作成方法:
- グループキー:
- 層化キー:
- ランダムシード:
- Fold 数:
- メトリック:
- 主な検証コマンド:
  ```bash
  task validate-exp EXP=expXXX_title
  task prepare-kaggle-notebooks EXP=expXXX_title EXTRA_ARGS="--strict"
  task push-kaggle-train EXP=expXXX_title
  task kaggle-logs KERNEL=<username>/<train-kernel-slug>
  ```

## リークチェックリスト

- [ ] 同一グループのデータが train/valid にまたがっていないか。
- [ ] 推論入力に正解ラベルなど、予測時点・評価条件で利用できない情報を混ぜていないか。
- [ ] test 由来の統計量を train に使っていないか。
- [ ] target encoding が fold 外データを参照していないか。
- [ ] augmentation や前処理が validation に不適切に影響していないか。
- [ ] 学習時と推論時の前処理が一致しているか。
- [ ] CV と LB の数値を`metrics.json`へ記録し、乖離の解釈を`result.md`へ記録しているか。
- [ ] 教師生成・内部予測・校正まで含めた分割を記録し、評価側の正解を教師や設定選択へ混ぜていないか。外側の評価結果を繰り返し見て方式を選んだ結果を、未使用データでの評価と呼んでいないか。

時間方向の利用可否は[推論入力の制約](04_data.md#推論入力の制約)で確認する。将来予測では予測時点以降の観測を使わず、系列全体が推論入力として与えられる課題では後続の観測を一律にリークと判定しない。学習側の正解から教師を作ることと、評価側の正解を学習に使うことを区別する。

## CV/LB 乖離の確認

横断比較は自動生成される`experiment_summary.md`で確認し、数値を手作業で転記しません。乖離の原因、比較条件、未解決事項は対応する実験の`result.md`へ記録します。

## 検証判断

- TODO
