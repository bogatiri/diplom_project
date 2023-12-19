const navbar = document.querySelector(".navbar"),
    searchIcon = document.querySelector("#searchIcon"),
    navOpenBtn = document.querySelector(".navOpenBtn"),
    navCloseBtn = document.querySelector(".navCloseBtn"),
    homeSection = document.querySelector(".home");
const body = document.querySelector("body"),
    sidebar = body.querySelector(".sidebar"),
    toggle = body.querySelector(".toggle"),
    searchBtn = body.querySelector(".search-box"),
    modeSwitch = body.querySelector(".toggle-switch"),
    modeText = body.querySelector(".mode-text");
    
    // !При нажатии на кнопку поиска
    searchIcon.addEventListener("click", () =>{
        navbar.classList.toggle("openSearch");
        navbar.classList.remove("openNavbar");
        homeSection.style.right = "0px";
    if(sidebar.classList.contains("close")){
    }else{
        sidebar.classList.toggle("close");
    }
    if(navbar.classList.contains("openSearch")){
        return  searchIcon.classList.replace("fa-magnifying-glass", "fa-xmark"),
        searchIcon.style.transform = 'translateX(-360px)',
        navOpenBtn.style.opacity = '1';
    }else{
        searchIcon.classList.replace("fa-xmark", "fa-magnifying-glass"),
        searchIcon.style.transform = 'translateX(0)';
    }
    });

    // !При нажатии на кнопку открытия меню
    navOpenBtn.addEventListener("click", () =>{
        navbar.classList.add("openNavbar");
        navOpenBtn.style.opacity = '0';
        navbar.classList.remove("openSearch");
        searchIcon.style.transform = 'translateX(0)';
    if(sidebar.classList.contains("close")){
    }else{
        sidebar.classList.toggle("close");
    }
        searchIcon.classList.replace("fa-xmark", "fa-magnifying-glass");
        searchIcon.style.transform = 'translateX(0)';
        homeSection.style.right = "306px";
    })

    // !При нажатии на кнопку закрытия меню
    navCloseBtn.addEventListener("click", () =>{
        navbar.classList.remove("openNavbar");
        navOpenBtn.style.opacity = '1';
        homeSection.style.right = "0px";
    })

    // !При нажатии на стрелочку у сайдбара
    toggle.addEventListener("click", () =>{
        sidebar.classList.toggle("close");
        navbar.classList.remove("openNavbar");
        navbar.classList.remove("openSearch");
        searchIcon.classList.replace("fa-xmark", "fa-magnifying-glass");
        navOpenBtn.style.opacity = 1;
        searchIcon.style.transform = 'translateX(0)';
        homeSection.style.right = "0px";
        });
    
    // !При нажатии на кнопку поиска сайдбара
    searchBtn.addEventListener("click", () =>{
    sidebar.classList.remove("close");
    navbar.classList.remove("openNavbar");
    navbar.classList.remove("openSearch");
    searchIcon.classList.replace("fa-xmark", "fa-magnifying-glass");
    navOpenBtn.style.display = 'block';
    searchIcon.style.transform = 'translateX(0)';
    homeSection.style.right = "250px";
    navOpenBtn.style.opacity = '1';
    });

    // Смена темы
    modeSwitch.addEventListener("click", () =>{
    const currentTheme = body.classList.contains("dark") ? "light" : "dark";
    body.classList.toggle("dark");
    if(body.classList.contains("dark")){
        modeText.innerText = "Light Mode"
    }else{
        modeText.innerText = "Dark Mode"
    }
    saveThemeToServer(currentTheme);
    });

// Сохранение темы на сервере
function saveThemeToServer(theme) {
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/save_theme', true);  // Используем маршрут, соответствующий вашему Flask-приложению
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.send('theme=' + theme);

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            console.log(xhr.responseText); // Распечатываем ответ сервера, если нужно
        }
    };
}
