_import("calendar");
_import("billshare");
_import("myext");
$(document).ready(function(){
	if(!$("#hdnId").val()||$("#hdnId").val()==0){
		$(".topbar").removeClass("on");
		$("#liTop1").addClass("on")
	}

	$("#txtRecDate,#aRecDate").click(function(){SelectDate($("#txtRecDate")[0],"yyyy-MM-dd")});



	$("#btnAdd,#btnUpdate").click(function(){
		if(validate()){
			$.ajax({
				url:"/mybill/accountbook.do?method=addOrUpdate",
				data:$(".accountbookdata").input2Json(),
				success:function(a){
					showMessage(a.result.message);
					if(!$("#hdnId").val()||$("#hdnId").val()==0){
						reset()
					}
				}
			})
		}
	})
});



function reset(){
	$("#txtAccountName").val("");
	$("#txtAccountNumber").val("");
	$("#txtAccountDisplayName").val("");
	$("#txtAccountType").val("");
}

function validate(){
	if(!$("#txtAccountBookName").val()){
	    showMessage("必须输入账本名称!");
		$("#txtAccountName").focus();
		return false
	}

	if(!$("#txtAccountBookCode").val()){
	    showMessage("必须输入账本号码!");
		$("#txtAccountBookCode").focus();
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
