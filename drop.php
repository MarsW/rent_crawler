<html>
<head>
	<meta charset="UTF-8">
	<title>591租屋-屏棄清單</title>
	<script src="http://code.jquery.com/jquery.js"></script>
	<link rel="stylesheet" type="text/css" href="//cdn.datatables.net/1.10.5/css/jquery.dataTables.css">
	<script type="text/javascript" charset="utf8" src="//cdn.datatables.net/1.10.5/js/jquery.dataTables.js"></script>
</head>
<body>
	<a href="./index.php" target="_blank">新物件、喜好清單</a>
	<?php
			$username="";
			$password="";
			$database="";
			$ip="";

			$connection=mysql_connect ($ip, $username, $password) or die("Not connected : " . mysql_error());
			$db_selected = mysql_select_db($database, $connection) or die("Can\'t use db : " . mysql_error());

			mysql_query("SET NAMES utf8");
			$sql="SELECT * FROM `rent` WHERE (`rating_marsw`<0 AND `rating_marsw` IS NOT NULL) OR (`rating_akoung`<0 AND `rating_akoung` IS NOT NULL) OR (`rating_awoo`<0 AND `rating_awoo` IS NOT NULL) OR (`rating_fufu`<0 AND `rating_fufu` IS NOT NULL)";
			$result = mysql_query($sql) or die('MySQL query error'.$sql."<br>".mysql_error()."<br>");

			echo '<table border="1" cellpadding="1" cellspacing="0" class="table table-striped" id="data_table" style="font-size: small">';

			echo '<thead style="background-color: #ffe"><tr>';
			echo '<th>編號</th>';
			echo '<th>租金</th>';
			echo '<th>格局</th>';
			echo '<th>傢俱?</th>';
			echo '<th>地址</th>';
			echo '<th>照片</th>';
			echo '<th>通勤:老翁</th>';
			echo '<th>通勤:阿嗚</th>';
			echo '<th>通勤:貢丸</th>';
			echo '<th>備註</th>';
			echo '<th>評分_老翁</th>';
			echo '<th>評分_貢丸</th>';
			echo '<th>評分_阿嗚</th>';
			echo '<th>評分_fufu</th>';
			echo '<th>更新時間</th>';
			echo '</tr></thead><tbody>';

			while($row = mysql_fetch_array($result)){ 
					echo '<tr>';
					echo '<td>',$row['sn'],'</td>';
					echo '<td><div class="price" id="price-',$row['sn'],'">',$row['price'],'</div></td>';
					echo '<td><div class="layout" id="layout-',$row['sn'],'">',$row['layout'],'</div></td>';
					echo '<td><div class="furniture" id="furniture-',$row['sn'],'">',$row['furniture'],'</div></td>';
					echo '<td><a href="',$row['url'],'" target="_blank">',$row['address'],'</a></td>';
					echo '<td><img src="',$row['img_url'],'" width="92px" ><img></td>';
					echo '<td><div class="marsw" id="marsw-',$row['sn'],'">',$row['marsw'],'</div></td>';
					echo '<td><div class="awooo" id="awooo-',$row['sn'],'">',$row['awooo'],'</div></td>';
					echo '<td><div class="akoung" id="akoung-',$row['sn'],'">',$row['akoung'],'</div></td>';
					echo '<td><div class="note" id="note-',$row['sn'],'">',$row['note'],'</div></td>';
					echo '<td><div class="rating_marsw" id="rating_marsw-',$row['sn'],'">',$row['rating_marsw'],'</div></td>';
					echo '<td><div class="rating_akoung" id="rating_akoung-',$row['sn'],'">',$row['rating_akoung'],'</div></td>';
					echo '<td><div class="rating_awoo" id="rating_awoo-',$row['sn'],'">',$row['rating_awoo'],'</div></td>';
					echo '<td><div class="rating_fufu" id="rating_fufu-',$row['sn'],'">',$row['rating_fufu'],'</div></td>';
					echo '<td><div class="mtime">',$row['mtime'],'</td>';
					echo '</tr>';
				
			}
			echo '</tbody></table>';
	?>
	<script type="text/javascript" src="./jquery.jeditable.js"></script>
	<script>
		$(document).ready( function () {
			//資料排序
		    var oTable = $('#data_table').DataTable({  
				"bJQueryUI": false,  //掛UI的視覺效果
				"bLengthChange":true, //控制是否要在表格左上角顯示一個可以更改每頁顯示列數的下拉式選單
				"bSortClasses": 1,
				"aLengthMenu":[[10,30,50,-1],[10,30,50,"All"]], //分頁方式設定
				"iDisplayLength":30, //預設筆數
				"sPaginationType": "full_numbers",  //頁碼
				"sDom": 'T&gt;lfrtip',
				"order": [[ 0, "asc" ]], //排序
				"oLanguage": {
					//"sSearch": "Search all columns:" //命別名
				},
				"oTableTools": {  //資料匯出
					"aButtons": [
						"xls","print"
						// ,//csv,pdf
						// {
						// "sExtends":    "collection",
						// "sButtonText": "Save",
						// "aButtons":    [ "xls" ]  //csv,pdf
						// }
					]
					}
				// , "fnDrawCallback": function( oSettings ) {
				//		$("#table1").show();
				// }

			});
			//資料編輯
			oTable.$(".price").editable("save.php", {
				cancel: '取消',
				submit: '修改',
				indicator: "儲存中...",
				width: "40px"
			});
			oTable.$(".furniture").editable("save.php", {
				cancel: '取消',
				submit: '修改',
				indicator: "儲存中...",
				width: "40px"
			});
			oTable.$(".marsw").editable("save.php", {
				cancel: '取消',
				submit: '修改',
				indicator: "儲存中...",
				width: "40px"
			});
			oTable.$(".awooo").editable("save.php", {
				cancel: '取消',
				submit: '修改',
				indicator: "儲存中...",
				width: "40px"
			});
			oTable.$(".akoung").editable("save.php", {
				cancel: '取消',
				submit: '修改',
				indicator: "儲存中...",
				width: "40px"
			});
			oTable.$(".note").editable("save.php", {
				cancel: '取消',
				submit: '修改',
				indicator: "儲存中...",
				width: "80px"
			});
			oTable.$(".rating_marsw").editable("save.php", {
				cancel: '取消',
				submit: '修改',
				indicator: "儲存中...",
				width: "10px"
			});
			oTable.$(".rating_akoung").editable("save.php", {
				cancel: '取消',
				submit: '修改',
				indicator: "儲存中...",
				width: "10px"
			});
			oTable.$(".rating_awoo").editable("save.php", {
				cancel: '取消',
				submit: '修改',
				indicator: "儲存中...",
				width: "10px"
			});
			oTable.$(".rating_fufu").editable("save.php", {
				cancel: '取消',
				submit: '修改',
				indicator: "儲存中...",
				width: "10px"
			});
			
		} );
	</script>
	
	
</body>
</html>