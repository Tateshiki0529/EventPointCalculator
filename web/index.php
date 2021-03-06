<html>
	<head>
		<meta charset="UTF-8">
		<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

		<title>イベントポイント計算機</title>

		<link rel="stylesheet" type="text/css" href="css/bootstrap.css">
		<script src="https://kit.fontawesome.com/3e1df4ea0d.js" crossorigin="anonymous"></script>
		<style type="text/css">
			.bs-component + .bs-component {
				margin-top: 1rem;
			}
			#page_top{
				width: 90px;
				height: 90px;
				position: fixed;
				right: 0;
				bottom: 0;
				opacity: 0.6;
			}
			#page_top a{
				position: relative;
				display: block;
				width: 90px;
				height: 90px;
				text-decoration: none;
			}
			#page_top a::before{
				font-family: 'FontAwesome';
				font-weight: 900;
				content: '\f102';
				font-size: 25px;
				color: #3f98ef;
				position: absolute;
				width: 25px;
				height: 25px;
				top: -40px;
				bottom: 0;
				right: 0;
				left: 0;
				margin: auto;
				text-align: center;
			}
			#page_top a::after{
				content: 'PAGE TOP';
				font-size: 13px;
				color: #fff;
				position: absolute;
				top: 45px;
				bottom: 0;
				right: 0;
				left: 0;
				margin: auto;
				text-align: center;
				color: #3f98ef;
			}
			@media (min-width: 768px) {
				.bs-docs-section {
					margin-top: 8em;
				}
				.bs-component {
					position: relative;
				}
				.bs-component .modal {
					position: relative;
					top: auto;
					right: auto;
					bottom: auto;
					left: auto;
					z-index: 1;
					display: block;
				}
				.bs-component .modal-dialog {
					width: 90%;
				}
				.bs-component .popover {
					position: relative;
					display: inline-block;
					width: 220px;
					margin: 20px;
				}
				.nav-tabs {
					margin-bottom: 15px;
				}
				.progress {
					margin-bottom: 10px;
				}
			}
		</style>
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
				</div>
				<div class="col-sm-6 border border-dark rounded p-3">
					<h2 id="form">計算フォーム</h2>
					<div class="form-inline">
						<label for="eventType">イベント種別:&nbsp;</label>
						<select id="eventType" class="form-control" onChange="JavaScript:selectType();">
							<option value="" selected disabled>-- 選択してください --</option>
							<option value="challenge">チャレンジライブイベント</option>
							<option value="versus">対バンライブイベント</option>
							<option value="try">ライブトライ！イベント</option>
							<option value="mission">ミッションライブイベント</option>
						</select>
					</div>
					<div id="type_Challenge">
						<hr>
						<div class="form-inline mb-5">
							<label for="challenge_Point" class="d-inline">欲しいイベントポイント数($p$):&nbsp;</label>
							<input type="number" id="challenge_Point" placeholder="300" class="form-control" onKeyUp="JavaScript:calc('challenge');" inputmode="numeric" pattern="[0-9]+" min="0" />
						</div>
						<div class="form-inline mt-5">
							<label for="challenge_Result" class="d-inline">獲得すべきライブスコア($S$):&nbsp;</label>
							<input type="text" id="challenge_Result" disabled class="form-control" />
						</div>
					</div>
					<div id="type_Versus">
						<hr>
						<div class="form-inline mb-5">
							<label for="versus_Point" class="d-inline">欲しいイベントポイント数($p$):&nbsp;</label>
							<input type="number" id="versus_Point" placeholder="300" class="form-control" onKeyUp="JavaScript:calc('versus');" inputmode="numeric" pattern="[0-9]+" min="0" />
						</div>
						<div class="form-inline m-2 border border-primary rounded p-3">
							<label for="versus_ParticipatePlayerCount">参加人数:&nbsp;</label>
							<select id="versus_ParticipatePlayerCount" onChange="JavaScript:changePlayerCount()" class="mr-3">
								<option value="2">2人</option>
								<option value="3">3人</option>
								<option value="4">4人</option>
								<option value="5" selected>5人</option>
							</select>&nbsp;
							<label for="versus_YourRank">あなたの貢献度ランキング:&nbsp;</label>
							<select id="versus_YourRank" onChange="JavaScript:changePlayerCount()">
								<option value="1" selected>1位</option>
								<option value="2">2位</option>
								<option value="3">3位</option>
								<option value="4">4位</option>
								<option value="5">5位</option>
							</select>
							<label for="versus_ContributePoint" class="d-inline">貢献度ポイント($C$):&nbsp;</label>
							<input type="number" id="versus_ContributePoint" value="60" class="form-control" disabled />
						</div>
						<div class="form-inline mt-5">
							<label for="versus_Result" class="d-inline">獲得すべきライブスコア($S$):&nbsp;</label>
							<input type="text" id="versus_Result" disabled class="form-control" />
						</div>
					</div>
					<div id="type_Try">
						<hr>
						<div class="form-inline mb-5">
							<label for="try_Point" class="d-inline">欲しいイベントポイント数($p$):&nbsp;</label>
							<input type="number" id="try_Point" placeholder="300" class="form-control" onKeyUp="JavaScript:calc('try');" inputmode="numeric" pattern="[0-9]+" min="0" />
						</div>
						<div class="form-inline mt-5">
							<label for="try_Result" class="d-inline">獲得すべきライブスコア($S$):&nbsp;</label>
							<input type="text" id="try_Result" disabled class="form-control" />
						</div>
					</div>
					<div id="type_Mission">
						<hr>
						<div class="form-inline mb-5">
							<label for="mission_Point" class="d-inline">欲しいイベントポイント数($p$):&nbsp;</label>
							<input type="number" id="mission_Point" placeholder="300" class="form-control" onKeyUp="JavaScript:calc('mission');" inputmode="numeric" pattern="[0-9]+" min="0" />
						</div>
						<div class="form-inline m-2 border border-primary rounded p-3">
							<label for="mission_SBPower" class="d-inline">サポートバンド総合力($P$):&nbsp;</label>
							<input type="number" id="mission_SBPower" placeholder="200000" class="form-control" onKeyUp="JavaScript:calc('mission');" inputmode="numeric" pattern="[0-9]+" min="0" />
						</div>
						<div class="form-inline mt-5">
							<label for="mission_Result" class="d-inline">獲得すべきライブスコア($S$):&nbsp;</label>
							<input type="text" id="mission_Result" disabled class="form-control" />
						</div>
					</div>
				</div>
			</div>
			<div class="row mt-3 border border-dark rounded">
				<div class="col-12 p-3 text-center">
					<h2 id="formula">計算式</h2>
					<p>
						$\lfloor\ \rfloor$ … 切り捨て記号($\lfloor\ \rfloor$内の数値は切り捨て)<br>
						$ex)\ \lfloor16.45\rfloor=16$
					</p>
					<div class="border m-1 p-2 border border-primary rounded" style="border-style: dotted !important;">
						<h4>チャレンジライブイベント</h4>
						<p>
							\[
								S=(p-20)\times25000
							\]
							$S$ … 獲得すべきライブスコア<br>
							$p$ … 欲しいイベントポイント<br><br>
							※フリーライブ、特攻キャラ(イベントタイプ・イベントキャラに当てはまらないカード)・ブースト無し時の数値
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
								S=(p-40)\times13000
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
								S=\{p-40-\lfloor P\div3000\rfloor\}\times10000
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
		<script type="text/javascript">
			function allHide() {
				$("#type_Challenge").hide();
				$("#type_Versus").hide();
				$("#type_Try").hide();
				$("#type_Mission").hide();
			}

			function selectType() {
				switch($("#eventType").val()) {
					case "challenge":
						allHide();
						$("#type_Challenge").show();
						break;
					case 'versus':
						allHide();
						$("#type_Versus").show();
						break;
					case 'try':
						allHide();
						$("#type_Try").show();
						break;
					case 'mission':
						allHide();
						$("#type_Mission").show();
						break;
				}
			}

			function calc(type) {
				switch(type) {
					case "challenge":
						var point = parseInt($("#challenge_Point").val());
						var result = (point - 20) * 25000;
						if(result + 24999 <= 0) {
							$("#challenge_Result").val("調整不可 (必要pt: "+result.toLocaleString()+" ～ "+(result+24999).toLocaleString()+")");
						} else if(isNaN(result)) {
							$("#challenge_Result").val("入力が不足しています");
						} else {
							$("#challenge_Result").val(result.toLocaleString()+" ～ "+(result+24999).toLocaleString());
						}
						break;
					case "versus":
						var point = parseInt($("#versus_Point").val());
						var contributePoint = parseInt($("#versus_ContributePoint").val());
						var result = (point - contributePoint) * 5500;
						if(result + 5499 <= 0) {
							$("#versus_Result").val("調整不可 (必要pt: "+result.toLocaleString()+" ～ "+(result+5499).toLocaleString()+")");
						} else if(isNaN(result)) {
							$("#versus_Result").val("入力が不足しています");
						} else {
							$("#versus_Result").val(result.toLocaleString()+" ～ "+(result+5499).toLocaleString());
						}
						break;
					case "try":
						var point = parseInt($("#try_Point").val());
						var result = (point - 40) * 13000;
						if(result + 12999 <= 0) {
							$("#try_Result").val("調整不可 (必要pt: "+result.toLocaleString()+" ～ "+(result+12999).toLocaleString()+")");
						} else if(isNaN(result)) {
							$("#try_Result").val("入力が不足しています");
						} else {
							$("#try_Result").val(result.toLocaleString()+" ～ "+(result+12999).toLocaleString());
						}
						break;
					case "mission":
						var point = parseInt($("#mission_Point").val());
						var power = parseInt($("#mission_SBPower").val());
						var result = (point - 40 - Math.floor(power / 3000)) * 10000;
						if(result + 9999 <= 0) {
							$("#mission_Result").val("調整不可 (必要pt: "+result.toLocaleString()+" ～ "+(result+9999).toLocaleString()+")");
						} else if(isNaN(result)) {
							$("#mission_Result").val("入力が不足しています");
						} else {
							$("#mission_Result").val(result.toLocaleString()+" ～ "+(result+9999).toLocaleString());
						}
						break;
				}
			}

			function changePlayerCount() {
				var playerCount = parseInt($("#versus_ParticipatePlayerCount").val());
				var rank = parseInt($("#versus_YourRank").val());
				switch(playerCount) {
					case 2:
						$("#versus_YourRank > option").remove();
						for(i=1;i<3;i++) {
							$("#versus_YourRank").append($("<option>").html(String(i)+"位").val(String(i)));
						}
						$("#versus_YourRank option[value="+String(rank)+"]").prop("selected", true);
						var rank = parseInt($("#versus_YourRank").val());
						var pointList = [37, 30];
						break;
					case 3:
						$("#versus_YourRank > option").remove();
						for(i=1;i<4;i++) {
							$("#versus_YourRank").append($("<option>").html(String(i)+"位").val(String(i)));
						}
						$("#versus_YourRank option[value="+String(rank)+"]").prop("selected", true);
						var rank = parseInt($("#versus_YourRank").val());
						var pointList = [44, 37, 30];
						break;
					case 4:
						$("#versus_YourRank > option").remove();
						for(i=1;i<5;i++) {
							$("#versus_YourRank").append($("<option>").html(String(i)+"位").val(String(i)));
						}
						$("#versus_YourRank option[value="+String(rank)+"]").prop("selected", true);
						var rank = parseInt($("#versus_YourRank").val());
						var pointList = [52, 44, 37, 30];
						break;
					case 5:
						$("#versus_YourRank > option").remove();
						for(i=1;i<6;i++) {
							$("#versus_YourRank").append($("<option>").html(String(i)+"位").val(String(i)));
						}
						$("#versus_YourRank option[value="+String(rank)+"]").prop("selected", true);
						var rank = parseInt($("#versus_YourRank").val());
						var pointList = [60, 52, 44, 37, 30];
						break;
				}
				var contributePoint = pointList[rank - 1];
				$("#versus_ContributePoint").val(contributePoint);
				calc("versus");
			}
			$(window).on("load", function() {
				allHide();
				$('a[href^="#"]').click(function(){
					let speed = 500;
					let href = $(this).attr("href");
					let target = $(href == "#" || href == "" ? 'html' : href);
					let position = target.offset().top;
					$("body,html").animate({scrollTop:position}, speed, "swing");
					return false;
				});
			});
			$(function() {
				var pageTop = $("#page_top");
				pageTop.hide();
				$(window).scroll(function() {
					console.log($(this).scrollTop());
					if ($(this).scrollTop() > 100) {
						pageTop.fadeIn();
					} else {
						pageTop.fadeOut();
					}
				});
				pageTop.click(function() {
					$("body,html").animate({scrollTop:0}, 500);
					return false;
				});
			})
		</script>

		<script type="text/javascript">
			$('.bs-component [data-toggle="popover"]').popover();
			$('.bs-component [data-toggle="tooltip"]').tooltip();
		</script>
	</body>
</html>