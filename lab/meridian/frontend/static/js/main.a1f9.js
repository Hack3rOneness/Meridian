(function () {
  var API = "/api/v2";
  var f = document.getElementById("login");
  if (!f) return;
  f.addEventListener("submit", function (e) {
    e.preventDefault();
    fetch(API + "/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user: f.user.value, pass: f.pass.value })
    }).then(function (r) { return r.json(); })
      .then(function (d) { if (!d.token) location.href = "/oops"; });
  });
})();
