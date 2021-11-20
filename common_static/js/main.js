function showLeftMenu() {
    let menu = $("#LeftMenu")[0];
    let content = $("#Content")[0];

    if (menu.style.display==="") {
        content.style.width="20%"
        menu.style.display="none"
        content.style.display=""
        content.style.width="100%"
        content.style.marginLeft=""
    } else {
        if (document.documentElement.clientWidth < 900) {
            content.style.display="none"
            menu.style.width="100%"
        } else {
            content.style.width="80%"
            content.style.marginLeft="1%"
        }
        menu.style.display="";
    }
}

$("#btnMenu").on("click", (e) => {
    e.preventDefault()
    showLeftMenu();
})