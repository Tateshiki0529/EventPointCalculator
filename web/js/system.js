function allHide() {
	$("#type_Challenge").hide();
	$("#type_Versus").hide();
	$("#type_Try").hide();
	$("#type_Mission").hide();
	$("#divide_input").hide();
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
	$("#divide_input").show();
}

function calc_PtS(type, liveType = null, p = NaN, P = NaN, C = NaN) {
	switch(type) {
		case "challenge":
			if (liveType == null || liveType == "free") {
				var result = (p - 20) * 25000;
			} else if (liveType = "challenge") {
				var result = point - 1000;
				result = result * 300;
			} else {
				return false;
			}
			break;
		case "versus":
			var result = (p - C) * 5500;
			break;
		case "try":
			var result = (p - 40) * 13000;
			break;
		case "mission":
			var result = (p - 40 - Math.floor(P / 3000)) * 10000;
			break;
		default:
			return false;
	}
	return result;
}

function calc(type) {
	switch(type) {
		case "challenge":
			var point = parseInt($("#challenge_Point").val());
			switch($("#challenge_LiveType").val()) {
				case "free":
					var result = calc_PtS("challenge", "free", point);
					if(result + 24999 <= 0) {
						$("#calc_Result").val("調整不可 (必要pt: "+result.toLocaleString()+" ～ "+(result+24999).toLocaleString()+")");
					} else if(isNaN(result)) {
						$("#calc_Result").val("入力が不足しています");
					} else {
						$("#calc_Result").val(result.toLocaleString()+" ～ "+(result+24999).toLocaleString());
						divideCheck();
					}
					break;
				case "challenge":
					var result = calc_PtS("challenge", "challenge", point);
					if(result + 299 <= 0) {
						$("#calc_Result").val("調整不可 (必要pt: "+result.toLocaleString()+" ～ "+(result+299).toLocaleString()+")");
					} else if(isNaN(result)) {
						$("#calc_Result").val("入力が不足しています");
					} else {
						$("#calc_Result").val(result.toLocaleString()+" ～ "+(result+299).toLocaleString());
						divideCheck();
					}
					break;
			}
			break;
		case "versus":
			var point = parseInt($("#versus_Point").val());
			var contributePoint = parseInt($("#versus_ContributePoint").val());
			var result = calc_PtS("versus", null, point, NaN, contributePoint);
			if(result + 5499 <= 0) {
				$("#calc_Result").val("調整不可 (必要pt: "+result.toLocaleString()+" ～ "+(result+5499).toLocaleString()+")");
			} else if(isNaN(result)) {
				$("#calc_Result").val("入力が不足しています");
			} else {
				$("#calc_Result").val(result.toLocaleString()+" ～ "+(result+5499).toLocaleString());
				divideCheck();
			}
			break;
		case "try":
			var point = parseInt($("#try_Point").val());
			var result = calc_PtS("try", null, point);
			if(result + 12999 <= 0) {
				$("#calc_Result").val("調整不可 (必要pt: "+result.toLocaleString()+" ～ "+(result+12999).toLocaleString()+")");
			} else if(isNaN(result)) {
				$("#calc_Result").val("入力が不足しています");
			} else {
				$("#calc_Result").val(result.toLocaleString()+" ～ "+(result+12999).toLocaleString());
				divideCheck();
			}
			break;
		case "mission":
			var point = parseInt($("#mission_Point").val());
			var power = parseInt($("#mission_SBPower").val());
			var result = calc_PtS("mission", null, point, power);
			if(result + 9999 <= 0) {
				$("#calc_Result").val("調整不可 (必要pt: "+result.toLocaleString()+" ～ "+(result+9999).toLocaleString()+")");
			} else if(isNaN(result)) {
				$("#calc_Result").val("入力が不足しています");
			} else {
				$("#calc_Result").val(result.toLocaleString()+" ～ "+(result+9999).toLocaleString());
				divideCheck();
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

function divideCheck() {
	var totalPoint = parseInt($("#"+$("#eventType").val()+"_Point").val());
	var oneTimePoint = Math.floor(totalPoint / parseInt($("#divideCount").val()));

	var pList = [];
	var totalPointBuf = 0;
	for (i=1;i<parseInt($("#divideCount").val());i++) {
		pList.push(oneTimePoint);
		totalPointBuf += oneTimePoint;
	}
	pList.push(totalPoint - totalPointBuf);
	var output = [];
	totalPointBuf = totalPoint;
	pList.forEach(function(value, index) {
		switch($("#eventType").val()) {
			case "challenge":
				switch($("#challenge_LiveType").val()) {
					case "free":
						var result = calc_PtS("challenge", "free", value);
						var resMax = result + 24999;
						break;
					case "challenge":
						var result = calc_PtS("challenge", "challenge", value);
						var resMax = result + 299;
						break;
				}
				break;
			case "versus":
				var point = parseInt($("#versus_Point").val());
				var contributePoint = parseInt($("#versus_ContributePoint").val());
				var result = calc_PtS("versus", null, value, NaN, contributePoint);
				var resMax = result + 5499;
				break;
			case "try":
				var point = parseInt($("#try_Point").val());
				var result = calc_PtS("try", null, value);
				var resMax = result + 12999;
				break;
			case "mission":
				var point = parseInt($("#mission_Point").val());
				var power = parseInt($("#mission_SBPower").val());
				var result = calc_PtS("mission", null, value, power);
				var resMax = result + 9999;
				break;
		}
		totalPointBuf -= value;
		output.push("#"+(index+1)+" "+value+" pts (Remaining: "+totalPointBuf+" pts) | Score: "+result.toLocaleString()+" ～ "+resMax.toLocaleString());
	});
	if ($("#timesDivide").prop("checked")) {
		$("#divideCount").prop("disabled", false);
		$("#divideDetails").prop("disabled", false);
		$("#divideDetails").text(output.join("\n"));
	} else {
		$("#divideCount").prop("disabled", true);
		$("#divideDetails").prop("disabled", true);
	}
}

$(window).on("load", function() {
	allHide();
	selectType();
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
		// console.log($(this).scrollTop());
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