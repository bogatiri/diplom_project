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


let taskId;

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

document.getElementById("avatar").addEventListener("change", function () {
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



function findClosestLi(element) {
  while (element && element.tagName !== 'LI') {
    element = element.parentElement;
  }
  return element;
}

function deleteTask(taskId) {
  const liTag = findClosestLi(document.querySelector(`[data-task-id="${taskId}"]`));
  console.log("liTag:", liTag);
  if (liTag) {
    console.log("Deleting task with ID:", taskId);
    liTag.remove();
    deleteTaskFromServer(taskId);
  } else {
    deleteTaskNow(e);
    console.log("Element not found for task ID:", taskId);
  }
}
function deleteTaskNow(e) {
  const liTag = e.currentTarget.parentElement;
  const taskId = liTag.getAttribute("data-task-id");
  liTag.remove();
  deleteTaskFromServer(taskId); // Функция для удаления задачи из базы данных
}


function deleteTaskFromServer(taskId) {
  fetch("/delete_task", {
    method: "POST",
    body: new URLSearchParams({ task_id: taskId }),
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  })
  .then(response => response.json())
  .then(data => {
    console.log("Задача успешно удалена:", data);
  })
  .catch(error => {
    console.error("Ошибка при удалении задачи:", error);
  });
}

function saveTaskToServer(taskDescription, sectionId, liTag) {
  fetch("/add_task", {
    method: "POST",
    body: new URLSearchParams({ task_description: taskDescription, section_id: sectionId }),
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  })
  .then(response => response.json())
  .then(data => {
    taskId = data.task_id;
    if (data.status === "success") {
      console.log("Задача успешно добавлена:", taskId);
      // Убедимся, что taskId не равен null или undefined, прежде чем устанавливать атрибут
      if (taskId != null) {
        liTag.setAttribute("data-task-id", taskId);
      }
      //taskId = liTag.getAttribute("data-task-id");
      // Вызываем функцию добавления задачи на форму с полученным идентификатором
      /* addTaskToForm(taskDescription, sectionId, taskId); */
    } else {
      console.error("Ошибка при добавлении задачи:", data.message);
    }
  })
  .catch(error => {
    console.error("Ошибка при добавлении задачи:", error);
  });
}

addTaskButton.addEventListener("click", () => {
  let liTag = document.createElement("li");
  liTag.classList.add("list");
  let checkbox = document.createElement("input");
  checkbox.type = "checkbox";
  checkbox.id = `checkbox-task-${taskId}`;

  let inputTask = document.createElement("div");
  inputTask.classList.add("input-task");
  
  let textarea = document.createElement("textarea");
  textarea.classList.add("written-task");
  textarea.id = `textarea-task-${taskId}`;
  textarea.placeholder = "Write Your Task";
  textarea.onkeydown = function (event) {
    return event.key !== 'Enter';
  };

  let trashIcon = document.createElement("i");
  trashIcon.classList.add("fa-solid", "fa-trash");
  trashIcon.onclick = function (event) {
    taskId = liTag.getAttribute("data-task-id");
    console.log("Удаляется", taskId);
    deleteTask(taskId);
  };

  let sectionId = document.getElementById('section-name').getAttribute('data-section-id');
  liTag.setAttribute('data-section-id', sectionId);

  inputTask.appendChild(textarea);
  liTag.appendChild(checkbox);
  liTag.appendChild(inputTask);
  liTag.appendChild(trashIcon);
  let taskDescription = textarea.value;
  //let taskId = liTag.getAttribute("data-task-id");
  saveTaskToServer(taskDescription, sectionId, liTag)
  todoList.appendChild(liTag);




  liTag.addEventListener("click", function () {
    taskId = this.getAttribute("data-task-id");
    //liTag.setAttribute("data-task-id", taskId);
    console.log("click", taskId);
  });

// Находим все textarea элементы внутри todoList
var textareas = todoList.querySelectorAll('textarea');

// Добавляем обработчик события focus для каждого textarea
textareas.forEach(textarea => {
  textarea.addEventListener('focus', function () {
    // Находим ближайший родительский элемент liTag
    var liTag = this.closest('li');
    // Проверяем, найден ли liTag
    if (liTag && liTag.tagName === 'LI') {
      // Получаем значение атрибута "data-task-id"
      //taskId = liTag.getAttribute('data-task-id');
      // Печатаем значение в консоль
      console.log('Value of data-task-id attribute:', taskId);
    }
  });
});

  textarea.focus();

  textarea.addEventListener("input", function() {
    // Устанавливаем высоту textarea равной высоте скролла
    // Это позволяет убрать лишний пространство и полосу прокрутки
    textarea.style.height = textarea.scrollHeight + "px";
    liTag.style.minHeight = textarea.scrollHeight + "px";
  });

  textarea.addEventListener('blur', function () {
    let taskDescription = textarea.value;
    console.log("asdasdasd", taskId);
    if (taskId) {
      if (taskDescription.trim() === '') {
        liTag.remove(); 
        deleteTaskFromServer(taskId);
      } else {
        updateTaskOnServer(taskId, taskDescription)
      }
    } else {
        console.error("taskId is undefined");
    } 
  }); 
});

function updateTaskOnServer(taskId, taskDescription, liTag) {
  fetch("/update_task", {
    method: "POST",
    body: new URLSearchParams({ task_id: taskId, task_description: taskDescription }),
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  })
  .then(response => response.json())
  .then(data => {
    if (data.status === "success") {
      console.log("Задача успешно обновлена:", data.task_id);
      console.log(data.task_description);
    } else {
      console.error("Ошибка при обновлении задачи:", data.message);
    }
  })
  .catch(error => {
    console.error("Ошибка при обновлении задачи:", error);
  });
}


// Функция для загрузки всех секций пользователя
function loadSections() {
  // Отправка запроса на сервер для получения секций
  fetch('/get_sections')
  .then(response => response.json())
  .then(data => {
    console.log('Секции успешно загружены:', data);
    
    // Загрузить задачи для каждой секции
    data.forEach(section => {
      loadTasks(section.id);
      console.log("section",section.id)
    });
  })
  .catch(error => {
    console.error('Ошибка при загрузке секций:', error);
  });
}

// Функция для загрузки задач для указанной секции
function loadTasks(sectionId) {
  // Получаем элемент секции с использованием переданного sectionId
  var taskSection = document.querySelector(`[data-section-id="${sectionId}"]`);
  console.log("taskSection", taskSection);

  if (!taskSection) {
    console.log("taskSection", sectionId);
    console.error(`Элемент с атрибутом "data-section-id=${sectionId}" не найден`);
    return;
  }

  // Отправляем запрос на сервер
  fetch(`/get_tasks?sectionId=${sectionId}`)
    .then(response => response.json())
    .then(data => {
      console.log('Ответ от сервера:', data);

      // Проверяем, есть ли ключ "tasks" в данных
      if (data.hasOwnProperty('tasks') && Array.isArray(data.tasks) && data.tasks.length > 0) {
        console.log('Задачи успешно загружены:', data.tasks);

        // НЕ очищаем содержимое элемента

        // Добавляем задачи в элемент
        data.tasks.forEach(task => {
          // Создаем новый li-элемент
          let liTag = document.createElement("li");
          liTag.classList.add("list");
          liTag.setAttribute("data-task-id", task.id);
          console.log("id", liTag.getAttribute("data-task-id"));
          // Создаем новый чекбокс
          let checkbox = document.createElement("input");
          checkbox.type = "checkbox";
          checkbox.id = `checkbox-task-${task.id}`;
  
          // Создаем блок для ввода задачи
          let inputTask = document.createElement("div");
          inputTask.classList.add("input-task");
  
          // Создаем текстовое поле для задачи
          let textarea = document.createElement("textarea");
          textarea.id = `textarea-task-${task.id}`;
          textarea.classList.add("written-task");
          textarea.value = task.task_description; // Задаем описание задачи
  
          // Создаем иконку корзины для удаления задачи
          let trashIcon = document.createElement("i");
          trashIcon.classList.add("fa-solid", "fa-trash");
          trashIcon.onclick = function (event) {
            console.log(task.id);
            //const taskId = event.currentTarget.parentElement.getAttribute("data-task-id");
            deleteTask(task.id);
          };
  
          // Добавляем элементы в li-элемент
          liTag.appendChild(checkbox);
          liTag.appendChild(inputTask);
          inputTask.appendChild(textarea);
          liTag.appendChild(trashIcon);
  
          // Добавляем li-элемент в taskSection
          document.body.appendChild(liTag);
          todoList.appendChild(liTag);
          liTag.appendChild(trashIcon);
          let foundLiTag = document.querySelector(`[data-task-id="${task.id}"]`);
          console.log(foundLiTag);

          liTag.addEventListener("click", function () {
            taskId = this.getAttribute("data-task-id");
          });


          textarea.addEventListener("input", function() {
            // Устанавливаем высоту textarea равной высоте скролла
            // Это позволяет убрать лишний пространство и полосу прокрутки
            textarea.style.height = textarea.scrollHeight + "px";
            liTag.style.minHeight = textarea.scrollHeight + "px";
          });

          textarea.addEventListener('blur', function () {
            let taskDescription = textarea.value;
            if (taskId) {
              if (taskDescription.trim() === '') {
                liTag.remove(); 
                deleteTaskFromServer(task.id);
              } else {
                updateTaskOnServer(task.id, taskDescription)
              }
            } else {
                console.error("taskId is undefined");
            } 
          });
                    // Получаем высоту скролла textarea
          var scrollHeight = textarea.scrollHeight;
          // Устанавливаем высоту textarea равной высоте скролла
          textarea.style.height = scrollHeight + "px";
          // Устанавливаем минимальную высоту liTag равной высоте скролла
          liTag.style.minHeight = scrollHeight + "px";
        });
      } else {
        console.log('Данные не содержат задач.');
      }
    })
    .catch(error => {
      console.error('Ошибка при загрузке задач:', error);
    });
}

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
  }
  )
  .catch(error => {
    console.error('Ошибка при добавлении секции:', error);
    console.log(sectionName)
  }
  );
}

// Функция для добавления секции

$(document).ready(function() {
  $('#section-name').on('blur', function() {
    var newText = $(this).val();
    var sectionId = $(this).data('section-id');  
    console.log(sectionId)
    $.ajax({
      type: 'POST',
      url: '/save_name_of_section',
      data: { text: newText, section_id: sectionId },
      success: function() { // Remove the unused 'response' parameter
        console.log('Изменения сохранены успешно');
      }, 
      error: function(error) {
        console.error('Ошибка при сохранении изменений:', error);
      }
    });
  });
});

/* function addSection() {
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
} */
