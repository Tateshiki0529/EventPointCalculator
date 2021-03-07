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
});
$('.bs-component [data-toggle="popover"]').popover();
$('.bs-component [data-toggle="tooltip"]').tooltip();