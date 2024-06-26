let currentSlide = 0;

const navButtonLeft = document.getElementById('nav-button-left');
const navButtonRight = document.getElementById('nav-button-right');

const slides = document.querySelectorAll('.slide');

function showSlide(newIndex) {
    const direction = newIndex > currentSlide ? 'right' : 'left';
    const exitClass = direction === 'right' ? 'slide-exit-left' : 'slide-exit-right';
    const enterClass = direction === 'right' ? 'slide-enter-right' : 'slide-enter-left';

    slides[currentSlide].classList.remove('active');
    slides[currentSlide].classList.add(exitClass);
    slides[currentSlide].addEventListener('animationend', onExitAnimationEnd);

    currentSlide = (newIndex + slides.length) % slides.length;

    slides[currentSlide].classList.remove(exitClass);
    slides[currentSlide].classList.add('active', enterClass);
    slides[currentSlide].addEventListener('animationend', onEnterAnimationEnd);
}

function changeSlide(direction) {
    showSlide(currentSlide + direction);
}

function onExitAnimationEnd(event) {
    event.target.classList.remove('slide-exit-left', 'slide-exit-right');
    event.target.removeEventListener('animationend', onExitAnimationEnd);
}

function onEnterAnimationEnd(event) {
    event.target.classList.remove('slide-enter-left', 'slide-enter-right');
    event.target.removeEventListener('animationend', onEnterAnimationEnd);
}

document.addEventListener('DOMContentLoaded', () => {
    showSlide(currentSlide);

    navButtonLeft.addEventListener('click', () => changeSlide(-1));
    navButtonRight.addEventListener('click', () => changeSlide(1));
});

document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowLeft') {
        changeSlide(-1);
    }
    else if (e.key === 'ArrowRight') {
        changeSlide(1);
    }
})
