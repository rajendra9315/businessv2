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
