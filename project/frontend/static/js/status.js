$(document).ready(() => {
	var checkUserStatus = () => {
		$.ajax({
			url: "/auth/status",
			method: "GET",
			headers: {
				"Authorization": "Bearer " + Cookies.get("auth_token")
			},
			success: (data, status) => {
				if (status !== "success") {
                    window.location.replace("/");
                    Cookies.remove("auth_token");
                    Cookies.remove("user_id");
				}
			},
			error: (data, status) => {
			    window.location.replace("/");
                Cookies.remove("auth_token");
                Cookies.remove("user_id");
				console.log(data);
				console.log(status);
			}
		});
	};

	checkUserStatus();
});