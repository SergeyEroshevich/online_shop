"use strict"

const ratings = document.querySelectorAll('.rating')
if (ratings.length > 0){
    initRatings();
}

// основная функция
function initRatings() {
    let ratingActive, ratingValue;
    // бегаем по всем рейтингам на странице
    for (let index = 0; index < ratings.length; index++) {
        const rating = ratings[index];
        initRating(rating);
    }

    // инициализируем конкретный рейтинг
    function initRating(rating) {
        initRatingVars(rating);
        setRatingActiveWidth();
    }

    // инициализация переменных
    function initRatingVars(rating) {
        ratingActive = rating.querySelector('.rating__active');
        ratingValue = rating.querySelector('.rating__value');
    }

    // изменяем ширину активных звезд
    function setRatingActiveWidth(index = ratingValue.innerHTML) {
        const ratingActiveWidth = index / 0.05;
        ratingActive.style.width = `${ratingActiveWidth}%`;
        
    }
}