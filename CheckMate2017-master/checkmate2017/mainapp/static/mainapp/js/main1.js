function getRandom(min, max){
  return Math.random() * (max - min) + min;
}

var isSafari = /constructor/i.test(window.HTMLElement);
var isFF = !!navigator.userAgent.match(/firefox/i);

if (isSafari) {
  document.getElementsByTagName('html')[0].classList.add('safari');
}

// Remove click on button for demo purpose
Array.prototype.slice.call(document.querySelectorAll('.button'), 0).forEach(function(bt) {
  bt.addEventListener('click', function(e) {
    e.preventDefault();
  });
});

initBt5();




// Button 5
function initBt5() {
  var bt = document.querySelectorAll('#component-5')[0];
  var turbVal = { val: 0.000001 };
  var turb = document.querySelectorAll('#filter-glitch-1 feTurbulence')[0];
  var btTl = new TimelineLite({
    paused: true,
    onStart: function() {
      bt.style.filter = 'url(#filter-glitch-1)';
    },
    onUpdate: function() {
      turb.setAttribute('baseFrequency', turbVal.val);
    },
    onComplete: function() {
      bt.style.filter = 'none';
    } });

  btTl.to(turbVal, 0.2, { val: 0.04 });
  btTl.to(turbVal, 0.2, { val: 0.000001 });

  bt.addEventListener('click', function() {
    btTl.restart();
  });
}
