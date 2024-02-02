const navbar = document.querySelector(".navbar"),
  searchIcon = document.querySelector("#searchIcon"),
  navOpenBtn = document.querySelector(".navOpenBtn"),
  navCloseBtn = document.querySelector(".navCloseBtn"),
  homeSection = document.querySelector(".home");
const inputField = document.querySelector(".input-field textarea"),
  todoList = document.querySelector(".todoList"),
  pendingNum = document.querySelector(".pending-num"),
  clearButton = document.querySelector(".clear-button"),
  addSectionButtons = document.querySelector(".add-section");
const body = document.querySelector("body"),
  sidebar = body.querySelector(".sidebar"),
  toggle = body.querySelector(".toggle"),
  searchBtn = body.querySelector(".search-box"),
  modeSwitch = body.querySelector(".toggle-switch"),
  modeText = body.querySelector(".mode-text");

document.addEventListener("DOMContentLoaded", function () {
  loadSections();
});

searchIcon.addEventListener("click", () => {
  // !При нажатии на кнопку поиска
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

navOpenBtn.addEventListener("click", () => {
  // !При нажатии на кнопку открытия меню
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

navCloseBtn.addEventListener("click", () => {
  // !При нажатии на кнопку закрытия меню
  navbar.classList.remove("openNavbar");
  navOpenBtn.style.opacity = "1";
  homeSection.style.right = "0px";
});

toggle.addEventListener("click", () => {
  // !При нажатии на стрелочку у сайдбара
  sidebar.classList.toggle("close");
  navbar.classList.remove("openNavbar");
  navbar.classList.remove("openSearch");
  searchIcon.classList.replace("fa-xmark", "fa-magnifying-glass");
  navOpenBtn.style.opacity = 1;
  searchIcon.style.transform = "translateX(0)";
  homeSection.style.right = "0px";
});

searchBtn.addEventListener("click", () => {
  // !При нажатии на кнопку поиска сайдбара
  sidebar.classList.remove("close");
  navbar.classList.remove("openNavbar");
  navbar.classList.remove("openSearch");
  searchIcon.classList.replace("fa-xmark", "fa-magnifying-glass");
  navOpenBtn.style.display = "block";
  searchIcon.style.transform = "translateX(0)";
  homeSection.style.right = "250px";
  navOpenBtn.style.opacity = "1";
});

modeSwitch.addEventListener("click", () => {
  // !Смена темы
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

function saveThemeToServer(theme) {
  // !Сохранение темы на сервере
  const xhr = new XMLHttpRequest();
  xhr.open("POST", "/save_theme", true);
  xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  xhr.send("theme=" + theme);
  xhr.onreadystatechange = function () {};
}

function findClosestLi(element) {
  // !Функция для нахождения ближайшего Li
  while (element && element.tagName !== "DIV") {
    element = element.parentElement;
  }
  return element;
}

function deleteTask(taskId) {
  // !Функция для Удаления задачи с фронта
  const liTag = findClosestLi(
    document.querySelector(`[data-task-id="${taskId}"]`)
  );
  if (liTag) {
    liTag.remove();
    deleteTaskFromServer(taskId);
  } else {
    deleteTaskNow(e);
  }
}
function deleteTaskNow(e) {
  const liTag = e.currentTarget.parentElement;
  const taskId = liTag.getAttribute("data-task-id");
  liTag.remove();
  deleteTaskFromServer(taskId);
}

function deleteTaskFromServer(taskId) {
  // !Функция для удаления задачи с базы
  fetch("/delete_task", {
    method: "POST",
    body: new URLSearchParams({ task_id: taskId }),
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  })
    .then((response) => response.json())
    .then((data) => {})
    .catch((error) => {
      console.error("Ошибка при удалении задачи:", error);
    });
}

function saveTaskToServer(taskDescription, liTag) {
  // !Функция для сохранения задачи в базу
  let formData = new FormData();
  formData.append("task_description", taskDescription);
  formData.append("section_id", liTag.getAttribute("data-section-id"));
  fetch("/add_task", {
    method: "POST",
    body: formData,
  })
    .then(function (response) {
      if (response.ok) {
        return response.json();
      } else {
        console.error(
          "Ошибка при добавлении задачи:",
          response.status,
          response.statusText
        );
      }
    })
    .then(function (data) {
      if (data.status == "success") {
        let taskId = data.task_id;
        liTag.setAttribute("data-task-id", taskId);
        let sectionId = liTag.getAttribute("data-section-id");
      } else {
        console.error("Ошибка при добавлении задачи:", data.message);
      }
    })
    .catch(function (error) {
      console.error("Ошибка при добавлении задачи:", error);
    });
}

function updateTaskOnServer(taskId, taskDescription, checked) {
  // !Функция для обновления значения задачи в базе
  fetch("/update_task", {
    method: "POST",
    body: new URLSearchParams({
      task_id: taskId,
      task_description: taskDescription,
      task_checked: checked,
    }),
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.status === "success") {
      } else {
        console.error("Ошибка при обновлении задачи:", data.message);
      }
    })
    .catch((error) => {
      console.error("Ошибка при обновлении задачи:", error);
    });
}

async function loadSections() {
  // !Функция, которая подгружает секции на страницу при обновлении
  const response = await fetch("/get_sections");
  const data = await response.json();
  for (const section of data) {
    let homeContainer = document.createElement("div");
    homeContainer.className = "home_container board"; //?
    homeContainer.setAttribute("data-section-id", section.id);
    // homeContainer.setAttribute("id", section.id);
    homeContainer.draggable = "true";
    let inputField = document.createElement("div");
    inputField.className = " input-field";
    inputField.classList.add("board-column-header");
    let textarea = document.createElement("textarea");
    textarea.name = "section-name";
    textarea.id = section.id;
    textarea.placeholder = "Print your title here";
    textarea.value = section.name_of_section;
    inputField.appendChild(textarea);
    let link = document.createElement("a");
    link.href = "#";
    let icon = document.createElement("i");
    icon.className = "fa-solid fa-ellipsis note-icon";
    link.appendChild(icon);
    inputField.appendChild(link);
    homeContainer.appendChild(inputField);
    let todoList = document.createElement("div");
    todoList.className = "todoList";
    todoList.classList.add("board-column-content-wrapper");
    todoList.id = section.id;
    homeContainer.appendChild(todoList);
    let listbtn = document.createElement("div");
    listbtn.className = "listbtn";
    listbtn.id = section.id;
    let plusIcon = document.createElement("i");
    plusIcon.className = "fa-solid fa-plus addTask";
    plusIcon.id = section.id;
    listbtn.appendChild(plusIcon);
    let button = document.createElement("button");
    button.className = "add-task";
    button.textContent = "Add Task";
    button.id = section.id;
    button.addEventListener("click", () => {
      // !Функция для добавления задач в подгруженных секциях
      let taskId = Math.random().toString(36);
      let liTag = document.createElement("div");
      liTag.classList.add("list"); //?
      liTag.classList.add("board-item");
      let checkbox = document.createElement("input");
      checkbox.type = "checkbox";
      checkbox.id = `checkbox-task-${taskId}`;
      checkbox.id = `checkbox-task-${taskId}`;
      let inputTask = document.createElement("div");
      inputTask.classList.add("input-task");
      let textarea = document.createElement("textarea");
      textarea.classList.add("written-task");
      textarea.id = `textarea-task-${taskId}`;
      textarea.placeholder = "Write Your Task";
      textarea.onkeydown = function (event) {
        return event.key !== "Enter";
      };
      let trashIcon = document.createElement("i");
      trashIcon.classList.add("fa-solid", "fa-trash");
      trashIcon.onclick = function (event) {
        // !Функция удаления задачи по клику на иконку, надо добавить подтверждение на самом деле
        taskId = liTag.getAttribute("data-task-id");
        deleteTask(taskId);
      };
      let sectionId = button.id;
      liTag.setAttribute("data-section-id", sectionId);
      liTag.setAttribute("data-task-id", taskId);
      inputTask.appendChild(textarea);
      liTag.appendChild(checkbox);
      liTag.appendChild(inputTask);
      liTag.appendChild(trashIcon);
      let taskDescription = textarea.value;
      saveTaskToServer(taskDescription, liTag);
      todoList.appendChild(liTag);
      textarea.addEventListener("focus", function () {
        // !Функция которая должна что-то делать при фокусе, но нихуя не делает
        var liTag = this.closest("div");
        taskId = liTag.getAttribute("data-task-id");
      });

      textarea.focus();
      textarea.addEventListener("input", function () {
        // !Функция которая при вводе в textaea меняет собственную высоту и высоту контейнера Li
        textarea.style.height = textarea.scrollHeight + "px";
        liTag.style.minHeight = textarea.scrollHeight + "px";
      });
      textarea.addEventListener("blur", function () {
        // !Функция которая при расфокусе с объекта либо удаляет задачу, либо обновляет ее значение, хз зачем удаляет, надо поменять на инпут вместо блюра
        let taskDescription = textarea.value;
        var taskId = liTag.getAttribute("data-task-id");
        if (taskId) {
          if (taskDescription.trim() === "") {
            liTag.remove();
            deleteTaskFromServer(taskId);
          } else {
            updateTaskOnServer(taskId, taskDescription);
          }
        } else {
          console.error("taskId is undefined");
        }
      });
      checkbox.addEventListener("input", function () {
        var taskId = liTag.getAttribute("data-task-id");
        let taskDescription = textarea.value;
        let checked = checkbox.checked;
        updateTaskOnServer(taskId, taskDescription, checked);
      });

      liTag.addEventListener("drop", function (event) {
        event.preventDefault();
        const data = event.dataTransfer.getData("text/plain");
        const draggedElement = document.getElementById(data);
        this.appendChild(draggedElement);
      });
      liTag.setAttribute("draggable", "true");
    });

    listbtn.appendChild(button);
    let link2 = document.createElement("a");
    link2.href = "#";
    link2.id = section.id;
    let ticketIcon = document.createElement("i");
    ticketIcon.className = "fa-solid fa-ticket note-iconbtn";
    ticketIcon.id = section.id;
    link2.appendChild(ticketIcon);

    textarea.addEventListener("keydown", function (event) {
      // !Функция, которая при нажатии ентер убирает фокус с textarea
      if (event.key == "Enter") {
        textarea.blur();
      }
    });

    listbtn.appendChild(link2);
    homeContainer.appendChild(listbtn);
    let addSectionButtons = document.querySelector(".add_section");
    let parent = document.querySelector(".home");
    parent.insertBefore(homeContainer, addSectionButtons);
    textarea.addEventListener("blur", function () {
      // !Функция которая при потере фокуса либо удаляет секцию, либо обновляет ее название, хз зачем удаляет опять-же
      let sectionName = textarea.value;
      if (section.id) {
        if (sectionName.trim() === "") {
          homeContainer.remove();
        } else {
          let sectionName = textarea.value;
          let sectionId = section.id;
          handleBlur(sectionName, sectionId);
        }
      }
    });
    await loadTasks(section.id);
  }
}

async function loadTasks(sectionId) {
  // !Функция которая подгружает задачи при обновлении страницы(Вызывается внутри функции загрузки секций)
  const response = await fetch(`/get_tasks?sectionId=${sectionId}`);
  const data = await response.json();
  for (const task of data.tasks) {
    let liTag = document.createElement("div");
    liTag.classList.add("list");
    liTag.classList.add("board-item");
    liTag.setAttribute("data-task-id", task.id);
    liTag.draggable = "true";

    let checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.id = `checkbox-task-${task.id}`;

    checkbox.addEventListener("input", function () {
      let checked = checkbox.checked;
      let task_description = textarea.value;
      updateTaskOnServer(task.id, task_description, checked);
    });
    let inputTask = document.createElement("div");
    inputTask.classList.add("input-task");
    inputTask.classList.add("board-item-content");
    let textarea = document.createElement("textarea");
    textarea.id = `textarea-task-${task.id}`;
    textarea.classList.add("written-task");
    textarea.value = task.task_description;
    let trashIcon = document.createElement("i");
    trashIcon.classList.add("fa-solid", "fa-trash");
    trashIcon.onclick = function (event) {
      deleteTask(task.id);
    };
    liTag.appendChild(checkbox);
    liTag.appendChild(inputTask);
    inputTask.appendChild(textarea);
    liTag.appendChild(trashIcon);
    document.body.appendChild(liTag);
    let todoList = document.querySelector(`div[id="${sectionId}"]`);
    todoList.appendChild(liTag);
    liTag.appendChild(trashIcon);
    textarea.addEventListener("input", function () {
      textarea.style.height = textarea.scrollHeight + "px";
      liTag.style.minHeight = textarea.scrollHeight + "px";
    });
    if (task.checked === true) {
      checkbox.checked = true;
    } else {
      checkbox.checked = false;
    }
    textarea.addEventListener("blur", function () {
      let taskDescription = textarea.value;
      var taskId = liTag.getAttribute("data-task-id");
      var checked = checkbox.checked;
      if (taskId) {
        if (taskDescription.trim() === "") {
          liTag.remove();
          deleteTaskFromServer(task.id);
        } else {
          updateTaskOnServer(task.id, taskDescription, checked);
        }
      } else {
        console.error("taskId is undefined");
      }
    });
    var scrollHeight = textarea.scrollHeight;
    textarea.style.height = scrollHeight + "px";
    liTag.style.minHeight = scrollHeight + "px";
  }
}

addSectionButtons.addEventListener("click", function () {
  // !Функция добавления новой секции(Все внутренние функции аналогичны тем, что были выше)
  let sectionId = Math.floor(Math.random() * 10000);
  let homeContainer = document.createElement("div");
  homeContainer.className = "home_container";
  homeContainer.draggable = "true";

  homeContainer.setAttribute("data-section-id", sectionId);
  let inputField = document.createElement("div");
  inputField.className = "board-column-header input-field"; //!

  let textarea = document.createElement("textarea");
  textarea.name = "section-name";
  textarea.id = sectionId;
  textarea.placeholder = "Print your title here";
  inputField.appendChild(textarea);

  let link = document.createElement("a");
  link.href = "#";

  let icon = document.createElement("i");
  icon.className = "fa-solid fa-ellipsis note-icon";
  link.appendChild(icon);
  inputField.appendChild(link);
  homeContainer.appendChild(inputField);

  let todoList = document.createElement("div");
  todoList.className = "todoList";
  homeContainer.appendChild(todoList);

  let listbtn = document.createElement("div");
  listbtn.className = "listbtn";

  let plusIcon = document.createElement("i");
  plusIcon.className = "fa-solid fa-plus addTask";
  listbtn.appendChild(plusIcon);

  let button = document.createElement("button");
  button.className = "add-task";
  button.textContent = "Add Task";

  let sectionName = Math.random().toString(36);
  saveSectionToServer(sectionName, homeContainer);

  button.addEventListener("click", () => {
    let liTag = document.createElement("div");
    liTag.classList.add("list"); //!
    liTag.classList.add("board-item-content");
    let checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    let taskId = Math.random().toString(36);
    checkbox.id = `checkbox-task-${taskId}`;
    let inputTask = document.createElement("div");
    inputTask.classList.add("input-task");

    let textarea = document.createElement("textarea");
    textarea.classList.add("written-task");
    textarea.id = `textarea-task-${taskId}`;
    textarea.placeholder = "Write Your Task";
    textarea.onkeydown = function (event) {
      return event.key !== "Enter";
    };

    let trashIcon = document.createElement("i");
    trashIcon.classList.add("fa-solid", "fa-trash");
    trashIcon.onclick = function (event) {
      taskId = liTag.getAttribute("data-task-id");
      deleteTask(taskId);
    };

    liTag.setAttribute("data-section-id", button.id);
    liTag.setAttribute("data-task-id", taskId);

    inputTask.appendChild(textarea);
    liTag.appendChild(checkbox);
    liTag.appendChild(inputTask);
    liTag.appendChild(trashIcon);

    let taskDescription = textarea.value;
    saveTaskToServer(taskDescription, liTag);
    todoList.appendChild(liTag);

    liTag.addEventListener("click", function () {
      let taskId = liTag.getAttribute("data-task-id");
    });

    textarea.addEventListener("focus", function () {
      var liTag = this.closest("div");
      taskId = liTag.getAttribute("data-task-id");
    });

    textarea.focus();
    textarea.addEventListener("input", function () {
      textarea.style.height = textarea.scrollHeight + "px";
      liTag.style.minHeight = textarea.scrollHeight + "px";
    });

    textarea.addEventListener("blur", function () {
      let taskDescription = textarea.value;
      var taskId = liTag.getAttribute("data-task-id");
      if (taskId) {
        if (taskDescription.trim() === "") {
          liTag.remove();
          deleteTaskFromServer(taskId);
        } else {
          updateTaskOnServer(taskId, taskDescription);
        }
      } else {
        console.error("taskId is undefined");
      }
    });
    checkbox.addEventListener("input", function () {
      var taskId = liTag.getAttribute("data-task-id");
      let checked = checkbox.checked;
      let taskDescription = textarea.value;
      updateTaskOnServer(taskId, taskDescription, checked);
    });
  });

  listbtn.appendChild(button);
  let link2 = document.createElement("a");
  link2.href = "#";

  let ticketIcon = document.createElement("i");
  ticketIcon.className = "fa-solid fa-ticket note-iconbtn";
  link2.appendChild(ticketIcon);

  textarea.addEventListener("keydown", function (event) {
    if (event.key == "Enter") {
      textarea.blur();
    }
  });

  listbtn.appendChild(link2);
  homeContainer.appendChild(listbtn);
  let addSectionButtons = document.querySelector(".add_section");
  let parent = document.querySelector(".home");
  parent.insertBefore(homeContainer, addSectionButtons);

  textarea.focus();
  textarea.addEventListener("blur", function () {
    let taskDescription = textarea.value;
    if (taskDescription.trim() === "") {
      homeContainer.remove();
    } else {
      let sectionName = textarea.value;
      let sectionId = homeContainer.getAttribute("data-section-id");
      handleBlur(sectionName, sectionId);
    }
  });
});

function saveSectionToServer(sectionName, homeContainer) {
  // !Функция сохранения секции в базу
  let sectionId = homeContainer.getAttribute("data-section-id");
  fetch("/add_section", {
    method: "POST",
    body: new URLSearchParams({
      section_name: sectionName,
      section_id: sectionId,
    }),
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.status === "success") {
        homeContainer.setAttribute("data-section-id", data.section_id);
        let button = homeContainer.querySelector(".add-task");
        if (button) {
          button.setAttribute("id", data.section_id);
        }
      } else {
        console.error("Ошибка при добавлении секции:", data.message);
      }
    })
    .catch((error) => {
      console.error("Ошибка при добавлении секции:", error);
    });
}

function handleBlur(sectionName, sectionId) {
  // !Функция для обновления названия темы в базу, хз почему аякс запрос, чатжпт такую дал, еблан
  $.ajax({
    type: "POST",
    url: "/save_name_of_section",
    data: { text: sectionName, section_id: sectionId },
    success: function () {},
    error: function (error) {
      console.error("Ошибка при сохранении изменений:", error);
    },
  });
}
