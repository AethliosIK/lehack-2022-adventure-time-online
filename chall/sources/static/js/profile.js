// Notification handling
function notify(type, message, delay = 2000) {
  $.notify(
    {
      message: $("<span>").text(message).html(),
    },
    {
      delay: delay,
      type: type,
      placement: {
        from: "top",
        align: "center",
      },
    }
  );
}

function callAPI(item, actionFunction, args) {
  var form = $("#" + item)[0];
  var file = $("#" + item + " #inputFile")[0];
  var data = new FormData(form);
  if (file.files.length != 0) {
    data.append("file", file.files[0]);
  }
  $.ajax({
    cache: false,
    type: form.method,
    url: form.action,
    data: data,
    processData: false,
    contentType: false,
    error: function (xhr, textStatus, error) {
      notify(
        "danger",
        "An error occured [url=" + url + "] : " + xhr.status + " " + error,
        10000
      );
    },
    success: function (data) {
      if (actionFunction != null) {
        actionFunction(data, args);
      }
      notify(data.status, data.message);
    },
  });
}

function updateProfile(data, args) {
  var form = args[0];
  $(form + " input").each(function (i) {
    if (data.elems[this.name] !== undefined) {
      this.value = data.elems[this.name];
    }
  });
}

function updateTextArea(data, args) {
  var area = args[0];
  console.log(data.elems);
  $(area)[0].value = data.elems;
}

$(document).on("click", "#save-btn", function () {
  $("#profile-form").attr("action", "/api/save");
  $("#profile-form")
    .off("submit")
    .submit(function (event) {
      event.preventDefault();
      return callAPI("profile-form", null, []);
    });
});

$(document).on("click", "#import-btn", function () {
  $("#profile-form").attr("action", "/api/import");
  $("#profile-form")
    .off("submit")
    .submit(function (event) {
      event.preventDefault();
      return callAPI("profile-form", updateProfile, ["#profile-form"]);
    });
});

$(document).on("click", "#export-btn", function () {
  $("#profile-form").attr("action", "/api/export");
  $("#profile-form")
    .off("submit")
    .submit(function (event) {
      event.preventDefault();
      return callAPI("profile-form", updateTextArea, ["#export-textarea"]);
    });
});
