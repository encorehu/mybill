_import("billshare");$(document).ready(function(){$(".aFolder").click(function(){if($(this).attr("state")=="min"){$(this).attr("state","max").removeClass("icoMin").addClass("icoMax").attr("title","展开");$("tr.trSubCategory_"+$(this).attr("cId")).hide()}else{$(this).attr("state","min").removeClass("icoMax").addClass("icoMin").attr("title","折叠");$("tr.trSubCategory_"+$(this).attr("cId")).show()}return false});$(".aDelCategory").click(function(){var c=$(this).attr("cId");var a=$(this).attr("sid");var b=confirm("删除该记录会同时删除对应的子项目,确定要删除该记录么?");if(b){$.ajax({url:"/mybill/category.do?method=del",data:{id:c,sid:a},success:function(d){showMessage(d.result.message);if(d.result.success=="true"){$("tr.trCategory_"+c).remove();if($("tr.trlev1").size()==0){$("#divNoList").show();$("#divCList").hide()}}}})}return false});$(".aEditSubCategory").click(function(){var a=$(this).attr("subCId");$("#spnEditSubCategoryName_"+a).show();$("#spnViewSubCategoryName_"+a).hide();return false});$(".iptCancelSubCategory").click(function(){var a=$(this).attr("subCId");$("#spnEditSubCategoryName_"+a).hide();$("#spnViewSubCategoryName_"+a).show();$("#iptSubCategoryName_"+a).val($("#spnViewSubCategoryName_"+a).text());return false});$(".iptSaveSubCategory").click(function(){var a=$(this).attr("subCId");if(!$("#iptSubCategoryName_"+a).val()){showMessage("必须输入收支项目名称!");return false}else{$.ajax({url:"/mybill/category.do?method=addOrUpdate",data:{id:a,categoryName:$("#iptSubCategoryName_"+a).val(),parentId:$(this).attr("cId"),type:$(this).attr("cType"),sid:$(this).attr("sid"),accountId:$(this).attr("accountId")},success:function(b){showMessage(b.result.message);if(b.result.success=="true"){$("#spnEditSubCategoryName_"+a).hide();$("#spnViewSubCategoryName_"+a).show();$("#spnViewSubCategoryName_"+a).text($("#iptSubCategoryName_"+a).val())}}})}return false});$(".aDelSubCategory").click(function(){var c=$(this).attr("subCId");var a=$(this).attr("sid");var b=confirm("确定要删除该记录么?");if(b){$.ajax({url:"/mybill/category.do?method=del",data:{id:c,sid:a},success:function(d){showMessage(d.result.message);if(d.result.success=="true"){$("#trSubCategory_"+c).remove()}}})}return false})});