// ОТКРЫТИЕ ЗАКРЫТИЕ ВСЕХ БЛОКОВ ПРО ИЗМЕНЕНИЕ
// Окно местописания
function openModal() {document.getElementById('TEXT').style.display = 'block';}
function closeModal() {document.getElementById('TEXT').style.display = 'none';}

// Окно адреса
function openAdress() {document.getElementById('adres').style.display = 'block';}
function closeadress() {document.getElementById('adres').style.display = 'none';}

// Окно о нас
function openAbout_uss() {document.getElementById('about_us').style.display = 'block';}
function about_uss_clos() {document.getElementById('about_us').style.display = 'none';}

// Окно Email
function openEmail() {document.getElementById('open_email').style.display = 'block';}
function clos_Email() {document.getElementById('open_email').style.display = 'none';}

// Окно meting
function openMeting() {document.getElementById('open_meting').style.display = 'block';}
function clos_meting() {document.getElementById('open_meting').style.display = 'none';}

function openRegister() {document.getElementById('open_registers').style.display = 'block';}
function clos_registers() {document.getElementById('open_registers').style.display = 'none';}

// Закрыть, если кликнули мимо окна (по темному фону)
window.onclick = function(event) {
        // Если кликнули по элементу с классом 'modal-overlay' (темный фон)
        if (event.target.classList.contains('modal-overlay')) {
            event.target.style.display = "none";
        }
    }