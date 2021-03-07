![GitHub issues](https://img.shields.io/github/issues/Tateshiki0529/EventPointCalculator)
# EventPointCalculator
ガルパのイベントポイントを計算する。
# 更新履歴
- 2021/03/07 v1.4.0(Commit: [cc50d8c](https://github.com/Tateshiki0529/EventPointCalculator/commit/cc50d8cb5857d00d7353a382cd37c3905d84e332))
	- イベントポイントを小分けにして数回に分けて調節できるように機能を追加(Beta)
		- [#2](https://github.com/Tateshiki0529/EventPointCalculator/issues/2) より(自問自答やめい)。Issueってまるでメモ帳のように…()
- 2021/03/07 v1.2.0(Commit: [18aef03](https://github.com/Tateshiki0529/EventPointCalculator/commit/18aef03dceafa07b7c8123c55f469f5b252fa59e))
	- イベント期間中…自動選択するように調整 <- 「イベント期間中」->「イベント開始日の11時20分～イベント終了まで」に変更 (web/index.php:100)
		- アプリ内DLがこの時間帯で入るためです。あとはBestdori等のリーク情報が公開される時間でもあるため… 
	- チャレンジライブイベントのチャレンジライブの調整式を追加(Beta) (web/index.php:118-124, js/system.js:33-54 etc.)
		- **おそらく**index.php:216の式で合ってると思います。何かあればIssue立ててください(他人任せ)。
- 2021/03/07 v1.1.0(Commit: [55df55a](https://github.com/Tateshiki0529/EventPointCalculator/commit/55df55a598dce49ebb01aff2e30dffb8e4e83c7d))
	- 最新イベント情報を取得するコードを追加
	- イベント期間中は当該イベント種別を自動選択するように調整
- 2021/03/07 v1.0.1 (Commit: [6613e28](https://github.com/Tateshiki0529/EventPointCalculator/commit/6613e280516d1ed40be32578d76a9660a319bcdd))
	- アイコンの追加
	- 計算式の修正
	- 計算タイミングの調整
- 2021/03/07 v1.0.0 (Commit: [3dc520e](https://github.com/Tateshiki0529/EventPointCalculator/commit/3dc520eac04ec9d8f0570a544d04a4fe157a24e3))
	- サイト公開