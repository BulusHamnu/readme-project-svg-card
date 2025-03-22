//codes
let count = 2;
if(window.matchMedia("(min-width: 767px)").matches) {
  count = 4;
}

document.addEventListener('DOMContentLoaded', function() {
  // Update copyright year
  document.getElementById('current-year').textContent = new Date().getFullYear();

  //quering and displaying svg images images examples
  const previewContent = document.querySelector(".preview-content")
  fetch("/api/bulushamnu/repos?pinned=True&theme=dark")
    .then( response => response.json() )
    .then( svg => { 
      for(i=0; i<count ; i++) {
        svgCard = document.createElement("div"); 
        svgCard.innerHTML = svg.data[i]; 
        previewContent.appendChild(svgCard); 
      }
    })
  
  
  // Intersection Observer for scroll animations
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };
  
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);
  
  // Observe all section elements for entrance animations
  document.querySelectorAll('section').forEach(section => {
    section.classList.add('animate-on-scroll');
    observer.observe(section);
  });
  
  
  // Add some CSS for the animation classes
  const style = document.createElement('style');
  style.textContent = `
    .animate-on-scroll {
      opacity: 0;
      transform: translateY(20px);
      transition: opacity 0.6s ease-out, transform 0.6s ease-out;
    }
    
    .animate-on-scroll.visible {
      opacity: 1;
      transform: translateY(0);
    }
    
    .feature-card.animate-on-scroll,
    .example-card.animate-on-scroll {
      transition-delay: calc(var(--animation-order, 0) * 0.1s);
    }
  `;
  document.head.appendChild(style);
  
});
