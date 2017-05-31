var cal;
var isFocus = false;

function SelectDate(A, C) {
	var E = new Date();
	var D = E.getFullYear() - 50;
	var B = E.getFullYear() + 50;
	cal = (cal == null) ? new Calendar(D, B, 0) : cal;
	cal.dateFormatStyle = C;
	cal.show(A);
	return true
}
String.prototype.toDate = function(style) {
	var y = this.substring(style.indexOf("y"), style.lastIndexOf("y") + 1);
	var m = this.substring(style.indexOf("M"), style.lastIndexOf("M") + 1);
	var d = this.substring(style.indexOf("d"), style.lastIndexOf("d") + 1);
	if (isNaN(y)) {
		y = new Date().getFullYear()
	}
	if (isNaN(m)) {
		m = new Date().getMonth()
	}
	if (isNaN(d)) {
		d = new Date().getDate()
	}
	var dt;
	eval("dt = new Date('" + y + "', '" + (m - 1) + "','" + d + "')");
	return dt
};
Date.prototype.format = function(C) {
	var A = {
		"M+": this.getMonth() + 1,
		"d+": this.getDate(),
		"h+": this.getHours(),
		"m+": this.getMinutes(),
		"s+": this.getSeconds(),
		"w+": "天一二三四五六".charAt(this.getDay()),
		"q+": Math.floor((this.getMonth() + 3) / 3),
		"S": this.getMilliseconds()
	};
	if (/(y+)/.test(C)) {
		C = C.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length))
	}
	for (var B in A) {
		if (new RegExp("(" + B + ")").test(C)) {
			C = C.replace(RegExp.$1, RegExp.$1.length == 1 ? A[B] : ("00" + A[B]).substr(("" + A[B]).length))
		}
	}
	return C
};

function Calendar(D, A, B, C) {
	this.beginYear = 1990;
	this.endYear = 2010;
	this.lang = 0;
	this.dateFormatStyle = "yyyy-MM-dd";
	if (D != null && A != null) {
		this.beginYear = D;
		this.endYear = A
	}
	if (B != null) {
		this.lang = B
	}
	if (C != null) {
		this.dateFormatStyle = C
	}
	this.dateControl = null;
	this.panel = this.getElementById("calendarPanel");
	this.container = this.getElementById("ContainerPanel");
	this.form = null;
	this.date = new Date();
	this.year = this.date.getFullYear();
	this.month = this.date.getMonth();
	this.colors = {
		"cur_word": "#FFFFFF",
		"cur_bg": "#00FF00",
		"sel_bg": "#FFCCCC",
		"sun_word": "#FF0000",
		"sat_word": "#0000FF",
		"td_word_light": "#333333",
		"td_word_dark": "#CCCCCC",
		"td_bg_out": "#EFEFEF",
		"td_bg_over": "#FFCC00",
		"tr_word": "#FFFFFF",
		"tr_bg": "#666666",
		"input_border": "#CCCCCC",
		"input_bg": "#EFEFEF"
	};
	this.draw();
	this.bindYear();
	this.bindMonth();
	this.changeSelect();
	this.bindData()
}
Calendar.language = {
	"year": [
		[""],
		[""]
	],
	"months": [
		["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"],
		["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
	],
	"weeks": [
		["日", "一", "二", "三", "四", "五", "六"],
		["SUN", "MON", "TUR", "WED", "THU", "FRI", "SAT"]
	],
	"clear": [
		["清空"],
		["CLS"]
	],
	"confirm": [
		["确定"],
		["CONFIRM"]
	],
	"today": [
		["今天"],
		["TODAY"]
	],
	"close": [
		["关闭"],
		["CLOSE"]
	]
};
Calendar.prototype.draw = function() {
	calendar = this;
	var C = [];
	C[C.length] = "  <div name=\"calendarForm\" style=\"margin: 0px;\">";
	C[C.length] = "    <table width=\"100%\" border=\"0\" cellpadding=\"0\" cellspacing=\"1\">";
	C[C.length] = "      <tr>";
	C[C.length] = "        <th align=\"left\" width=\"1%\"><input style=\"border: 1px solid " + calendar.colors["input_border"] + ";background-color:" + calendar.colors["input_bg"] + ";width:16px;height:20px;\" name=\"prevMonth\" type=\"button\" id=\"prevMonth\" value=\"&lt;\" /></th>";
	C[C.length] = "        <th align=\"center\" width=\"98%\" nowrap=\"nowrap\"><select name=\"calendarYear\" id=\"calendarYear\" style=\"font-size:12px;\"></select><select name=\"calendarMonth\" id=\"calendarMonth\" style=\"font-size:12px;\"></select></th>";
	C[C.length] = "        <th align=\"right\" width=\"1%\"><input style=\"border: 1px solid " + calendar.colors["input_border"] + ";background-color:" + calendar.colors["input_bg"] + ";width:16px;height:20px;\" name=\"nextMonth\" type=\"button\" id=\"nextMonth\" value=\"&gt;\" /></th>";
	C[C.length] = "      </tr>";
	C[C.length] = "    </table>";
	C[C.length] = "    <table id=\"calendarTable\" width=\"100%\" style=\"border:0px solid #CCCCCC;background-color:#FFFFFF\" border=\"0\" cellpadding=\"3\" cellspacing=\"1\">";
	C[C.length] = "      <tr>";
	for (var A = 0; A < 7; A++) {
		C[C.length] = "      <th style=\"font-weight:normal;background-color:" + calendar.colors["tr_bg"] + ";color:" + calendar.colors["tr_word"] + ";\">" + Calendar.language["weeks"][this.lang][A] + "</th>"
	}
	C[C.length] = "      </tr>";
	for (var A = 0; A < 6; A++) {
		C[C.length] = "    <tr align=\"center\">";
		for (var D = 0; D < 7; D++) {
			if (D == 0) {
				C[C.length] = "  <td style=\"cursor:default;color:" + calendar.colors["sun_word"] + ";\"></td>"
			} else {
				if (D == 6) {
					C[C.length] = "  <td style=\"cursor:default;color:" + calendar.colors["sat_word"] + ";\"></td>"
				} else {
					C[C.length] = "  <td style=\"cursor:default;\"></td>"
				}
			}
		}
		C[C.length] = "    </tr>"
	}
	C[C.length] = "      <tr style=\"background-color:" + calendar.colors["input_bg"] + ";\">";
	C[C.length] = "        <th colspan=\"2\"><input name=\"calendarClose\" type=\"button\" id=\"calendarClose\" value=\"" + Calendar.language["close"][this.lang] + "\" style=\"border: 1px solid " + calendar.colors["input_border"] + ";background-color:" + calendar.colors["input_bg"] + ";width:100%;height:20px;font-size:12px;\"/></th>";
	C[C.length] = "        <th colspan=\"3\"><input name=\"calendarToday\" type=\"button\" id=\"calendarToday\" value=\"" + Calendar.language["today"][this.lang] + "\" style=\"border: 1px solid " + calendar.colors["input_border"] + ";background-color:" + calendar.colors["input_bg"] + ";width:100%;height:20px;font-size:12px;\"/></th>";
	C[C.length] = "        <th colspan=\"2\"><input name=\"calendarConfirm\" type=\"button\" id=\"calendarConfirm\" value=\"" + Calendar.language["confirm"][this.lang] + "\" style=\"border: 1px solid " + calendar.colors["input_border"] + ";background-color:" + calendar.colors["input_bg"] + ";width:100%;height:20px;font-size:12px;\"/></th>";
	C[C.length] = "      </tr>";
	C[C.length] = "    </table>";
	C[C.length] = "  </div>";
	this.panel.innerHTML = C.join("");
	var B = this.getElementById("prevMonth");
	B.onclick = function() {
		calendar.goPrevMonth(calendar)
	};
	B.onblur = function() {
		calendar.onblur()
	};
	this.prevMonth = B;
	B = this.getElementById("nextMonth");
	B.onclick = function() {
		calendar.goNextMonth(calendar)
	};
	B.onblur = function() {
		calendar.onblur()
	};
	this.nextMonth = B;
	B = this.getElementById("calendarClose");
	B.onclick = function() {
		calendar.hide()
	};
	this.calendarClose = B;
	B = this.getElementById("calendarYear");
	B.onchange = function() {
		calendar.update(calendar)
	};
	B.onblur = function() {
		calendar.onblur()
	};
	this.calendarYear = B;
	B = this.getElementById("calendarMonth");
	with(B) {
		onchange = function() {
			calendar.update(calendar)
		};
		onblur = function() {
			calendar.onblur()
		}
	}
	this.calendarMonth = B;
	B = this.getElementById("calendarConfirm");
	B.onclick = function() {
		calendar.dateControl.value = calendar.date.format(calendar.dateFormatStyle);
		calendar.hide()
	};
	this.calendarConfirm = B;
	B = this.getElementById("calendarToday");
	B.onclick = function() {
		var A = new Date();
		calendar.date = A;
		calendar.year = A.getFullYear();
		calendar.month = A.getMonth();
		calendar.changeSelect();
		calendar.bindData();
		calendar.dateControl.value = A.format(calendar.dateFormatStyle);
		calendar.hide()
	};
	this.calendarToday = B
};
Calendar.prototype.bindYear = function() {
	var B = this.calendarYear;
	B.length = 0;
	for (var A = this.beginYear; A <= this.endYear; A++) {
		B.options[B.length] = new Option(A + Calendar.language["year"][this.lang], A)
	}
};
Calendar.prototype.bindMonth = function() {
	var B = this.calendarMonth;
	B.length = 0;
	for (var A = 0; A < 12; A++) {
		B.options[B.length] = new Option(Calendar.language["months"][this.lang][A], A)
	}
};
Calendar.prototype.goPrevMonth = function(A) {
	if (this.year == this.beginYear && this.month == 0) {
		return
	}
	this.month--;
	if (this.month == -1) {
		this.year--;
		this.month = 11
	}
	this.date = new Date(this.year, this.month, 1);
	this.changeSelect();
	this.bindData()
};
Calendar.prototype.goNextMonth = function(A) {
	if (this.year == this.endYear && this.month == 11) {
		return
	}
	this.month++;
	if (this.month == 12) {
		this.year++;
		this.month = 0
	}
	this.date = new Date(this.year, this.month, 1);
	this.changeSelect();
	this.bindData()
};
Calendar.prototype.changeSelect = function() {
	var B = this.calendarYear;
	var C = this.calendarMonth;
	for (var A = 0; A < B.length; A++) {
		if (B.options[A].value == this.date.getFullYear()) {
			B[A].selected = true;
			break
		}
	}
	for (var A = 0; A < C.length; A++) {
		if (C.options[A].value == this.date.getMonth()) {
			C[A].selected = true;
			break
		}
	}
};
Calendar.prototype.update = function(A) {
	this.year = A.calendarYear.options[A.calendarYear.selectedIndex].value;
	this.month = A.calendarMonth.options[A.calendarMonth.selectedIndex].value;
	this.date = new Date(this.year, this.month, 1);
	this.changeSelect();
	this.bindData()
};
Calendar.prototype.bindData = function() {
	var A = this;
	var C = this.getMonthViewArray(this.date.getFullYear(), this.date.getMonth());
	var D = this.getElementById("calendarTable").getElementsByTagName("td");
	for (var B = 0; B < D.length; B++) {
		D[B].style.backgroundColor = A.colors["td_bg_out"];
		D[B].onclick = function() {
			return
		};
		D[B].onmouseover = function() {
			return
		};
		D[B].onmouseout = function() {
			return
		};
		if (B > C.length - 1) {
			break
		}
		D[B].innerHTML = C[B];
		if (C[B] != "&nbsp;") {
			D[B].onclick = function() {
				if (A.dateControl != null) {
					A.dateControl.value = new Date(A.date.getFullYear(), A.date.getMonth(), this.innerHTML).format(A.dateFormatStyle)
				}
				A.hide()
			};
			D[B].onmouseover = function() {
				this.style.backgroundColor = A.colors["td_bg_over"]
			};
			D[B].onmouseout = function() {
				this.style.backgroundColor = A.colors["td_bg_out"]
			};
			if (new Date().format(A.dateFormatStyle) == new Date(A.date.getFullYear(), A.date.getMonth(), C[B]).format(A.dateFormatStyle)) {
				D[B].style.backgroundColor = A.colors["cur_bg"];
				D[B].onmouseover = function() {
					this.style.backgroundColor = A.colors["td_bg_over"]
				};
				D[B].onmouseout = function() {
					this.style.backgroundColor = A.colors["cur_bg"]
				}
			}
			if (A.dateControl != null && A.dateControl.value == new Date(A.date.getFullYear(), A.date.getMonth(), C[B]).format(A.dateFormatStyle)) {
				D[B].style.backgroundColor = A.colors["sel_bg"];
				D[B].onmouseover = function() {
					this.style.backgroundColor = A.colors["td_bg_over"]
				};
				D[B].onmouseout = function() {
					this.style.backgroundColor = A.colors["sel_bg"]
				}
			}
		}
	}
};
Calendar.prototype.getMonthViewArray = function(F, C) {
	var A = [];
	var E = new Date(F, C, 1).getDay();
	var D = new Date(F, C + 1, 0).getDate();
	for (var B = 0; B < 42; B++) {
		A[B] = "&nbsp;"
	}
	for (var B = 0; B < D; B++) {
		A[B + E] = B + 1
	}
	return A
};
Calendar.prototype.getElementById = function(id) {
	if (typeof(id) != "string" || id == "") {
		return null
	}
	if (document.getElementById) {
		return document.getElementById(id)
	}
	if (document.all) {
		return document.all(id)
	}
	try {
		return eval(id)
	} catch (A) {
		return null
	}
};
Calendar.prototype.getElementsByTagName = function(A, B) {
	if (document.getElementsByTagName) {
		return document.getElementsByTagName(B)
	}
	if (document.all) {
		return document.all.tags(B)
	}
};
Calendar.prototype.getAbsPoint = function(C) {
	var B = C.offsetLeft;
	var A = C.offsetTop;
	while (C = C.offsetParent) {
		B += C.offsetLeft;
		A += C.offsetTop
	}
	return {
		"x": B,
		"y": A
	}
};
Calendar.prototype.show = function(C, B) {
	if (C == null) {
		throw new Error("arguments[0] is necessary")
	}
	this.dateControl = C;
	this.date = (C.value.length > 0) ? new Date(C.value.toDate(this.dateFormatStyle)) : new Date();
	this.year = this.date.getFullYear();
	this.month = this.date.getMonth();
	this.changeSelect();
	this.bindData();
	if (B == null) {
		B = C
	}
	var A = this.getAbsPoint(B);
	this.panel.style.left = A.x - 25 + "px";
	this.panel.style.top = (A.y + C.offsetHeight) + "px";
	this.panel.style.display = "";
	this.container.style.display = "";
	C.onblur = function() {
		calendar.onblur()
	};
	this.container.onmouseover = function() {
		isFocus = true
	};
	this.container.onmouseout = function() {
		isFocus = false
	}
};
Calendar.prototype.hide = function() {
	this.panel.style.display = "none";
	this.container.style.display = "none";
	isFocus = false
};
Calendar.prototype.onblur = function() {
	if (!isFocus) {
		this.hide()
	}
};
document.write("<div id=\"ContainerPanel\" style=\"display:none\"><div id=\"calendarPanel\" style=\"position: absolute;display: none;z-index: 9999;");
document.write("background-color: #FFFFFF;border: 1px solid #CCCCCC;width:175px;font-size:12px;\"></div>");
if (document.all) {
	document.write("<iframe style=\"position:absolute;z-index:2000;width:expression(this.previousSibling.offsetWidth);");
	document.write("height:expression(this.previousSibling.offsetHeight);");
	document.write("left:expression(this.previousSibling.offsetLeft);top:expression(this.previousSibling.offsetTop);");
	document.write("display:expression(this.previousSibling.style.display);\" scrolling=\"no\" frameborder=\"no\"></iframe>")
}
document.write("</div>");