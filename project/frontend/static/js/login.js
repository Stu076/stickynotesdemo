$(document).ready(() => {
    $("#register").hide();

    $("#logout").click(() => {
        $.ajax({
            url: "/auth/logout",
            method: "POST",
            headers: {
                "Authorization": "Bearer " + Cookies.get("auth_token")
            },
            success: (data, status) => {
                Cookies.remove("auth_token");
                Cookies.remove("user_id");
                window.location.replace("/");
            },
            error: (data) => {
                console.log(data);
            }
        });
    });

    $("#switch").click(() => {
        if ($("#switch").text() == "Register") {
            $("#switch").text("Log In");
            $("#register").show();
            $("#login").hide();
        } else {
            $("#switch").text("Register");
            $("#register").hide();
            $("#login").show();
        }
    });

    $("#register").click(() => {
        var registerData = {
            "email": $("#email").val(),
            "password": $("#password").val()
        };

        $.ajax({
            url: "/auth/register",
            method: "POST",
            contentType: "application/json",
            data: JSON.stringify(registerData),
            success: (data, status) => {
                if (status === "success") {
                    Cookies.set("auth_token", data.auth_token, { expires: 1 });
                    Cookies.set("user_id", data.user_id, { expires : 1 });
                    window.location.replace("/index");
                }
            },
            error: (data) => {
                console.log(data);
            }
        });
    });

    $("#login").click(() => {
    	var loginData = {
    		"email": $("#email").val(),
    		"password": $("#password").val()
    	};

    	$.ajax({
    		url: "/auth/login",
    		method: "POST",
    		contentType: "application/json",
    		data: JSON.stringify(loginData),
    		success: (data, status) => {
                if (status === "success") {
                    Cookies.set("auth_token", data.auth_token, { expires: 1 });
                    Cookies.set("user_id", data.user_id, { expires : 1 });
                    window.location.replace("/index");
                }
    		},
    		error: (data) => {
    			console.log(data);
    		}
    	});
    });
});