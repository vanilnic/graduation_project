//проверка авторизации
document.addEventListener("DOMContentLoaded", function() {
    const favoriteBtn = document.getElementById("favorites-btn");
    const tripsBtn = document.getElementById("trips-btn");
    const favoBtn = document.getElementById("favo-btn");
    const tripBtn = document.getElementById("trip-btn");

    const moreRoomLinks = document.querySelectorAll(".more_room_link");
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
    if (moreRoomLinks) {
        moreRoomLinks.forEach(link => {
            link.addEventListener("click", function (event) {
                if (!window.isAuthenticated) {
                    event.preventDefault();
                    showModal();
                }
            });
        });
    }
});



// payments
document.querySelector('.card_number').addEventListener('input', function(e) {
    let value = e.target.value.replace(/\D/g, ''); // только цифры
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
    const allowedKeys = [8, 9, 37, 38, 39, 40, 46]; // управление
    if (allowedKeys.includes(e.keyCode)) return;

    if (
        (e.keyCode < 48 || e.keyCode > 57) &&
        (e.keyCode < 96 || e.keyCode > 105)
    ) {
        e.preventDefault();
    }
});

// =====================
// Форматирование и валидация даты (MM/YY)
// =====================
document.querySelector('.card_date').addEventListener('input', function(e) {
    let input = e.target;
    let value = input.value.replace(/\D/g, ''); // только цифры

    if (value.length >= 3) {
        input.value = value.slice(0, 2) + '/' + value.slice(2, 4);
    } else {
        input.value = value;
    }

    validateExpiryDate(input);
});

function validateExpiryDate(input) {
    const errorElement = input.nextElementSibling;
    const parts = input.value.split('/');
    let isValid = false;

    if (parts.length === 2) {
        let [month, year] = parts.map(p => parseInt(p, 10));
        const now = new Date();
        const currentMonth = now.getMonth() + 1;
        const currentYear = now.getFullYear() % 100;

        if (month >= 1 && month <= 12) {
            if (year > currentYear || (year === currentYear && month >= currentMonth)) {
                isValid = true;
            }
        }
    }

    if (!isValid && input.value.length === 5) {
        input.style.borderColor = 'red';
        if (errorElement) errorElement.style.display = 'inline';
    } else {
        input.style.borderColor = '';
        if (errorElement) errorElement.style.display = 'none';
    }

    return isValid;
}

document.querySelector('.card_date').addEventListener('keydown', function(e) {
    const allowedKeys = [8, 9, 37, 38, 39, 40, 46];
    if (allowedKeys.includes(e.keyCode)) return;

    if (
        (e.keyCode < 48 || e.keyCode > 57) &&
        (e.keyCode < 96 || e.keyCode > 105)
    ) {
        e.preventDefault();
    }
});

// =====================
// Валидация при отправке формы
// =====================
document.querySelector('form')?.addEventListener('submit', function(e) {
    const dateInput = document.querySelector('.card_date');
    if (!validateExpiryDate(dateInput)) {
        e.preventDefault();
        dateInput.focus();
    }
});

// =====================
// Валидация CVV (только цифры)
// =====================
document.querySelector('.card_cvv').addEventListener('input', function(e) {
    this.value = this.value.replace(/\D/g, '');
});