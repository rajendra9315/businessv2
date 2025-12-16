// ===== SIMPLE AUTH STATE =====
function loginUser() {
  // fake login (later backend will handle this)
  localStorage.setItem("isLoggedIn", "true");
  window.location.href = "dashboard.html";
}

function logoutUser() {
  localStorage.removeItem("isLoggedIn");
  window.location.href = "../public/index.html";
}

// ===== PAGE PROTECTION =====
function protectPage() {
  const isLoggedIn = localStorage.getItem("isLoggedIn");

  if (!isLoggedIn) {
    window.location.href = "../public/index.html";
  }
}
