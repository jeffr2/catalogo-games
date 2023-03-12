$(document).ready(function() {
    $("#login-button").click(function() {
      var username = $("#username").val();
      var password = $("#password").val();
  
      $.ajax({
        url: "/login",
        type: "POST",
        data: {
          username: username,
          password: password
        },
        success: function(response) {
          window.location.href = "/games";
        },
        error: function() {
          alert("Usuário ou senha incorretos.");
        }
      });
    });
  
    $("#reset-button").click(function() {
      alert("Função de resetar senha não implementada.");
    });
  });