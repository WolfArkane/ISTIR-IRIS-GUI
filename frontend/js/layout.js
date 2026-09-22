document.addEventListener('DOMContentLoaded', () => {
  const sidebar = document.getElementById('sidebar');
  const overlay = document.getElementById('sidebar-overlay');
  const burger = document.getElementById('burger-toggle');

  const isMobile = () => window.innerWidth <= 768;

  function toggleSidebar() {
    if (isMobile()) {
      sidebar.classList.toggle('open');
      overlay.classList.toggle('open');
    } else {
      sidebar.classList.toggle('collapsed');
    }
  }

  function closeSidebar() {
    sidebar.classList.remove('open');
    overlay.classList.remove('open');
  }

  burger.addEventListener('click', toggleSidebar);
  overlay.addEventListener('click', closeSidebar);
});