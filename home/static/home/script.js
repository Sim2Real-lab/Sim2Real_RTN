function toggleMenu() {
    const nav = document.querySelector('.nav');
    const toggleBtn = document.getElementById('menuToggleBtn');

    nav.classList.toggle('active');

    // Change icon between ☰ and ✖
    if (nav.classList.contains('active')) {
      toggleBtn.textContent = '✖';
    } else {
      toggleBtn.textContent = '☰';
    }
  }