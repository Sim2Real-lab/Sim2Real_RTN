document.addEventListener("DOMContentLoaded", function () {
  // Toggle Team Forms
  const createTeamBtn = document.getElementById("create-team-btn");
  const joinTeamBtn = document.getElementById("join-team-btn");
  const createTeamForm = document.getElementById("create-team-form");
  const joinTeamForm = document.getElementById("join-team-form");

  if (createTeamBtn && joinTeamBtn) {
    createTeamBtn.addEventListener("click", () => {
      createTeamForm.classList.remove("hidden");
      joinTeamForm.classList.add("hidden");
    });

    joinTeamBtn.addEventListener("click", () => {
      joinTeamForm.classList.remove("hidden");
      createTeamForm.classList.add("hidden");
    });
  }

  // Autocomplete with Restriction (Year Field)
  const yearInput = document.getElementById("year");
  const suggestions = document.getElementById("year-suggestions");

  const yearOptions = ["1st Year", "2nd Year", "3rd Year", "4th Year"];

  function showSuggestions(value) {
    suggestions.innerHTML = "";

    const inputValue = value.toLowerCase();
    const filtered = yearOptions.filter(option =>
      option.toLowerCase().includes(inputValue)
    );

    filtered.forEach(option => {
      const li = document.createElement("li");
      li.textContent = option;
      li.classList.add("suggestion-item");
      li.addEventListener("click", () => {
        yearInput.value = option;
        suggestions.innerHTML = "";
        yearInput.setAttribute("data-valid", "true");
      });
      suggestions.appendChild(li);
    });
  }

  if (yearInput) {
    yearInput.addEventListener("input", function () {
      showSuggestions(this.value);
      this.setAttribute("data-valid", "false");
    });

    yearInput.addEventListener("blur", function () {
      const isValid = yearOptions.includes(this.value);
      if (!isValid) {
        this.value = "";
        this.setAttribute("data-valid", "false");
      } else {
        this.setAttribute("data-valid", "true");
      }
      setTimeout(() => suggestions.innerHTML = "", 100); // delay hide to allow click
    });

    document.addEventListener("click", function (e) {
      if (!yearInput.contains(e.target)) {
        suggestions.innerHTML = "";
      }
    });
  }
});
