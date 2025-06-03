// Adding JS function to handle the accordion functionality.
// This is more efficient than styling with html and css alone beause it allows for better interaction and control for the user.

// contentloaded waits for the entire HTML document to be rendered before running the script
document.addEventListener("DOMContentLoaded", () => {
  const accordionButtons = document.querySelectorAll(".accordion-button button");
//   const accordionContent = document.querySelectorAll(".accordion-content"); 

  accordionButtons.forEach((button) => {
    button.addEventListener("click", () => {
        // .closest method will find the closest ancestor element to the button that matches the selector. 
        // Can't use .accordion-content because it is a sibling of the of the accrdion button and .closest method only searches up the DOM. 
      const accordion = button.closest(".accordion");
      if (accordion) {
        accordion.classList.toggle("open"); // CSS will handle the open/close functionality
      }
    });
  });
});


/* ---------------- Work Cited ---------------- */
// https://www.youtube.com/watch?v=Q3ipHIy-YG0&ab_channel=xplodivity
// https://developer.mozilla.org/en-US/docs/Web/API/Document/DOMContentLoaded_event
// https://developer.mozilla.org/en-US/docs/Web/API/Element/closest
// https://developer.mozilla.org/en-US/docs/Web/API/Element/classList