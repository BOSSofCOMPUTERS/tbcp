const sign_in_btn = document.querySelector("#sign-in-brn");
const sign_up_btn = document.querySelector("#sign-up-brn");
const containerr = document.querySelector("#sign-in-brn");

sign_up_btn.addEventListener("click", () => {
    containerr.classList.add("sign-up-mode");
});

sign_in_btn.addEventListener("click", () => {
    containerr.classList.add("sign-in-mode");
});
