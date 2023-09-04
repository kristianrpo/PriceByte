function hide(){
    const button = document.getElementById("all")
    const title = document.getElementById("title")
    const title_all = document.getElementById("title_all")
    const products_top = document.getElementById("products_top")
    const products_all = document.getElementById("products_all")
    button.style.display = "none";
    title.style.display = "none";
    title_all.style.display = "block";
    products_top.style.display = "none";
    products_all.style.display = "flex";
}