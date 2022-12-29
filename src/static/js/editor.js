// Ace редактор
let executeCodeBtn = document.querySelector(".run-button");

let codeEditor = ace.edit("editor");
let defaultCode = "";

let editorLib = {
    init() {
        codeEditor.setTheme("ace/theme/cobalt");
        codeEditor.session.setMode("ace/mode/sql");
        codeEditor.setOptions({
            fontSize: "12pt",
            enableBasicAutocompletion: true,
            enableLiveAutocompletion: true,
        });
        codeEditor.setValue(defaultCode);
        codeEditor.session.setTabSize(4);
        codeEditor.setHighlightActiveLine(true);
        codeEditor.setShowPrintMargin(true);
    },
};

executeCodeBtn.addEventListener("click", () => {
    const userCode = codeEditor.getValue();
    submit_run(userCode);
    try {
        new Function(userCode)();
    } catch (err) {
        console.error(err);
    }
});

editorLib.init();

// Выполнить sql - запрос
function submit_run(value) {
    fetch("/run", {
        method: "POST",
        headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ query: value }),
    })
        .then((resp) => resp.text())
        .then((data) => {
            document.getElementById("responseArea").innerHTML = data;
        })
        .catch((error) => {
            console.error(error);
        });
}

// Создать новую базу данных
function submit_new_database() {
    fetch("/new-database", {
        method: "POST",
        headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ data: "create" }),
    })
        .then((resp) => resp.text())
        .then((data) => {
            document.getElementById("responseArea").innerHTML = data;
        })
        .catch((error) => {
            console.error(error);
        });
}

// Удалить базу данных
function submit_delete() {
    fetch("/delete", {
        method: "POST",
        headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ data: "delete" }),
    })
        .then((resp) => resp.text())
        .then((data) => {
            document.getElementById("responseArea").innerHTML = data;
        })
        .catch((error) => {
            console.error(error);
        });
}

// Анимация кнопки создания БД
document.querySelector("button").addEventListener("click", function (event) {
    var classes = event.target.classList;
    var text = event.target.textContent;
    if (classes.contains("loading") || classes.contains("success")) {
        return;
    }

    classes.add("loading");

    setTimeout(function () {
        classes.remove("loading");
        classes.add("success");
        event.target.textContent = "Success!";

        setTimeout(function () {
            classes.remove("success");
            event.target.textContent = text;
        }, 2500);
    }, 15000);
});
