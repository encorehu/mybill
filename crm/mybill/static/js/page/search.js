_import("calendar");
_import("billshare");
_import("pagerable");
$(document).ready(function(){
    $("#txtFromRecDate,#aFromRecDate").click(function(){
        SelectDate($("#txtFromRecDate")[0],"yyyy-MM-dd")
    });

    $("#txtToRecDate,#aToRecDate").click(function(){
        SelectDate($("#txtToRecDate")[0],"yyyy-MM-dd")
    });

    $("#btnSearch").click(function(){
        var f=$("#selCategoryIds").val();
        var e=f.split("|")?f.split("|")[0]:0;
        var g=f.split("|")?f.split("|")[1]:0;
        var d=f.split("|")?f.split("|")[2]:0;
        $("#hdnType").val(e?e:0);
        $("#hdnCategoryId").val(g?g:0);
        $("#hdnSubCategoryId").val(d?d:0);
        $("#frmBillSearch")[0].submit()
    });

    var c=parseInt($("#hdnTotalCount").val());
    var a=parseInt($("#hdnPageIndex").val());
    var b=parseInt($("#hdnPageSize").val());
    $(document).initPageNav(showPage,c,a,b)
});


function showPage(a){
    if(a||a=="0"){
        $("#hdnPageIndex").val(a);
        $("#btnSearch").click()
    }
}

function del2(b,a){
    if(confirm("确认要删除该记录?")){
        $.ajax({
            url:"/mybill/bill.do?accountid="+accountid+"method=del",
            type:"post",
            dataType:"json",
            data:{id:b,sid:a},
            success:function(c){
                showMessage(c.result.message);
                $("#trBill_"+b).remove();
                $(".trBillList:even").removeClass("tr2").addClass("tr1");
                $(".trBillList:odd").removeClass("tr1").addClass("tr2");
                $("#btnSearch").click()
            },
            error:function(){
                showMessage("删除记录失败,请稍后再试!")
            }
        })
    }
    return false
};
