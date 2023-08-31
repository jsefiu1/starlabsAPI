var login = document.querySelector(".typewritter");
var register = document.querySelector(".typewriter");

var typewriter = new Typewriter(login, {
  loop: true
})

typewriter.typeString("LOG IN")
  .pause(2000)
  .deleteAll()
  .typeString("LOG IN")
  .deleteAll()
  .pause()
  .start()

var typewriter = new Typewriter(register, {
  loop: true
})

typewriter.typeString("Register")
  .pause(2000)
  .deleteAll()
  .typeString("Register")
  .deleteAll()
  .pause()
  .start()
