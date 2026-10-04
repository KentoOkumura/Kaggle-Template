# {{ EXPERIMENT_NAME }} 要件と実装方法

この文書を、実装前の契約、実装方法、受け入れ条件の正とする。実行中の進捗は`SESSION_NOTES.md`へ記録し、この文書へ重複させない。

## 実験化の入口・引き継ぎ・承認

- 実験化の入口と承認: TODO (`直接承認`、またはbacklog時の状態と、承認日時 / 依頼メッセージ)
- 移行元backlog: TODO (`N/A` または移行した `backlog/<candidate>.md`。内容の移行確認後、元ファイルと未着手行の削除を`kaggle-strategy`へ引き渡す)
- 対応する上位仮説: TODO (`HYP-YYYYMMDD-NN` または `N/A`。backlogから移行する場合は候補詳細と一致させる)
- 上位仮説のうちこの実験が検証する範囲: TODO
- この実験だけで上位仮説を判断できるか: TODO
- 上位仮説の判断に残る検証: TODO
- 親実験: TODO
- 根拠 / 一次資料 / 参照実装: TODO
- 固定するもの: TODO
- 変更するもの: TODO
- 最小の反証可能な検証: TODO
- この比較で判別する問い: TODO
- 成功条件: TODO
- 停止条件: TODO
- 結果別の次の行動: TODO（支持・反証・判断不能の場合の次の確認。既存の承認範囲と追加承認が必要な操作）
- 実行しないこと: TODO
- 未決事項: TODO（実装開始時は`なし`。`AGENTS.md`に従い、設計上の未決事項と下記の測定待ち・先行条件を区別する）
- 調査・実行時に確認する事項: TODO（未測定の精度・費用・生成物SHAと確認方法。なければ`なし`）
- 先行条件 / 依存: TODO（必要な入力・生成元と、揃うまで実行できない工程。なければ`なし`）
- backlog記録から解釈を変更した箇所とユーザー承認: TODO (`N/A` または承認日時 / 依頼メッセージ)

## 判断履歴

- YYYY-MM-DD: TODO（backlogでの判断、実験化承認、契約変更の承認を時系列で移す）

## 手法契約

実装区分は`docs/glossary.md`に定義したこのリポジトリ内の管理用ラベルを使う。ユーザーへの説明では、先に実装する処理と省略する処理を具体的に示し、その後に必要ならラベルを添える。

- 依頼原文: TODO
- 期待する成果: TODO
- input: TODO
- target / objective: TODO
- output: TODO
- loss: TODO
- decode: TODO
- context unit: TODO (`row`、`window`、`whole-group`、`set`、`entity` など)
- 実装区分: TODO (`faithful`、`staged-faithful`、`proxy`)
- 省略する機構と理由: TODO
- proxyで検証できない主張: TODO
- proxyの場合のユーザー承認: TODO (`N/A` または承認日時 / 依頼メッセージ)
- この実験が支持 / 棄却できる主張: TODO
- この実験では判断できない主張: TODO

## 実装方法

- アプローチ: TODO
- inputの実装箇所と変換: TODO
- target / objectiveの構築箇所: TODO
- outputの生成箇所と表現: TODO
- lossの実装箇所: TODO
- decode / postprocessの実装箇所: TODO
- context unitを保つ処理箇所: TODO
- 変更するファイル / component: TODO
- 固定事項を保つ確認方法: TODO
- 検証の処理範囲: TODO（初回比較で保つ中核、縮小後にも残る対象現象、最終処理まで通す範囲、未判定となる効果）
- 予備診断と結果別の行動: TODO（必要な場合だけ。判別する問いと本命の着手・修正・中止への影響、棄却できない効果。不要なら`なし`）
- 全工程の依存関係・資源上限・実測記録: TODO（前処理・必要な対照・学習・最終評価・契約に含む推論。確定した資源制約と、実行後に時間・進捗を確認する方法。事前の所要時間予測は記入しない）
- 長い処理の保存・再開方法: TODO（比較条件を保つ分割単位、中間生成物、入力・設定・版の照合。不要なら理由）
- 参照sourceとの一致を確認するテスト: TODO
- 承認済み差分を確認するテスト: TODO

## 探索幅とpivot判定

- 変更class: TODO (`parameter`、`add-only`、`selector-only`、`postprocess`、`mechanism`、`representation`)
- 本命の初回比較の実施状況と残る障害: TODO（診断・微調整で未実施なら理由。既存記録への参照でよい）
- positiveなoracle headroom / coverage / 誤差非相関性: TODO
- 比較したtarget、output、decode、context unitを変える案: TODO
- 小改善の継続またはpivotを選ぶ根拠: TODO
- `kaggle-idea-forge` の実行要否と根拠: TODO

## 再現性・リスク

- seed policy: TODO (`docs/06_reproducibility.md` を参照)
- stochastic 処理の有無: TODO
- stochastic feature generation / augmentation / seed bagging の有無: TODO
- 並列処理と乱数の関係: TODO
- CPU/GPU runtime と deterministic flags: TODO
- train cache / test feature regeneration の SHA 記録方針: TODO
- model manifest / prediction / submission SHA 記録方針: TODO
- Kaggle package bootstrap 確認方針: TODO
- リークリスク: TODO
- CV/LB 不一致リスク: TODO
- ランタイム/メモリリスク: TODO
- 再現性リスク: TODO
- 手法忠実性リスク: TODO
- 過度な縮小 / proxy化リスク: TODO

## 受け入れ基準

- [ ] 手法契約の `input / target / output / loss / decode / context unit` がコードと一致する。
- [ ] 実装区分と実験名が実装した機構を正確に表す。
- [ ] `proxy` の場合は、省略点、検証不能な主張、ユーザー承認が記録されている。
- [ ] backlogから移行した場合は、根拠、親実験との差分、成功条件、停止条件、実行しないこと、判断履歴が欠落していない。
- [ ] `config.yaml`の`lineage.hypothesis_id`と`lineage.backlog_candidate`がこの文書と一致する。
- [ ] 実験固有テストと静的検証が通る。
- [ ] 予定した比較の実施範囲と未完了部分を明示し、判別できた問い・残った問い・推奨する次の行動を`result.md`へ記録する。
- [ ] deterministic anchor として扱う場合は、必要なSHAとKaggle kernel versionを`metrics.json`の`evidence`へ記録する。
- [ ] gzip生成物を比較する場合は、decompressed content SHAを主証拠として記録する。
