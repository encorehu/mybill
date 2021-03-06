_import("calendar");
_import("billshare");
_import("myext");
$(document).ready(function(){
	if(!$("#hdnId").val()||$("#hdnId").val()==0){
		$(".topbar").removeClass("on");
		$("#liTop6").addClass("on")
	}

	$("#txtRecDate,#aRecDate").click(function(){SelectDate($("#txtRecDate")[0],"yyyy-MM-dd")});

	$("#aAddInCategory").click(function(){
		$("#liAddInCategory").toggle();
		$("#liAddOutCategory").hide();
		$("#liOutOption").addClass("disable");
		$("#liInOption").removeClass("disable");
		$("#rdoTypeIn").attr("checked","true")
		});


	$("#selInCategory").change(function(){
		$("#liAddOutCategory").hide();
		$("#liOutOption").addClass("disable");
		$("#liInOption").removeClass("disable");
		$("#rdoTypeIn").attr("checked","true");
		return true
		});

	$("#selOutCategory").change(function(){$("#liAddInCategory").hide();
		$("#liInOption").addClass("disable");
		$("#liOutOption").removeClass("disable");
		$("#rdoTypeOut").attr("checked","true");
		return true
	});
	$("#aAddOutCategory").click(function(){$("#liAddOutCategory").toggle();
	$("#liAddInCategory").hide();
	$("#liInOption").addClass("disable");
	$("#liOutOption").removeClass("disable");
	$("#rdoTypeOut").attr("checked","true")});

	$("#rdoTypeIn").click(function(){$("#liOutOption").addClass("disable");
	$("#liInOption").removeClass("disable");
	$("#liAddOutCategory").hide()});

	$("#rdoTypeOut").click(function(){$("#liInOption").addClass("disable");
	$("#liOutOption").removeClass("disable");
	$("#liAddInCategory").hide()});

	$("#btnCancelAddInCategory").click(function(){$("#liAddInCategory").hide();

	resetCategory()});

	$("#btnCancelAddOutCategory").click(function(){$("#liAddOutCategory").hide();

	resetCategory()});

	$("#btnSubmitInCategory").click(function(){
		var a=$(".categoryData").input2Json();
		if(validateCategory("in")){
			$.ajax({
				url:"/mybill/category.do?accountid="+accountid+"&method=addOrUpdate",
				data:$(".categoryData").input2Json(),
				success:function(b){
					showMessage(b.result.message);
					if(b.result.success=="true"){
						handleCategoryData(b.result.data);
						$("#liAddInCategory").hide()
					}
				}
			})
		}
	});

	$("#btnSubmitOutCategory").click(function(){
		if(validateCategory("out")){
			$.ajax({
				url:"/mybill/category.do?accountid="+accountid+"&method=addOrUpdate",
				data:$(".categoryData").input2Json(),
				success:function(a){
					showMessage(a.result.message);
					if(a.result.success=="true"){
						handleCategoryData(a.result.data);
						$("#liAddOutCategory").hide()
					}
				}
			})
		}
	});

	$("#btnAdd,#btnTransfer").click(function(){
		if(validate()){
			$.ajax({
				url:"/mybill/bill.do?accountid="+accountid+"&method=transfer",
				data:$(".transferData").input2Json(),
				success:function(a){
					showMessage(a.result.message);
					if(!$("#hdnId")||!$("#hdnId").val()||$("#hdnId").val()==0){
						reset()
					}
				}
			})
		}
	})
});

function handleCategoryData(b){
	var c;
  var a;
	try{
		resetCategory();
		if(b.type==0){
			c=$("#selOutCategory");
			a=$("#selOutCategories")
		}else{
			c=$("#selInCategory");
			a=$("#selInCategories")
		}
		if(b.parentId==0){
			var j=$("<option/>");
			j.val(b.type+"|"+b.id);
			j.text(b.categoryName);
			j.appendTo(a).attr("selected","true");
			var h=$("<option/>");
			h.text(b.categoryName);
			h.val(b.type+"|"+b.id+"|0");
			h.appendTo(c).attr("selected","true")
		}else{
			var d=$("<option/>");
			var g=b.type+"|"+b.parentId+"|"+b.id;
			var i=$("option:selected",a).text()+" - "+b.categoryName;
			d.val(g);
			d.text(i);
			d.insertAfter($("option[value^='"+b.type+"|"+b.parentId+"']:last",c)).attr("selected","true")
		}
	}catch(f){
		console.log(f);
		return false}
}

function reset(){
	$("#txtTitle").val("");
	$("#txtNote").val("");
	$("#txtAmount").val("");
	$("#txtReceipt").val("");
	//$("#selToAccount").val("");
	showMessage("数据已保存，可以添加新数据了");
}

function resetCategory(){
	$("#txtOutCategoryName").val("");
	$("#txtInCategoryName").val("")
}

function validate(){
	if(!$("#txtRecDate").val()){showMessage("必须输入日期!");
		$("#txtRecDate").focus();
		return false
	}


	if(!$("#selToAccount").val()){showMessage("必须选择转入账户!");
		$("#selToAccount").focus();
		return false
	}

	try{
		var c=$("#selToAccount").val();
		$("#hdnToAccountId").val(c);
	}catch(d){
		showMessage("账户数据读取出错,请刷新页面后再试!");
		return false
	}

	if(!$("#txtAmount").val()){
		showMessage("必须输入金额");
		$("#txtAmount").focus();
		return false
	}

	var b=new RegExp("^\\d{1,8}(\\.\\d{0,2})?$","gi");
	if(!b.test($("#txtAmount").val())){
		showMessage("金额格式输入错误!");
		$("#txtAmount").focus();
		return false
	}
	return true
}

function validateCategory(a){
	if(a=="in"){
		if(!$("#txtInCategoryName").val()||$.trim($("#txtInCategoryName").val())==""){
			$("#txtInCategoryName").focus();
			showMessage("必须输入收入项目名称!");
			return false
		}

		try{
			$("#hdnCCategoryName").val($("#txtInCategoryName").val());
			$("#hdnCType").val("1");

			if($("#rdoScopeInCategory").is(":checked")){
				$("#hdnCParentId").val("0")
			}else{
				if($("#selInCategories option").size()==0){
					$("#rdoScopeInCategory").attr("checked","true").focus();
					showMessage("目前没有一级收入项目可选,请先建立一级项目!");
					b.preventDefault();
					return false
				}else{
					$("#hdnCParentId").val($("#selInCategories option:selected").val().split("|")[1])
				}
			}
		}catch(b){
			return false
		}
	}else{
		if(!$("#txtOutCategoryName").val()||$.trim($("#txtOutCategoryName").val())==""){
			$("#txtOutCategoryName").focus();
			showMessage("必须输入支出项目名称!");
			return false
		}
		try{
			$("#hdnCCategoryName").val($("#txtOutCategoryName").val());
			$("#hdnCType").val("0");
			if($("#rdoScopeOutCategory").is(":checked")){
				$("#hdnCParentId").val("0")
			}else{
				if($("#selOutCategories option").size()==0){
					$("#rdoScopeOutCategory").attr("checked","true").focus();
					showMessage("目前没有一级支出项目可选,请先建立一级项目!");
					b.preventDefault();
					return false
				}else{
					$("#hdnCParentId").val($("#selOutCategories option:selected").val().split("|")[1])
				}
			}
		}catch(b){return false}
	}
	return true
};
