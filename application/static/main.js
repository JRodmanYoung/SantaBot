saveNewPerson = function(){
	let firstName = document.getElementById("firstName").value;
	let lastName = document.getElementById("lastName").value;
	let email = document.getElementById("email").value;
	
	$(document).ready(function(){	
		$.ajax({
			type: "POST",
			contentType: "application/json; charset=utf-8",
			url: "/api/v1/person",
			data: JSON.stringify({"first_name": firstName, "last_name": lastName, "email": email}),
			success: function (data) {
				console.log(data.person_ID);
				document.getElementById("firstName").value = '';
				document.getElementById("lastName").value = '';
				document.getElementById("email").value = '';
				$('#userTable tr:last').before("<tr><td>" + data.first_name + "</td>" + 
											    "<td>" + data.last_name + "</td>" +
												"<td>" + data.email + "</td>" +
												"<td><button class='deleteButton' id='" + data.person_ID + "' type='button'>delete</button></tr>")
			},
			dataType: "json"
		});
	})
}

$(document).ready(function(){
	$("#userTable").on("click", ".deleteButton", function(){
	// $(".deleteButton").click(function(){
		let thisElement = $(this);
		$.ajax({
			type: "DELETE",
			contentType: "application/json; charset=utf-8",
			url: "/api/v1/person/" + this.id,
			success: function(data) {
				console.log(data)
				thisElement.parent().parent().remove();
			}
		});
	})
});
