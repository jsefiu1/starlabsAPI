document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector(".needs-validation");
  const emailInput = document.getElementById("inputEmail");
  const passwordInput = document.getElementById("inputPassword");

  const emailInputPlaceholder = emailInput.getAttribute("placeholder");
  const passwordInputPlaceholder = passwordInput.getAttribute("placeholder");

  emailInput.addEventListener("input", function () {
    if (emailInput.classList.contains("is-invalid")) {
      emailInput.classList.remove("is-invalid");
      emailInput.nextElementSibling.style.display = "none";
      emailInput.value = "";
    } else {
      emailInput.setAttribute("placeholder", emailInputPlaceholder);
      emailInput.nextElementSibling.style.display = "none";
    }
  });

  passwordInput.addEventListener("input", function () {
    if (passwordInput.classList.contains("is-invalid")) {
      passwordInput.classList.remove("is-invalid");
      passwordInput.nextElementSibling.style.display = "none";
      passwordInput.value = "";
    } else {
      passwordInput.setAttribute("placeholder", passwordInputPlaceholder);
      passwordInput.nextElementSibling.style.display = "none";
    }
  });

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    event.stopPropagation();

    if (!form.checkValidity()) {
      if (!emailInput.checkValidity()) {
        emailInput.classList.add("is-invalid");
        emailInput.nextElementSibling.textContent = "Please enter your email";
        emailInput.nextElementSibling.style.display = "block";
        emailInput.value = "";
        emailInput.removeAttribute("placeholder");
      } else {
        emailInput.classList.add("is-valid");
        emailInput.nextElementSibling.style.display = "none";
      }

      if (!passwordInput.checkValidity()) {
        passwordInput.classList.add("is-invalid");
        passwordInput.nextElementSibling.textContent = "Please enter your password";
        passwordInput.nextElementSibling.style.display = "block";
        passwordInput.value = "";
        passwordInput.removeAttribute("placeholder");
      } else {
        passwordInput.classList.add("is-valid");
        passwordInput.nextElementSibling.style.display = "none";
      }
    } else {
      emailInput.setAttribute("placeholder", emailInputPlaceholder);
      passwordInput.setAttribute("placeholder", passwordInputPlaceholder);
    }

    form.classList.add("was-validated");
  });

  // Shfaqja e tikut të gjelbër dhe pikës së kuqe në ndryshimin e input-it
  emailInput.addEventListener("change", function () {
    if (emailInput.checkValidity()) {
      emailInput.classList.add("is-valid");
      emailInput.nextElementSibling.style.display = "none";
    } else {
      emailInput.classList.remove("is-valid");
      emailInput.nextElementSibling.style.display = "none";
    }
  });

  passwordInput.addEventListener("change", function () {
    if (passwordInput.checkValidity()) {
      passwordInput.classList.add("is-valid");
      passwordInput.nextElementSibling.style.display = "none";
    } else {
      passwordInput.classList.remove("is-valid");
      passwordInput.nextElementSibling.style.display = "none";
    }
  });
});