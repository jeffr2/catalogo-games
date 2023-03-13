$(document).ready(function() {
  $("#submit-button").click(function() {
    var name = $("#name").val();
    var description = $("#description").val();
    var image_url = $("#image-url").val();
    var price = $("#price").val();

    $.ajax({
      url: "/api/games",
      type: "POST",
      data: {
        name: name,
        description: description,
        image_url: image_url,
        price: price
      },
      success: function(response) {
        window.location.href = "/games";
      },
      error: function() {
        alert("Erro ao criar novo jogo.");
      }
    });
  });

  $("#cancel-button").click(function() {
    window.location.href = "/games";
  });
});
