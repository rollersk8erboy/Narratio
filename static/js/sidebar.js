function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    const content = document.querySelector('.content');
    const overlay = document.querySelector('.overlay');

    content.style.transition = 'all 0.3s';
    sidebar.style.transition = 'all 0.3s';
    overlay.style.transition = 'all 0.3s';

    if (window.getComputedStyle(sidebar).getPropertyValue('margin-left') === '0px') {
        sidebar.style.marginLeft = '-250px';
        content.style.marginLeft = '0px';
        overlay.style.display = 'none';
    } else {
        sidebar.style.marginLeft = '0px';
        if (window.innerWidth <= 768) {
            content.style.marginLeft = '0px';
            overlay.style.display = 'block';
        } else {
            content.style.marginLeft = '250px';
        }
    }
}