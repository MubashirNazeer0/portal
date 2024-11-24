$('#button-right').click(function() {
  $('.slider').children().addClass('left').removeClass('right').first().appendTo('.slider');
});

$('#button-left').click(function() {
  $('.slider').children().addClass('right').removeClass('left').last().prependTo('.slider');
});

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
