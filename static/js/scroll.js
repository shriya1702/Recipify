
// JavaScript to handle scrolling


document.addEventListener("DOMContentLoaded", function() {
  // Get the recipe links
  const recipeLinks = document.querySelectorAll('.recipe-link');

  // Add click event listener to each recipe link
  recipeLinks.forEach(function(link) {
    link.addEventListener('click', function(event) {
      // Prevent the default action of the link
      
      // Get the position of the middle section
      const middleSection = document.getElementById('middle');
      const middleSectionPosition = middleSection.offsetTop;

      // Scroll to the middle section
      window.scrollTo({
        top: middleSectionPosition,
        behavior: 'smooth' // Smooth scrolling effect
      });
    });
  });
});
