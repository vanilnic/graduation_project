//проверка авторизации
document.addEventListener("DOMContentLoaded", function() {
    const favoriteBtn = document.getElementById("favorites-btn");
    const tripsBtn = document.getElementById("trips-btn");
    // Функция для отображения модального окна
    const showModal = () => {
        const modal = new bootstrap.Modal(document.getElementById("exampleModalToggle"));
        modal.show();
    };
    // Проверка на авторизацию при нажатии на "Избранное"
    if (favoriteBtn) {
        favoriteBtn.addEventListener("click", function(event) {
            if (!window.isAuthenticated) {
                event.preventDefault();
                showModal();
            }
        });
    }
    // Проверка на авторизацию при нажатии на "Мои поездки"
    if (tripsBtn) {
        tripsBtn.addEventListener("click", function(event) {
            if (!window.isAuthenticated) {
                event.preventDefault();
                showModal();
            }
        });
    }
});



// payments
// для input номера карты
document.querySelector('.card_number').addEventListener('input', function(e) {
    // Удаляем все нецифровые символы
    let value = e.target.value.replace(/\D/g, '');
    
    // Добавляем пробелы после каждых 4 цифр
    let formattedValue = '';
    for (let i = 0; i < value.length; i++) {
        if (i > 0 && i % 4 === 0) {
            formattedValue += ' ';
        }
        formattedValue += value[i];
    }
    
    e.target.value = formattedValue;
});
// Запрещаем ввод нецифровых символов
document.querySelector('.card_number').addEventListener('keydown', function(e) {
    // Разрешаем: Backspace, Delete, Tab, стрелки
    if ([8, 9, 37, 38, 39, 40, 46].includes(e.keyCode)) {
        return;
    }
    // Запрещаем всё, кроме цифр
    if (e.keyCode < 48 || e.keyCode > 57) {
        if (e.keyCode < 96 || e.keyCode > 105) { // Проверка numpad
            e.preventDefault();
        }
    }
});
// для input даты
document.querySelector('.card_date').addEventListener('input', function(e) {
    const input = e.target;
    let value = input.value.replace(/\D/g, '');
    // Форматирование
    let formattedValue = '';
    if (value.length > 0) formattedValue = value.slice(0, 2);
    if (value.length > 2) formattedValue += '.' + value.slice(2, 4);
    if (value.length > 4) formattedValue += '.' + value.slice(4, 8);

    input.value = formattedValue;
    
    // Валидация в реальном времени
    validateDateInput(input);
});
// Проверка валидности даты
function validateDateInput(input) {
    const errorElement = input.nextElementSibling;
    const [day, month, year] = input.value.split('.').map(Number);
    
    let isValid = true;
    
    // Проверяем заполненность всех частей
    if (input.value.length === 10) {
        // Проверяем день (1-31)
        if (day < 1 || day > 31) isValid = false;
        // Проверяем месяц (1-12)
        if (month < 1 || month > 12) isValid = false;
        // Проверяем год (1900-2099)
        if (year < 1900 || year > 2099) isValid = false;
        // Дополнительная проверка для месяцев с 30 днями
        if (month === 4 || month === 6 || month === 9 || month === 11) {
            if (day > 30) isValid = false;
        }
        // Проверка февраля (упрощённая, без учёта високосных годов)
        if (month === 2 && day > 28) isValid = false;
    } else if (input.value.length > 0) {
        // Если введена неполная дата, но есть символы
        isValid = false;
    }
    // Подсветка ошибки
    if (!isValid && input.value.length > 0) {
        input.style.borderColor = 'red';
        errorElement.style.display = 'inline';
    } else {
        input.style.borderColor = '';
        errorElement.style.display = 'none';
    }
    return isValid;
}
// Валидация при отправке формы
document.querySelector('form')?.addEventListener('submit', function(e) {
    const dateInput = document.querySelector('.card_date');
    if (!validateDateInput(dateInput)) {
        e.preventDefault();
        dateInput.focus();
    }
});
// Запрет ввода нецифровых символов
document.querySelector('.card_date').addEventListener('keydown', function(e) {
    // Разрешаем: Backspace, Delete, Tab, стрелки
    if ([8, 9, 37, 38, 39, 40, 46].includes(e.keyCode)) return;
    // Запрещаем всё, кроме цифр
    if (e.keyCode < 48 || e.keyCode > 57) {
        if (e.keyCode < 96 || e.keyCode > 105) {
            e.preventDefault();
        }
    }
});






// history
// Обновление значений рядом с ползунками
document.querySelectorAll('.range-slider').forEach(slider => {
    const valueDisplay = slider.nextElementSibling;
    valueDisplay.textContent = slider.value;
    
    slider.addEventListener('input', () => {
        valueDisplay.textContent = slider.value;
    });
});

// Обработка отправки формы
document.getElementById('reviewForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Собираем данные формы
    const formData = {
        rating: document.querySelector('input[name="rating"]:checked')?.value,
        location: document.querySelector('input[name="location"]').value,
        cleanliness: document.querySelector('input[name="cleanliness"]').value,
        comfort: document.querySelector('input[name="comfort"]').value,
        staff: document.querySelector('input[name="staff"]').value,
        value: document.querySelector('input[name="value"]').value,
        comment: document.getElementById('comment').value
    };
    
    console.log('Отправленные данные:', formData);
    alert('Спасибо за ваш отзыв!');
    this.reset();
});
