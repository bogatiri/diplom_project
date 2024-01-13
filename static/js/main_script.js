const navbar = document.querySelector(".navbar"),
  searchIcon = document.querySelector("#searchIcon"),
  navOpenBtn = document.querySelector(".navOpenBtn"),
  navCloseBtn = document.querySelector(".navCloseBtn"),
  homeSection = document.querySelector(".home");
const inputField = document.querySelector(".input-field textarea"),
  todoList = document.querySelector(".todoList"),
  pendingNum = document.querySelector(".pending-num"),
  clearButton = document.querySelector(".clear-button"),
  addTaskButton = document.querySelector(".add-task");
const body = document.querySelector("body"),
  sidebar = body.querySelector(".sidebar"),
  toggle = body.querySelector(".toggle"),
  searchBtn = body.querySelector(".search-box"),
  modeSwitch = body.querySelector(".toggle-switch"),
  modeText = body.querySelector(".mode-text");




document.addEventListener('DOMContentLoaded', function () {
  // Вызовите функцию загрузки секций после полной загрузки DOM
  loadSections();
});
                                                    // !При нажатии на кнопку поиска
searchIcon.addEventListener("click", () => {
  navbar.classList.toggle("openSearch");
  navbar.classList.remove("openNavbar");
  homeSection.style.right = "0px";
  if (sidebar.classList.contains("close")) {
  } else {
    sidebar.classList.toggle("close");
  }
  if (navbar.classList.contains("openSearch")) {
    return (
      searchIcon.classList.replace("fa-magnifying-glass", "fa-xmark"),
      (searchIcon.style.transform = "translateX(-360px)"),
      (navOpenBtn.style.opacity = "1")
    );
  } else {
    searchIcon.classList.replace("fa-xmark", "fa-magnifying-glass"),
      (searchIcon.style.transform = "translateX(0)");
  }
});

                                                      // !При нажатии на кнопку открытия меню
navOpenBtn.addEventListener("click", () => {
  navbar.classList.add("openNavbar");
  navOpenBtn.style.opacity = "0";
  navbar.classList.remove("openSearch");
  searchIcon.style.transform = "translateX(0)";
  if (sidebar.classList.contains("close")) {
  } else {
    sidebar.classList.toggle("close");
  }
  searchIcon.classList.replace("fa-xmark", "fa-magnifying-glass");
  searchIcon.style.transform = "translateX(0)";
  homeSection.style.right = "306px";
});

                                                      // !При нажатии на кнопку закрытия меню
navCloseBtn.addEventListener("click", () => {
  navbar.classList.remove("openNavbar");
  navOpenBtn.style.opacity = "1";
  homeSection.style.right = "0px";
});

                                                      // !При нажатии на стрелочку у сайдбара
toggle.addEventListener("click", () => {
  sidebar.classList.toggle("close");
  navbar.classList.remove("openNavbar");
  navbar.classList.remove("openSearch");
  searchIcon.classList.replace("fa-xmark", "fa-magnifying-glass");
  navOpenBtn.style.opacity = 1;
  searchIcon.style.transform = "translateX(0)";
  homeSection.style.right = "0px";
});

                                                      // !При нажатии на кнопку поиска сайдбара
searchBtn.addEventListener("click", () => {
  sidebar.classList.remove("close");
  navbar.classList.remove("openNavbar");
  navbar.classList.remove("openSearch");
  searchIcon.classList.replace("fa-xmark", "fa-magnifying-glass");
  navOpenBtn.style.display = "block";
  searchIcon.style.transform = "translateX(0)";
  homeSection.style.right = "250px";
  navOpenBtn.style.opacity = "1";
});

                                                      // !Смена темы
modeSwitch.addEventListener("click", () => {
  const currentTheme = body.classList.contains("dark") ? "light" : "dark";
  body.classList.toggle("dark");
  if (body.classList.contains("dark")) {
    modeText.innerText = "Light Mode";
  } else {
    modeText.innerText = "Dark Mode";
  }
  saveThemeToServer(currentTheme);
});

document.getElementById("avatar").addEventListener("change", function (e) {
  document.getElementById("upload-form").submit();
});

                                                      // !Сохранение темы на сервере
function saveThemeToServer(theme) {
  const xhr = new XMLHttpRequest();
  xhr.open("POST", "/save_theme", true);
  xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  xhr.send("theme=" + theme);
  xhr.onreadystatechange = function () {
  };
}


function deleteTask(e) {                              // !Удаление задачи
  const liTag = e.currentTarget.parentElement;
  liTag.remove();
}


function saveTaskToServer(taskDescription, sectionId) {
  fetch("/add_task", {
    method: "POST",
    body: new URLSearchParams({ task_description: taskDescription, section_id: sectionId }),
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  })
  .then(response => response.json())
  .then(data => {
    console.log("Задача успешно добавлена:", data); 
    // Дополнительные действия при успешном добавлении задачи
  })
  .catch(error => {
    console.error("Ошибка при добавлении задачи:", error);
  });
}


addTaskButton.addEventListener("click", () => {
  // Создаем новый li-элемент
  let liTag = document.createElement("li");
  liTag.classList.add("list");

  // Создаем новый чекбокс
  let checkbox = document.createElement("input");
  checkbox.type = "checkbox";

  // Создаем блок для ввода задачи
  let inputTask = document.createElement("div");
  inputTask.classList.add("input-task");

  // Создаем текстовое поле для задачи
  let textarea = document.createElement("textarea");
  textarea.id = "textarea-task";
  textarea.classList.add("written-task");
  textarea.placeholder = "Write Your Task";
  textarea.onkeydown = function (event) {
    return event.key !== 'Enter';
  };

  // Создаем иконку корзины для удаления задачи
  let trashIcon = document.createElement("i");
  trashIcon.classList.add("fa-solid", "fa-trash");
  trashIcon.onclick = function (event) {
    deleteTask(event);
  };

  // Получаем идентификатор секции
  let sectionId = document.getElementById('section-name').getAttribute('data-section-id');

  // Добавляем элементы в li-элемент
  liTag.appendChild(checkbox);
  liTag.appendChild(inputTask);
  inputTask.appendChild(textarea);
  liTag.appendChild(trashIcon);

  // Добавляем li-элемент в todoList
  todoList.appendChild(liTag);

  // Активируем текстовое поле при создании
  textarea.focus();

  // Устанавливаем обработчик события потери фокуса
  textarea.addEventListener('blur', function () {
    // Если поле пусто, удаляем li-элемент
    if (textarea.value.trim() === '') {
      liTag.remove();
    } else {
      // Если поле не пусто, сохраняем задачу в базу данных
      saveTaskToServer(textarea.value, sectionId);
    }
  });
});


function addSection() {
  const sectionName = document.getElementById('section-name').value;
  fetch('/add_section', {
    method: 'POST',
    body: new URLSearchParams({ section_name: sectionName }),
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  })
  .then(response => response.json())
  .then(data => {
    console.log('Секция успешно добавлена:', data);
console.log('Функция addSection() вызвана');
    // После добавления секции обновляем список секций
    loadSections();
  })
  .catch(error => {
    console.error('Ошибка при добавлении секции:', error);
    console.log(sectionName)
  });
}

// Функция для добавления задачи

/* function addTask() {
  const taskDescription = prompt('Введите описание задачи:');

  let sectionId = document.getElementById('section-name').dataset.sectionId;

  fetch('/add_task', {
    method: 'POST',
    body: new URLSearchParams({
      task_description: taskDescription,
      section_id: sectionId,
    }),
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  })
  .then(response => response.json())
  .then(data => {
    console.log('Задача успешно добавлена:', data);
    console.log('sectionId');
    console.log(taskDescription);
    loadTasks(sectionId);
  })
  .catch(error => {
    console.error('Ошибка при добавлении задачи:', error);
    console.log(taskDescription);
    console.log(sectionId)
  });
} */

// Функция для загрузки секций
function loadSections() {
  fetch('/get_sections')
  .then(response => response.json())
  .then(data => {
    console.log('Секции успешно загружены:', data);

    // Отобразить секции в соответствующем списке
    const sectionsList = document.getElementById('sections-list');
    //sectionsList.innerHTML = '';//!!!!!!!!!!!!!!!
//!!!!!!!!!!!!!!!
/*     data.forEach(section => {//!!!!!!!!!!!!!!!
      const li = document.createElement('li');//!!!!!!!!!!!!!!!
      li.textContent = section.name_of_section;  //!!!!!!!!!!!!!!!
      sectionsList.appendChild(li);//!!!!!!!!!!!!!!!
    }); *///!!!!!!!!!!!!!!!
  })
  .catch(error => {
    console.error('Ошибка при загрузке секций:', error);
  });
}



// Функция для загрузки задач для указанной секции
function loadTasks(sectionId) {
  // Отправка запроса на сервер для получения задач
  fetch(`/get_tasks?section_id=${sectionId}`)
  .then(response => response.json())
  .then(data => {
    console.log('Задачи успешно загружены:', data);

    // Отобразить задачи в соответствующем списке
    const tasksList = document.getElementById(`task-section-${sectionId}`);
    tasksList.innerHTML = '';

    data.forEach(task => {
      const li = document.createElement('li');
      li.textContent = task.task_description;
      tasksList.appendChild(li);
    });
  })
  .catch(error => {
    console.error('Ошибка при загрузке задач:', error);
  });
}

/* // Вызываем функцию загрузки секций при загрузке страницы
loadSections(); */




$(document).ready(function() {
  $('#section-name').on('blur', function() {
    var newText = $(this).val();
    var sectionId = $(this).data('section-id');  
    console.log(sectionId)
    $.ajax({
      type: 'POST',
      url: '/save_name_of_section',
      data: { text: newText, section_id: sectionId },
      success: function(response) {
        console.log('Изменения сохранены успешно');
      }, 
      error: function(error) {
        console.error('Ошибка при сохранении изменений:', error);
      }
    });
  });
});


