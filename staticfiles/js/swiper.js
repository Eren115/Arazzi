var swiper = new Swiper(".mySwiper", {
  
  cssMode: true,
  // slidesPerView: 1,
  // lazy: true,
  // spaceBetween: 30,
  // effect: "fade",
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
  
  loop: true,
  // mousewheel: true,
  // keyboard: true,
});

let cursor = document.querySelector('.cursor')
let prev = document.querySelector('.swiper-button-prev')
let next = document.querySelector('.swiper-button-next')
document.addEventListener("mousemove", moveCursor)

let svg = document.querySelector('.spe__svg')
let speDiv = document.querySelector('.spe__div25')
let speDiv2 = document.querySelector('.spe__div26')
let navDiv = document.querySelector('.nav__div10')

function openHam() {
  speDiv.style.width = "33.5vw"
  speDiv.style.transition = "0.5s ease-in-out"
  speDiv.style.opacity = 1
  // console.log("click")
}

function closeHam() {
  speDiv.style.width = "0vw"
  speDiv.style.transition = "0.5s ease-in-out"
  speDiv.style.opacity = 0
  document.body.style.overflow = "scroll" 
}

function openHams() {
  speDiv.style.width = "100%"
  speDiv.style.height = "100%"
  document.body.style.overflow = "hidden" 
  speDiv.style.transition = "0.5s ease-in-out"
  speDiv.style.opacity = 1
}

function openHamburger() {
  navDiv.addEventListener("click", window.screen.width <= 430 ? openHams : openHam)
  // document.getElementById('nav__div10').click = function () {
  //   alert('yoo')
  //   console.log('yyy')
  // }
  
}

function closeHamburger() {
  svg.addEventListener("click", closeHam)
}

openHamburger()
closeHamburger()



function moveCursor(e) {
  let x = e.clientX;
  let y = e.clientY;
  // console.log(x, y)
  cursor.style.left = `${x}px`;
  cursor.style.top = `${y}px`;
}

function changeFont() {
  cursor.innerHTML = "Prev"
}
function nothingH() {
  cursor.innerHTML = ""
}

function changeFonts() {
  cursor.innerHTML = "Next"
}
function nothingHs() {
  cursor.innerHTML = ""
}


function prevs() {
  prev.addEventListener("mouseover", changeFont)
  
  prev.addEventListener("mouseout", nothingH)
}

prevs()


function nexts() {
  next.addEventListener("mouseover", changeFonts)
  
  next.addEventListener("mouseout", nothingHs)
}

nexts()





