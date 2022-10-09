const nav = document.querySelector('.navbar');
console.log(nav)

window.addEventListener('scroll', () => {
    let scroll = window.scrollY;
    if (scroll > 70) {
        nav.classList.add('navbar-change')
    }

    else {
        nav.classList.remove('navbar-change')
    }
})
