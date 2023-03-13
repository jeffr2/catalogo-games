$(document).ready(function() {
    $("#submit-button").click(function() {
      var title = $("#title").val();
      var year = $("#year").val();
      var platform = $("#platform").val();
      var genre = $("#genre").val();
  
      $.ajax({
        url: "/games",
        type: "POST",
        data: {
          title: title,
          year: year,
          platform: platform,
          genre: genre
        },
        success: function(response) {
          window.location.href = "/games";
        },
        error: function() {
          alert("Erro ao adicionar novo jogo.");
        }
      });
    });
  });  