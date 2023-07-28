var login = document.querySelector(".typewritter");
var signup = document.querySelector(".typewriter");

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

var typewriter = new Typewriter(signup, {
  loop: true
})

typewriter.typeString("SIGN UP")
  .pause(2000)
  .deleteAll()
  .typeString("SIGN UP")
  .deleteAll()
  .pause()
  .start()