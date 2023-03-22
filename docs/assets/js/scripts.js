(function() {
    var elements;
    var windowHeight;
  
    function init() {
      elements = document.querySelectorAll('.fadeInUp');
      windowHeight = window.innerHeight;
      addEventHandlers();
      checkElements();
    }
  
    function addEventHandlers() {
      window.addEventListener('scroll', checkElements);
      window.addEventListener('resize', init);
    }
  
    function checkElements() {
      for (var i = 0; i < elements.length; i++) {
        var element = elements[i];
        var position = element.getBoundingClientRect().top;
        if (position - windowHeight <= 0) {
          element.classList.add('is-visible');
        }
      }
    }
  
    init();
  })();
  

// get the default image element
const defaultImage = document.getElementById("default-image");

// function to select an item
function selectItem(item) {
  // get all the list items
  const listItems = document.querySelectorAll(".list-item");

  // deselect all items except the clicked item
  listItems.forEach((listItem) => {
    if (listItem !== item) {
      listItem.classList.remove("selected");
    }
  });

  // select the clicked item
  item.classList.toggle("selected");

  // get the selected item's image
  const selectedImage = item.querySelector("img");

  // update the default image with the selected image
  if (item.classList.contains("selected")) {
    defaultImage.src = selectedImage.src;
  }
  // update the default image with the default image
  else {
    defaultImage.src = "/img/List1.png";
  }
}

const imageBox = document.querySelector('.image-box');

imageBox.addEventListener('mouseover', () => {
  imageBox.classList.add('show-caption');
});

imageBox.addEventListener('mouseout', () => {
  imageBox.classList.remove('show-caption');
});
