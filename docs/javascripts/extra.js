// Stride Custom JavaScript

// Add copy button feedback
document.querySelectorAll('.md-clipboard').forEach(button => {
  button.addEventListener('click', () => {
    const original = button.innerHTML;
    button.innerHTML = '✓ Copied!';
    button.style.color = '#4caf50';
    setTimeout(() => {
      button.innerHTML = original;
      button.style.color = '';
    }, 2000);
  });
});

// Add smooth scroll behavior
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });
    }
  });
});

// Add external link icons
document.querySelectorAll('a[href^="http"]').forEach(link => {
  if (!link.hostname.includes('stride') && !link.querySelector('img')) {
    link.classList.add('external-link');
    link.setAttribute('target', '_blank');
    link.setAttribute('rel', 'noopener noreferrer');
  }
});

// Analytics (placeholder - add your tracking code)
console.log('Stride Documentation loaded');
