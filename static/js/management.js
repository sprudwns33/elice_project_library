$(function () {
	$("#star").hide();
	$("#regi_email_msg").hide();
	$("#regi_name_msg").hide();
	$("#regi_pwd_msg").hide();
	$("#login_email_msg").hide();
	$("#login_pwd_msg").hide();
	$("#current_path_register").hide();
	$("#current_path_login").hide();
	$("#alert-success").hide();
	$("#alert-danger").hide();
	$(".pwd_ck").keyup(function () {
		const pwd1 = $("#pwd1").val();
		const pwd2 = $("#pwd2").val();
		if (pwd1 == "" || pwd2 == "") {
			$("#alert-success").hide();
			$("#alert-danger").hide();
		}
		else if (pwd1 == pwd2) {
			$("#alert-success").show();
			$("#alert-danger").hide();
		} else {
			$("#alert-success").hide();
			$("#alert-danger").show();
		}
	});
	$(".name_ck").keyup(function () {
		const name = $("#regi_name").val();
		const regex = /^[ㄱ-ㅎ|가-힣|a-z|A-Z|]+$/;
		if (name == "") {
			$("#regi_name_msg").hide();
			$("#regi_name_msg").text("");
		}
		else if (regex.test(name) == false) {
			$("#regi_name_msg").show();
			$("#regi_name_msg").text("한글/영문만 입력이 가능합니다.");
		} else {
			$("#regi_name_msg").hide();
			$("#regi_name_msg").text("");
		}
	});

	$(".pwdm_ck").keyup(function () {
		const pw = $("#pwd1").val();
		const num = pw.search(/[0-9]/g);
		const eng = pw.search(/[a-z]/ig);
		const spe = pw.search(/[`~!@#$%^&*()_+|]/gi);

		if (pw == "") {
			$("#regi_pwd_msg").hide();
			$("#regi_pwd_msg").text("");
		}
		else if (/(\w)\1\1\1/.test(pw)) {
			$("#regi_pwd_msg").show();
			$("#regi_pwd_msg").text("같은 문자를 4번 이상 사용하실 수 없습니다.");
		}
		else if (pw.search(/\s/) != -1) {
			$("#regi_pwd_msg").show();
			$("#regi_pwd_msg").text("비밀번호는 공백 없이 입력해주세요.");
		}
		else if ((num >= 0 && eng >= 0 && spe >= 0) && (pw.length >= 8)) {
			$("#regi_pwd_msg").hide();
			$("#regi_pwd_msg").text("");
		}
		else if(((num >= 0 && eng >= 0) || (eng >= 0 && spe >= 0) || (spe >= 0 && num >= 0)) && (pw.length >= 10)) {
			$("#regi_pwd_msg").hide();
			$("#regi_pwd_msg").text("");
		}
		else {
			$("#regi_pwd_msg").show();
			$("#regi_pwd_msg").text("영문, 숫자, 특수문자 중 3가지를 포함한 8자리 이상이거나, 2가지를 포함한 10자리 이상이어야 합니다.");
		}
	});
});

function ol_id_check() {
	$.ajax({
		url: "/idCheck",
		type: "post",
		dataType: "json",
		data: { "regi_email": $('#regi_email').val() },
		success: function (data) {
			if ($("#regi_email").val() == "") {
				$("#regi_email_msg").show();
				$("#regi_email_msg").text("아이디를 입력해주세요.");
				$("#regi_email_msg").attr("style", "width:100%; margin-top:10px;color:rgb(255 59 59);background-color:#ffd5d9; border-color:#ffd5d9");
			}
			else if (data == 1) {
				$("#regi_email_msg").show();
				$("#regi_email_msg").text("아이디가 중복되었습니다.");
				$("#regi_email_msg").attr("style", "width:100%; margin-top:10px;color:rgb(255 59 59);background-color:#ffd5d9; border-color:#ffd5d9");
			} else if (data == 2) {
				$("#regi_email_msg").show();
				$("#regi_email_msg").text("이메일 형식에 맞지 않습니다.");
				$("#regi_email_msg").attr("style", "width:100%; margin-top:10px;color:rgb(255 59 59);background-color:#ffd5d9; border-color:#ffd5d9");
			}
			else if (data == 0) {
				$("#regi_email_msg").show();
				$("#regi_email_msg").text("사용 가능한 아이디 입니다.");
				$("#regi_email_msg").attr("style", "width:100%; margin-top:10px;background-color: #cff4fc;border-color: #b6effb;");
			}
		}
	});
}

function r_id_check() {
	if ($("#regi_email_msg").text() == "사용 가능한 아이디 입니다.") {
		$("#regi_email_msg").hide();
		$("#regi_email_msg").text('');
	}
}

function regi_reset() {
	$("#regi_email_msg").hide();
	$("#regi_name_msg").hide();
	$("#regi_pwd_msg").hide();
	$("#alert-success").hide();
	$("#alert-danger").hide();
	$('#regi_email').val("");
	$("#regi_name").val("");
	$("#pwd1").val("");
	$("#pwd2").val("");
}

function login_reset() {
	$('#login_email').val("");
	$("#login_password").val("");
	$("#login_email_msg").hide();
	$("#login_pwd_msg").hide();
}

function login_check() {
	let result = "";
	$.ajax({
		url: "/loginCheck",
		type: "post",
		dataType: "json",
		async: false,
		data: { "login_email": $('#login_email').val(), "login_password": $('#login_password').val() },
		success: function (data) {
			result = data;
		}
	})
	return result
}

$(document).ready(
	function() {
		$("#register").on(
				"click",
				function() {
					if ($("#regi_email").val() == "") {
						alert("아이디를 입력해주세요.");
						$("#regi_email").focus();
						return false;
					}
					if ($("#regi_name").val() == "") {
						alert("이름을 입력해주세요.");
						$("#regi_name").focus();
						return false;
					}
					if ($("#pwd1").val() == "") {
						alert("비밀번호를 입력해주세요.");
						$("#pwd1").focus();
						return false;
					}
					if ($("#regi_email_msg").text() != "사용 가능한 아이디 입니다.") {
						alert("아이디 중복확인을 해주세요.");
						$("#regi_email").focus();
						return false;
					}
					if ($("#regi_name_msg").text() != "") {
						alert("이름을 확인해주세요.");
						$("#regi_name").focus();
						return false;
					}
					if ($("#regi_pwd_msg").text() != "") {
						alert("비밀번호를 확인해주세요.");
						$("#pwd1").focus();
						return false;
					}
					var pwd1 = $("#pwd1").val();
					var pwd2 = $("#pwd2").val();
					if (pwd1 != "" || pwd2 != "") {
						if (pwd1 !== pwd2) {
							alert("비밀번호를 확인해주세요.");
							$("#pwd1").val();
							return false;
						}
					}
				});
		$("#login").on(
			"click",
			function() {
				const result = login_check();
				if ($("#login_email").val() == "") {
					$("#login_email_msg").show();
					$("#login_email_msg").text("아이디를 입력해주세요.");
					$("#login_pwd_msg").hide();
					$("#login_email").focus();
					return false;
				}
				if (result == 0) {
					$("#login_email_msg").show();
					$("#login_email_msg").text("존재하지 않는 아이디입니다.");
					$("#login_pwd_msg").hide();
					$("#login_email").focus();
					return false;
				}
				if ($("#login_password").val() == "") {
					$("#login_pwd_msg").show();
					$("#login_pwd_msg").text("비밀번호를 입력해주세요.");
					$("#login_email_msg").hide();
					$("#login_password").focus();
					return false;
				}
				if (result == 2) {
					$("#login_pwd_msg").show();
					$("#login_pwd_msg").text("비밀번호는 최소 8자리 이상입니다.");
					$("#login_email_msg").hide();
					$("#login_password").focus();
					return false;
				}
				if (result == 3) {
					$("#login_pwd_msg").show();
					$("#login_pwd_msg").text("비밀번호가 일치하지 않습니다.");
					$("#login_email_msg").hide();
					$("#login_password").focus();
					return false;
				}
				alert("로그인에 성공하였습니다.");
			});
		$("#review_add").on(
			"click",
			function() {
				const review_val = $("#review_content").val();
				if (review_val == "") {
					alert("댓글을 작성해주세요.")
					return false;
				}
				const star = $("#star").val();
				if (star == 0) {
					alert("별점을 선택해주세요.")
					return false;
				}
			});
	})


	$(".star_rating a").click(function() {
		$(this).parent().children("a").removeClass("on");
		$(this).addClass("on").prevAll("a").addClass("on");
		const star_val = $(this).prevAll("a");
		$("#star").val(star_val.length + 1);
		return false;
	});