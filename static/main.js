/* =================================
PORTFOLIO JAVASCRIPT
================================= */


/* =================================
TYPING TEXT ANIMATION
================================= */

const typedTextSpan = document.querySelector(".typed-text");
const cursorSpan = document.querySelector(".cursor");

const textArray = [
"Engineer",
"AI Developer",
"Generative AI Developer",
"Python Developer"
];

const typingDelay = 100;
const erasingDelay = 60;
const newTextDelay = 1500;

let textArrayIndex = 0;
let charIndex = 0;

function type() {

if (charIndex < textArray[textArrayIndex].length) {

typedTextSpan.textContent += textArray[textArrayIndex].charAt(charIndex);

charIndex++;

setTimeout(type, typingDelay);

} else {

setTimeout(erase, newTextDelay);

}

}

function erase() {

if (charIndex > 0) {

typedTextSpan.textContent =
textArray[textArrayIndex].substring(0, charIndex - 1);

charIndex--;

setTimeout(erase, erasingDelay);

} else {

textArrayIndex++;

if (textArrayIndex >= textArray.length) {
textArrayIndex = 0;
}

setTimeout(type, typingDelay + 1000);

}

}

document.addEventListener("DOMContentLoaded", () => {

if (typedTextSpan) {
setTimeout(type, newTextDelay);
}

});



/* =================================
SMOOTH SCROLL NAVBAR
================================= */

document.querySelectorAll("nav a[href^='#']").forEach(anchor => {

anchor.addEventListener("click", function (e) {

e.preventDefault();

const section = document.querySelector(this.getAttribute("href"));

if (section) {

section.scrollIntoView({
behavior: "smooth"
});

}

});

});



/* =================================
ACTIVE NAVBAR LINK
================================= */

const sections = document.querySelectorAll("section");
const navLinks = document.querySelectorAll("nav a");

window.addEventListener("scroll", () => {

let current = "";

sections.forEach(section => {

const sectionTop = section.offsetTop;

if (pageYOffset >= sectionTop - 200) {

current = section.getAttribute("id");

}

});

navLinks.forEach(link => {

link.classList.remove("active");

if (link.getAttribute("href") === "#" + current) {

link.classList.add("active");

}

});

});



/* =================================
CONTACT FORM SUBMIT
================================= */

const form = document.getElementById("contact-form");

if (form) {

form.addEventListener("submit", async function (e) {

e.preventDefault();

const name = document.getElementById("name").value.trim();
const email = document.getElementById("email").value.trim();
const message = document.getElementById("message").value.trim();


/* BASIC VALIDATION */

if (!name || !email || !message) {

alert("Please fill all fields");

return;

}

try {

/* CHANGE THIS URL IF RUNNING LOCALLY */

const response = await fetch("/contact", {

method: "POST",

headers: {
"Content-Type": "application/json"
},

body: JSON.stringify({
name: name,
email: email,
message: message
})

});


const data = await response.json();

if (response.ok) {

alert("Message sent successfully!");

form.reset();

} else {

alert(data.error || "Something went wrong");

}

} catch (error) {

console.error(error);

alert("Server error. Please try again later.");

}

});

}



/* =================================
SCROLL REVEAL ANIMATION
================================= */

const revealElements = document.querySelectorAll(".reveal");

function revealOnScroll() {

const windowHeight = window.innerHeight;

revealElements.forEach(el => {

const elementTop = el.getBoundingClientRect().top;

const visiblePoint = 150;

if (elementTop < windowHeight - visiblePoint) {

el.classList.add("active");

}

});

}

window.addEventListener("scroll", revealOnScroll);

/* trigger once on load */

revealOnScroll();