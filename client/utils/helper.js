export function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
}

export function initPopovers() {
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl));
}

export function makeTablesResponsive() {
    const tables = document.querySelectorAll('table');
    tables.forEach(table => {
        table.classList.add('table', 'table-striped', 'table-hover');
        const wrapper = document.createElement('div');
        wrapper.classList.add('table-responsive');
        table.parentNode.insertBefore(wrapper, table);
        wrapper.appendChild(table);
    });
}

export function animateCardsOnScroll() {
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        const cardTop = card.getBoundingClientRect().top;
        const windowHeight = window.innerHeight;
        if (cardTop < windowHeight - 100) {
            card.classList.add('animate__animated', 'animate__fadeIn');
        }
    });
}

export function setupScrollAnimation() {
    window.removeEventListener('scroll', animateCardsOnScroll); // prevent duplicate
    window.addEventListener('scroll', animateCardsOnScroll);
    animateCardsOnScroll(); // initial
}