_import("billshare");$(document).ready(function(){

	Date.prototype.format = function(fmt) {
		var o = {
			"M+" : this.getMonth()+1,                 //月份
			"d+" : this.getDate(),                    //日
			"h+" : this.getHours(),                   //小时
			"m+" : this.getMinutes(),                 //分
			"s+" : this.getSeconds(),                 //秒
			"q+" : Math.floor((this.getMonth()+3)/3), //季度
			"S"  : this.getMilliseconds()             //毫秒
		};
		if(/(y+)/.test(fmt)) {
			fmt=fmt.replace(RegExp.$1, (this.getFullYear()+"").substr(4 - RegExp.$1.length));
		}
		for(var k in o) {
			if(new RegExp("("+ k +")").test(fmt)){
				fmt = fmt.replace(RegExp.$1, (RegExp.$1.length==1) ? (o[k]) : (("00"+ o[k]).substr((""+ o[k]).length)));
			}
		}
		return fmt;
	}

	$("#btnSearch").click(function(){
		if(!$("#txtStrMonth").val()){showMessage("请先选择需要查询的月份!")}else{$("#frmBillMonth")[0].submit()
	}return false});

	$("#txtStrMonth,#aShowSelect").click(function(){$("#divSelectMonth").toggle();return false});

	$("#btnEnterMonth").click(function(){
		$("#txtStrMonth").val(($("#selYear").val()+"-"+$("#selMonth").val()));
		$("#divSelectMonth").hide();
		$("#frmBillMonth")[0].submit();
		return false}
	);

	$("#btnCancelMonth").click(function(){$("#divSelectMonth").hide();return false})

	$("#btnNextMonth").click(function(){
		if(!$("#txtStrMonth").val()){showMessage("请先选择需要查询的月份!")}else{
			strDate = $("#txtStrMonth").val()+"-1";
			now = new Date(strDate.replace(/\-/g,"/"));
			nextMonth =new Date( now.setMonth(now.getMonth() + 1));
			$("#txtStrMonth").val(nextMonth.format("yyyy-M"));
			$("#frmBillMonth")[0].submit()
	}return false});

	$("#btnPrevMonth").click(function(){
		if(!$("#txtStrMonth").val()){showMessage("请先选择需要查询的月份!")}else{
			strDate = $("#txtStrMonth").val()+"-1";
			now = new Date(strDate.replace(/\-/g,"/"));
			prevMonth =new Date( now.setMonth(now.getMonth() - 1));
			strMonth = prevMonth.getFullYear() + "-" + (prevMonth.getMonth()+1)
			$("#txtStrMonth").val(prevMonth.format("yyyy-M"));
			$("#frmBillMonth")[0].submit();
	}return false});

});