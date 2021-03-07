<?php
	// latest event retriever
	$eventUrl = "https://bandori.party/api/events/";
	$accessDate = date("Y/m/d H:i:s");
	$eventData = json_decode(file_get_contents($eventUrl), true);
	$latestEvent = $eventData["results"][0];
	$eventTypeActive = "";
?>
<html>
	<head>
		<meta charset="UTF-8">
		<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

		<title>イベントポイント計算機</title>

		<link rel="stylesheet" type="text/css" href="css/bootstrap.css">
		<link rel="stylesheet" type="text/css" href="css/style.css">
		<script src="https://kit.fontawesome.com/3e1df4ea0d.js" crossorigin="anonymous"></script>
		<script type="text/x-mathjax-config">	
			MathJax.Hub.Config({
				showProcessingMessages: false,
				tex2jax: { inlineMath: [['$','$'],['\\(','\\)']] }
			});
		</script>
		<script type="text/javascript" id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@2/MathJax.js?config=TeX-MML-AM_HTMLorMML"></script>
	</head>
	<body>
		<header>
			<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
				<a class="navbar-brand" href="#">イベントポイント計算機</a>
				<button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarColor02" aria-controls="navbarColor02" aria-expanded="false" aria-label="Toggle navigation">
					<span class="navbar-toggler-icon"></span>
				</button>

				<div class="collapse navbar-collapse" id="navbarColor02">
					<ul class="navbar-nav mr-auto">
						<li class="nav-item">
							<a class="nav-link" href="#banner"><i class="fas fa-home"></i> イベントポイント計算機</a>
						</li>
						<li class="nav-item">
							<a class="nav-link" href="#usage"><i class="fas fa-book-open"></i> 使い方</a>
						</li>
						<li class="nav-item">
							<a class="nav-link" href="#form"><i class="fas fa-calculator"></i> 計算フォーム</a>
						</li>
						<li class="nav-item">
							<a class="nav-link" href="#formula"><i class="fas fa-pen-alt"></i> 計算式</a>
						</li>
						<li class="nav-item">
							<a class="nav-link" href="https://twitter.com/@T_BanGDreamer" target="_blank"><i class="fab fa-twitter"></i> 開発者Twitter <i class="fas fa-external-link-alt"></i></a>
						</li>
						<li class="nav-item">
							<a class="nav-link" href="https://github.com/Tateshiki0529/EventPointCalculator" target="_blank"><i class="fab fa-github"></i> GitHub <i class="fas fa-external-link-alt"></i></a>
						</li>
						<li class="nav-item">
							<a class="nav-link" href="https://ttsk3.net/594" target="_blank"><i class="fas fa-file-alt"></i> ブログ記事(更新履歴) <i class="fas fa-external-link-alt"></i></a>
						</li>
					</ul>
				</div>
			</nav>
		</header>
		<div class="container">
			<div class="page-header">
				<div class="row my-4">
					<div class="col-12">
						<h1 class="display-5" id="banner">イベントポイント計算機</h1>
						<p class="lead">ガルパのイベントポイントをただただ計算するだけのサイト。</p>
					</div>
				</div>
			</div>
			<div class="row">
				<div class="col-sm-6 p-3 border border-dark rounded">
					<h2 id="usage">使い方</h2>
					<ol>
						<li>イベントの種類を選択する。</li>
						<li>値を入力する。</li>
						<li>結果を見る。</li>
					</ol>
					<p>それだけ。</p>
					<h2 id="notice">ひとこと</h2>
					<ol>
						<li>チャレンジライブイベントのライブ種別:協力プレイについて</li>
						<ul>
							<li>ポイントを割る定数(割ってスコアボーナスとする)が全体スコアに対して60000～100000(?)程度変化するらしい</li>
							<ul>
								<li>変化の規則性がわかるまで実装予定はありません。てかどうしようもないです。</li>
							</ul>
						</ul>
						<li>小分けシステムについて</li>
						<ul>
							<li>システムから書き直すのでしばらくお待ちくだされ。</li>
						</ul>
					</ol>
				</div>
				<div class="col-sm-6 border border-dark rounded p-3">
					<h2 id="form">計算フォーム</h2>
					<?php if(isset($latestEvent)): ?>
						<p class="alert-primary p-3 rounded">
							<i class="far fa-check-circle"></i> 最新イベント情報取得に成功(<?=$accessDate;?>)。<br><br>
							イベントタイトル: <?=$latestEvent["japanese_name"];?><br>
							<?php
								$startDate = Datetime::createFromFormat(DateTime::ATOM, $latestEvent["start_date"])->setTimezone(new DateTimeZone("Asia/Tokyo"));
								$endDate = Datetime::createFromFormat(DateTime::ATOM, $latestEvent["end_date"])->setTimezone(new DateTimeZone("Asia/Tokyo"));
								$eventTypeActive = $latestEvent["i_type"];
								$eventTypeList = [
									"challenge_live" => "チャレンジライブイベント",
									"vs_live" => "対バンライブイベント",
									"live_goals" => "ライブトライ！イベント",
									"mission_live" => "ミッションライブイベント"
								];
							?>
							イベント期間: <?=$startDate->format("Y/m/d(D.) H:i");?> ～ <?=$endDate->format("Y/m/d(D.) H:i");?><br>
							イベントタイプ: <?=$eventTypeList[$eventTypeActive];?>
							<?php if (strtotime($startDate->format("Y/m/d")." 11:20") >= time()) {
								$eventTypeActive = "";
								echo "<br><br>(イベント開始日の11時20分以降は種別が自動選択されます)";
							} ?>
						</p>
					<?php endif; ?>
					<div class="form-inline">
						<label for="eventType">イベント種別:&nbsp;</label>
						<select id="eventType" class="form-control" onChange="JavaScript:selectType();">
							<option value="" <?=($eventTypeActive == "")?"selected":"";?> disabled>-- 選択してください --</option>
							<option value="challenge"<?=($eventTypeActive == "challenge_live")?" selected":"";?>>チャレンジライブイベント</option>
							<option value="versus"<?=($eventTypeActive == "vs_live")?" selected":"";?>>対バンライブイベント</option>
							<option value="try"<?=($eventTypeActive == "live_goals")?" selected":"";?>>ライブトライ！イベント</option>
							<option value="mission"<?=($eventTypeActive == "mission_live")?" selected":"";?>>ミッションライブイベント</option>
						</select>
					</div>
					<div id="type_Challenge">
						<hr>
						<div class="form-inline">
							<label for="challenge_LiveType" class="d-inline">ライブ種別:&nbsp;</label>
							<select id="challenge_LiveType" onChange="JavaScript:calc('challenge');" class="form-control">
								<option value="free" selected>フリーライブ</option>
								<option value="challenge">チャレンジライブ(Beta)</option>
							</select>
						</div>
						<div class="form-inline mb-5">
							<label for="challenge_Point" class="d-inline">欲しいイベントポイント数($p$):&nbsp;</label>
							<input type="number" id="challenge_Point" placeholder="300" class="form-control" onKeyUp="JavaScript:calc('challenge');" onChange="JavaScript:calc('challenge');" inputmode="numeric" pattern="[0-9]+" min="0" />
						</div>
					</div>
					<div id="type_Versus">
						<hr>
						<div class="form-inline mb-5">
							<label for="versus_Point" class="d-inline">欲しいイベントポイント数($p$):&nbsp;</label>
							<input type="number" id="versus_Point" placeholder="300" class="form-control" onKeyUp="JavaScript:calc('versus');" onChange="JavaScript:calc('versus'); inputmode="numeric" pattern="[0-9]+" min="0" />
						</div>
						<div class="form-inline m-2 border border-primary rounded p-3">
							<label for="versus_ParticipatePlayerCount">参加人数:&nbsp;</label>
							<select id="versus_ParticipatePlayerCount" onChange="JavaScript:changePlayerCount()" class="mr-3 form-control">
								<option value="2">2人</option>
								<option value="3">3人</option>
								<option value="4">4人</option>
								<option value="5" selected>5人</option>
							</select>&nbsp;
							<label for="versus_YourRank">あなたの貢献度ランキング:&nbsp;</label>
							<select id="versus_YourRank" onChange="JavaScript:changePlayerCount()" class="form-control">
								<option value="1" selected>1位</option>
								<option value="2">2位</option>
								<option value="3">3位</option>
								<option value="4">4位</option>
								<option value="5">5位</option>
							</select>
							<label for="versus_ContributePoint" class="d-inline">貢献度ポイント($C$):&nbsp;</label>
							<input type="number" id="versus_ContributePoint" value="60" class="form-control" disabled />
						</div>
					</div>
					<div id="type_Try">
						<hr>
						<div class="form-inline mb-5">
							<label for="try_Point" class="d-inline">欲しいイベントポイント数($p$):&nbsp;</label>
							<input type="number" id="try_Point" placeholder="300" class="form-control" onKeyUp="JavaScript:calc('try');" onChange="JavaScript:calc('try');" inputmode="numeric" pattern="[0-9]+" min="0" />
						</div>
					</div>
					<div id="type_Mission">
						<hr>
						<div class="form-inline mb-5">
							<label for="mission_Point" class="d-inline">欲しいイベントポイント数($p$):&nbsp;</label>
							<input type="number" id="mission_Point" placeholder="300" class="form-control" onKeyUp="JavaScript:calc('mission');" onChange="JavaScript:calc('mission');" inputmode="numeric" pattern="[0-9]+" min="0" />
						</div>
						<div class="form-inline m-2 border border-primary rounded p-3">
							<label for="mission_SBPower" class="d-inline">サポートバンド総合力($P$):&nbsp;</label>
							<input type="number" id="mission_SBPower" placeholder="200000" class="form-control" onKeyUp="JavaScript:calc('mission');" onChange="JavaScript:calc('mission');" inputmode="numeric" pattern="[0-9]+" min="0" />
						</div>
					</div>
					<div class="result_form">
						<div class="form-group mt-5">
							<label for="calc_Result" class="d-inline">獲得すべきライブスコア($S$):&nbsp;</label>
							<input type="text" id="calc_Result" disabled class="form-control" />
						</div>
						<hr>
						<div class="custom-control custom-checkbox">
							<input type="checkbox" id="timesDivide" class="custom-control-input" onChange="JavaScript:divideCheck();">
							<label class="custom-control-label" for="timesDivide">小分けにしてみる</label>
						</div>
						<div class="form-inline mt-5">
							<label for="" class="d-inline">小分け回数:&nbsp;</label>
							<select id="divideCount" class="form-control" disabled onChange="JavaScript:divideCheck();">
								<?php 
									foreach(range(1, 99) as $v) {
										echo "<option value=\"".($v+1)."\">".($v+1)."回</option>\n";
									}
								?>
							</select>
						</div>
						<div class="form-group">
							<label for="divideDetails">小分け詳細:</label>
							<textarea id="divideDetails" cols="30" rows="10" class="form-control" disabled readonly></textarea>
						</div>
					</div>
				</div>
			</div>
			<div class="row mt-3 border border-dark rounded">
				<div class="col-12 p-3 text-center">
					<h2 id="formula">計算式</h2>
					<p>
						$\newcommand{\bm}[1]{{\boldsymbol{\it #1}}}$
						$\lfloor\ \rfloor$ … 切り捨て記号($\lfloor\ \rfloor$内の数値は切り捨て)<br>
						$ex)\ \lfloor16.45\rfloor=16$<br>
						$\bm{\underline{n}}$ … 基本ポイント(これ以下の指定・調節は不可)
					</p>
					<div class="border m-1 p-2 border border-primary rounded" style="border-style: dotted !important;">
						<h4>チャレンジライブイベント</h4>
						<h6>フリーライブ</h6>
						<p>
							\[
								S=(p-\bm{\underline{20}})\times25000
							\]
							$S$ … 獲得すべきライブスコア<br>
							$p$ … 欲しいイベントポイント<br><br>
							※フリーライブ、特攻キャラ(イベントタイプ・イベントキャラに当てはまらないカード)・ブースト無し時の数値
						</p>
						<hr>
						<h6>チャレンジライブ (Beta)</h6>
						<p>
							\[
								p=\lfloor S\div300\rfloor+\bm{\underline{1000}}
							\]
							$S$ … 獲得すべきライブスコア<br>
							$p$ … 欲しいイベントポイント<br><br>
							※チャレンジライブ、ブースト無し時の数値<br>
							<span class="bg-warning p-1 rounded"><span class="text-danger">Warning:</span> 独自に算出した数式を利用しています。</span><br>
							<span class="bg-warning p-1 rounded">確実な数式ではないためこの数式・計算機を使ったスコアの誤差が発生しても当サイトは一切の責任を負いません。</span>
						</p>
					</div>
					<div class="border m-1 p-2 border border-primary rounded" style="border-style: dotted !important;">
						<h4>対バンライブイベント</h4>
						<p>
							\[
								S=(p-C)\times5500
							\]
							$S$ … 獲得すべきライブスコア<br>
							$p$ … 欲しいイベントポイント<br>
							$C$ … 貢献度ポイント<br><br>
							※対バンライブ、ブースト無し時の数値<br>
							※貢献度ランキングによる定数$C$一覧:
						</p>
						<table class="table table-bordered">
							<thead class="table-dark">
								<tr>
									<th>貢献度ランキング</th>
									<th>貢献度ポイント($C$の値)</th>
								</tr>
							</thead>
							<tbody>
								<tr>
									<th>1位</th>
									<td>60pts</td>
								</tr>
								<tr>
									<th>2位</th>
									<td>52pts</td>
								</tr>
								<tr>
									<th>3位</th>
									<td>44pts</td>
								</tr>
								<tr>
									<th>4位</th>
									<td>37pts</td>
								</tr>
								<tr>
									<th>5位</th>
									<td>30pts</td>
								</tr>
							</tbody>
						</table>
						ただし参加人数によって$C$の最大が変動する(3人の場合、3,4,5位のスコアが適用される)
					</div>
					<div class="border m-1 p-2 border border-primary rounded" style="border-style: dotted !important;">
						<h4>ライブトライ！イベント</h4>
						<p>
							\[
								S=(p-\bm{\underline{40}})\times13000
							\]
							$S$ … 獲得すべきライブスコア<br>
							$p$ … 欲しいイベントポイント<br><br>
							※フリーライブ、特攻キャラ(イベントタイプ・イベントキャラに当てはまらないカード)・ブースト無し時の数値
						</p>
					</div>
					<div class="border m-1 p-2 border border-primary rounded" style="border-style: dotted !important;">
						<h4>ミッションライブイベント</h4>
						<p>
							\[
								S=\{p-\bm{\underline{40}}-\lfloor P\div3000\rfloor\}\times10000
							\]
							$S$ … 獲得すべきライブスコア<br>
							$p$ … 欲しいイベントポイント<br>
							$P$ … サポートバンド総合力<br><br>
							※フリーライブ、特攻キャラ(イベントタイプ・イベントキャラに当てはまらないカード)・ブースト無し時の数値
						</p>
					</div>
					<p>※ブーストの$n$倍には小数計算も含まれるため、イベントポイント調整には不適</p>
				</div>
			</div>
		</div>
		<div id="page_top"><a href="#"></a></div>
		<footer class="bg-dark text-center mt-3 p-3">
			<small class="text-light">Copyright &copy; <script>start=2021;if(new Date().getFullYear()==start){document.write("2021");}else{document.write("2021-"+new Date().getFullYear());}</script> <a target="_blank" href="https://ttsk3.net/">Tateshiki0529</a>.</small>
			<!--タグはここから--><table border="0" cellspacing="0" cellpadding="0" style="margin-left: auto;margin-right: auto;"><tr><td align="center"><a href="http://www.rays-counter.com/"><img src="http://www.rays-counter.com/d480_f6_028/6043d509817ed/" alt="アクセスカウンター" border="0"></a></td></tr><tr><td align="center"><img src="http://www.rays-counter.com/images/counter_01.gif" border="0"><img src="http://www.rays-counter.com/images/counter_02.gif" border="0"><img src="http://www.rays-counter.com/images/counter_03.gif" border="0" alt=""><img src="http://www.rays-counter.com/images/counter_04.gif" border="0"><img src="http://www.rays-counter.com/images/counter_05.gif" border="0" ></td></tr></table><!--ここまで-->
		</footer>

		<script src="https://code.jquery.com/jquery-3.6.0.min.js" integrity="sha256-/xUj+3OJU5yExlq6GSYGSHk7tPXikynS7ogEvDej/m4=" crossorigin="anonymous"></script>
		<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
		<script src="./js/bootstrap.min.js"></script>
		<script type="text/javascript" src="./js/system.js?<?=time();?>"></script>
	</body>
</html>