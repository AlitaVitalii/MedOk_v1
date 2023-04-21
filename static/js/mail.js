$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-mail .modal-content").html("");
        $("#modal-mail").modal("show");
      },
      success: function (data) {
        $("#modal-mail .modal-content").html(data.html_form);
      }
    });
  };

  var saveForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
           alert("Ваше сообщение отправлено!");
          $("#modal-mail").modal("hide");
      }
    });
    return false;
  };


  /* Binding */

  $(".js-email").click(loadForm);
  $("#modal-mail").on("submit", ".js-email-form", saveForm);

});
