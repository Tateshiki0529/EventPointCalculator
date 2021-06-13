<?php 

	/**
	 * EventPointCalculator 画像表示スクリプト (img.php)
	 * 
	 * 画像を表示する。SSL非対応のサイトから画像を持ってくる際に利用する。
	 * 
	 * @access private
	 * @author Tateshiki0529
	 * @copyright Tateshiki0529 All Rights Reserved.
	 * @package EventPointCalculator
	 * @category Grab
	**/

	// デバッグ用
	header("Content-Type: application/json");

	// 画像URLを取得する
	$imgUrl = urldecode($_GET["url"]);

	if (!isset($imgUrl)) { // 不正アクセス
		header("HTTP/1.1 400 Bad Request");
		exit();
	}
	$imgData = file_get_contents($imgUrl, false, stream_context_create(["http" => ["ignore_errors" => true]]));
	if (strpos($http_response_header[0], "200") !== false) { // 200 OK
		$imgType = getimagesizefromstring($imgData);
		$imgWidth = $imgType[0];
		$imgHeight = $imgType[1];
		$imgMime = $imgType["mime"];

		// 画像生成
		$canvas = imagecreatefromstring($imgData);
		header("Content-Type: {$imgMime}");
		if (strpos($imgMime, "png") !== false) {
			imagepng($canvas);
		} elseif (strpos($imgMime, "jpg") !== false or strpos($imgMime, "jpeg") !== false) {
			imagejpeg($canvas);
		} elseif (strpos($imgMime, "bmp") !== false) {
			imagewbmp($canvas);
		} elseif (strpos($imgMime, "gif") !== false) {
			imagegif($canvas);
		}
		imagedestroy($canvas);
	} else { // それ以外
		// header("HTTP/1.1 500 Internal Server Error");
		// exit();
		var_dump($imgData);
	}

?>