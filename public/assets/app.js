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

// ===== FAKE DATA ANALYSIS =====
function analyzeData() {
  // Fake results (later backend will calculate real ones)
  const fakeResults = {
    revenue: "₹ 12,40,000",
    profit: "₹ 3,10,000",
    margin: "25%",
    growth: "12%",
    insight: "Profit margin dropped last month due to increased delivery costs. Focus on Product A to improve margins.",
    risk: "Logistics cost is increasing faster than revenue.",
    opportunity: "Product A has the highest margin and strong growth potential."
  };

  // Save results
  localStorage.setItem("analysisResults", JSON.stringify(fakeResults));

  // Redirect to dashboard
  window.location.href = "dashboard.html";
}
// ===== USER REGISTRATION =====
function registerUser() {
  const user = {
    status: "PENDING" // PENDING | APPROVED
  };

  localStorage.setItem("user", JSON.stringify(user));
  alert("Registration successful. Please complete payment and wait for approval.");
  window.location.href = "login.html";
}

// ===== LOGIN WITH APPROVAL CHECK =====
function loginUser() {
  const user = JSON.parse(localStorage.getItem("user"));

  if (!user) {
    alert("No account found. Please register first.");
    return;
  }

  if (user.status !== "APPROVED") {
    alert("Your account is not approved yet.");
    return;
  }

  localStorage.setItem("isLoggedIn", "true");
  window.location.href = "dashboard.html";
}

// ===== ADMIN SETTINGS =====
const defaultAdminSettings = {
  dashboardEnabled: true,
  uploadEnabled: true,
  insightsEnabled: true,
  maxUploads: 5
};

if (!localStorage.getItem("adminSettings")) {
  localStorage.setItem(
    "adminSettings",
    JSON.stringify(defaultAdminSettings)
  );
}

function getAdminSettings() {
  return JSON.parse(localStorage.getItem("adminSettings"));
}
