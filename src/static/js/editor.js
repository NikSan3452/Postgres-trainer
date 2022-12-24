let executeCodeBtn = document.querySelector(".run-button");

let codeEditor = ace.edit("editor");
let defaultCode = "select * from employees;";

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

function submit_run(value) {
    fetch("/run", {
        method: "POST",
        headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ data: value }),
    })  
        .then((resp) => resp.text()) 
        .then((data) => {
            document.getElementById("responseArea").innerHTML = data;
        })
        .catch((error) => {
            console.error(error);
        });
}


function submit_new_database() {
    fetch("/new-database", {
        method: "POST",
        headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ data: 'create' }),
    })  
        .then((resp) => resp.text())
        .then((data) => {
            document.getElementById("responseArea").innerHTML = data;
        })
        .catch((error) => {
            console.error(error);
        });
}


function submit_delete() {
    fetch("/delete", {
        method: "POST",
        headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ data: 'delete' }),
    })
        .then((resp) => resp.text())
        .then((data) => {
            document.getElementById("responseArea").innerHTML = data;
        })
        .catch((error) => {
            console.error(error);
        });
}
