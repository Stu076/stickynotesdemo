var deleteNote = (id) => {
		var deleteNoteContent = {
			"id": id
		};

		$.ajax({
			url: "/stickynote/delete",
			method: "POST",
			headers: {
				"Authorization": "Bearer " + Cookies.get("auth_token")
			},
			contentType: "application/json",
			data: JSON.stringify(deleteNoteContent),
			success: (data, status) => {
				if (status === "success") {
					getNotes();
				}
			},
			error: (data) => {
				console.log(data);
			}
		});
	};

	var updateNote = (id) => {
		var updateNoteContent = {
			"id": id,
			"note_content": $("#textarea-" + id).val()
		};

		$.ajax({
			url: "/stickynote/update",
			method: "POST",
			headers: {
				"Authorization": "Bearer " + Cookies.get("auth_token")
			},
			contentType: "application/json",
			data: JSON.stringify(updateNoteContent),
			success: (data, status) => {
				if (status === "success") {
					getNotes();
				}
			},
			error: (data) => {
				console.log(data);
			}
		});
	};

	var getNotes = () => {
		$.ajax({
			url: "/stickynote/get?user_id=" + Cookies.get("user_id"),
			method: "GET",
			headers: {
				"Authorization": "Bearer " + Cookies.get("auth_token")
			},
			success: (data, status) => {
				if (status === "success") {
					$("#stickynotes-wrapper").html("");
					var html = "";
					$.each(JSON.parse(data.sticky_notes), (key, value) => {
						html += "<div id='sticky-note-" + value.id + "' class='float-left stickynote'> " +
								"<div><textarea id='textarea-" + value.id + "' rows='5' cols='50'> " +
								value.note_content + "</textarea></div>" +
								"<div><button onclick='updateNote(" + value.id + ")' class='btn btn-dark'>" +
								"Update note</button> <button onclick='deleteNote(" + value.id + ")' class='btn btn-danger'>" +
								"Delete note</button></div></div>";
					});
					$("#stickynotes-wrapper").html(html);
				}
			},
			error: (data) => {
				console.log(data);
			}
		});
	};

$(document).ready(() => {
	$("#add-note-popup-btn").click(() => {
		$("#add-note-popup").show();
	});

	$("#add-note").click(() => {
		var noteContent = {
			"note_content": $("#add-note-content").val(),
			"user_id": Cookies.get("user_id")
		};

		$.ajax({
			url: "/stickynote/add",
			method: "POST",
			headers: {
				"Authorization": "Bearer " + Cookies.get("auth_token")
			},
			contentType: "application/json",
			data: JSON.stringify(noteContent),
			success: (data, status) => {
				if (status === "success") {
					getNotes();
					$("#add-note-popup").hide();
				}
			},
			error: (data) => {
				console.log(data);
			}
		});
	});

	$("#cancel-add-note").click(() => {
		$("#add-note-content").val("");
		$("#add-note-popup").hide();
	});

	getNotes();
	$("#add-note-popup").hide();
});