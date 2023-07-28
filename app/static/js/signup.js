document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector(".needs-validation");
  const firstNameInput = document.getElementById("inputFirstName");
  const lastNameInput = document.getElementById("inputLastName");
  const usernameInput = document.getElementById("inputUsername");
  const emailInput = document.getElementById("inputEmail");
  const passwordInput = document.getElementById("inputPassword");

  const firstNameInputPlaceholder = firstNameInput.getAttribute("placeholder");
  const lastNameInputPlaceholder = lastNameInput.getAttribute("placeholder");
  const usernameInputPlaceholder = usernameInput.getAttribute("placeholder");
  const emailInputPlaceholder = emailInput.getAttribute("placeholder");
  const passwordInputPlaceholder = passwordInput.getAttribute("placeholder");

  firstNameInput.addEventListener("input", function () {
    if (firstNameInput.classList.contains("is-invalid")) {
      firstNameInput.classList.remove("is-invalid");
      firstNameInput.nextElementSibling.style.display = "none";
    } else {
      firstNameInput.setAttribute("placeholder", firstNameInputPlaceholder);
      firstNameInput.nextElementSibling.style.display = "none";
    }
  });

  lastNameInput.addEventListener("input", function () {
    if (lastNameInput.classList.contains("is-invalid")) {
      lastNameInput.classList.remove("is-invalid");
      lastNameInput.nextElementSibling.style.display = "none";
    } else {
      lastNameInput.setAttribute("placeholder", lastNameInputPlaceholder);
      lastNameInput.nextElementSibling.style.display = "none";
    }
  });

  usernameInput.addEventListener("input", function () {
    if (usernameInput.classList.contains("is-invalid")) {
      usernameInput.classList.remove("is-invalid");
      usernameInput.nextElementSibling.style.display = "none";
    } else {
      usernameInput.setAttribute("placeholder", usernameInputPlaceholder);
      usernameInput.nextElementSibling.style.display = "none";
    }
  });

  emailInput.addEventListener("input", function () {
    if (emailInput.classList.contains("is-invalid")) {
      emailInput.classList.remove("is-invalid");
      emailInput.nextElementSibling.style.display = "none";
    } else {
      emailInput.setAttribute("placeholder", emailInputPlaceholder);
      emailInput.nextElementSibling.style.display = "none";
    }
  });

  passwordInput.addEventListener("input", function () {
    if (passwordInput.classList.contains("is-invalid")) {
      passwordInput.classList.remove("is-invalid");
      passwordInput.nextElementSibling.style.display = "none";
    } else {
      passwordInput.setAttribute("placeholder", passwordInputPlaceholder);
      passwordInput.nextElementSibling.style.display = "none";
    }
  });

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    event.stopPropagation();

    if (!form.checkValidity()) {
      if (!firstNameInput.checkValidity()) {
        firstNameInput.classList.add("is-invalid");
        firstNameInput.nextElementSibling.textContent = "Please enter your first name";
        firstNameInput.nextElementSibling.style.display = "block";
        firstNameInput.setAttribute("placeholder", "");
      } else {
        firstNameInput.classList.add("is-valid");
        firstNameInput.nextElementSibling.style.display = "none";
      }

      if (!lastNameInput.checkValidity()) {
        lastNameInput.classList.add("is-invalid");
        lastNameInput.nextElementSibling.textContent = "Please enter your last name";
        lastNameInput.nextElementSibling.style.display = "block";
        lastNameInput.setAttribute("placeholder", "");
      } else {
        lastNameInput.classList.add("is-valid");
        lastNameInput.nextElementSibling.style.display = "none";
      }

      if (!usernameInput.checkValidity()) {
        usernameInput.classList.add("is-invalid");
        usernameInput.nextElementSibling.textContent = "Please enter your username";
        usernameInput.nextElementSibling.style.display = "block";
        usernameInput.value = "";
        usernameInput.removeAttribute("placeholder");
      } else {
        usernameInput.classList.add("is-valid");
        usernameInput.nextElementSibling.style.display = "none";
      }

      if (!emailInput.checkValidity()) {
        emailInput.classList.add("is-invalid");
        emailInput.nextElementSibling.textContent = "Please enter a valid email address";
        emailInput.nextElementSibling.style.display = "block";
        emailInput.value = "";
        emailInput.removeAttribute("placeholder");
      } else {
        emailInput.classList.add("is-valid");
        emailInput.nextElementSibling.style.display = "none";
      }

      if (!passwordInput.checkValidity()) {
        passwordInput.classList.add("is-invalid");
        passwordInput.nextElementSibling.textContent = "Please enter a password";
        passwordInput.nextElementSibling.style.display = "block";
        passwordInput.value = "";
        passwordInput.removeAttribute("placeholder");
      } else {
        passwordInput.classList.add("is-valid");
        passwordInput.nextElementSibling.style.display = "none";
      }
    } else {
      firstNameInput.setAttribute("placeholder", firstNameInputPlaceholder);
      lastNameInput.setAttribute("placeholder", lastNameInputPlaceholder);
      usernameInput.setAttribute("placeholder", usernameInputPlaceholder);
      emailInput.setAttribute("placeholder", emailInputPlaceholder);
      passwordInput.setAttribute("placeholder", passwordInputPlaceholder);
    }

    form.classList.add("was-validated");
  });

  // Shtoni këtë event për të ndryshuar ngjyrën e tikut në input change
  const inputs = [firstNameInput, lastNameInput, usernameInput, emailInput, passwordInput];
  inputs.forEach(function (input) {
    input.addEventListener("change", function () {
      if (input.checkValidity()) {
        input.classList.add("is-valid");
        input.nextElementSibling.style.display = "none";
      } else {
        input.classList.remove("is-valid");
        input.nextElementSibling.style.display = "none";
      }
    });
  });
});