//проверка авторизации
document.addEventListener("DOMContentLoaded", function() {
    const favoriteBtn = document.getElementById("favorites-btn");
    const tripsBtn = document.getElementById("trips-btn");
    const favoBtn = document.getElementById("favo-btn");
    const tripBtn = document.getElementById("trip-btn");
    // Функция для отображения модального окна
    const showModal = () => {
        const modal = new bootstrap.Modal(document.getElementById("exampleModalToggle"));
        modal.show();
    };
    if (favoriteBtn) {
        favoriteBtn.addEventListener("click", function(event) {
            if (!window.isAuthenticated) {
                event.preventDefault();
                showModal();
            }
        });
    }
    if (tripsBtn) {
        tripsBtn.addEventListener("click", function(event) {
            if (!window.isAuthenticated) {
                event.preventDefault();
                showModal();
            }
        });
    }
    if (favoBtn) {
        favoBtn.addEventListener("click", function(event) {
            if (!window.isAuthenticated) {
                event.preventDefault();
                showModal();
            }
        });
    }
    if (tripBtn) {
        tripBtn.addEventListener("click", function(event) {
            if (!window.isAuthenticated) {
                event.preventDefault();
                showModal();
            }
        });
    }
});



// payments
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
        if (day < 1 || day > 31) isValid = false;
        if (month < 1 || month > 12) isValid = false;
        if (year < 1900 || year > 2099) isValid = false;
        if (month === 4 || month === 6 || month === 9 || month === 11) {
            if (day > 30) isValid = false;
        }
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

document.querySelector('.card_cvv').addEventListener('input', function(e) {
    // Удаляем все символы, кроме цифр
    this.value = this.value.replace(/\D/g, '');
});