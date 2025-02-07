// Пример простого скрипта для будущих функций или анимаций
// Используйте этот файл для добавления интерактивных элементов позже

document.addEventListener("DOMContentLoaded", function () {
    // Здесь можно добавить ваши скрипты
    console.log("Сайт загружен и скрипты готовы к работе!");
});

// Пример плавного скролла к якорным ссылкам (если потребуется)
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();

        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});
