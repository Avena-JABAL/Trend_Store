const mainImage = document.getElementById('main-product-image');
const thumbs = document.querySelectorAll('.thumb');
const productSize = document.querySelectorAll('.size-pill');
const swatches = document.querySelectorAll('.swatch');
const quantityValue = document.querySelector('.qty-value');
const qtyButtons = document.querySelectorAll('.qty-btn');

thumbs.forEach((thumb) => {
  thumb.addEventListener('click', () => {
    thumbs.forEach((item) => item.classList.remove('active'));
    thumb.classList.add('active');
    mainImage.src = thumb.dataset.image;
  });
});

productSize.forEach((size) => {
  size.addEventListener('click', () => {
    productSize.forEach((item) => item.classList.remove('active'));
    size.classList.add('active');
  });
});

swatches.forEach((swatch) => {
  swatch.addEventListener('click', () => {
    swatches.forEach((item) => item.classList.remove('active'));
    swatch.classList.add('active');
  });
});

let quantity = 1;
qtyButtons.forEach((button) => {
  button.addEventListener('click', () => {
    const action = button.dataset.action;
    quantity = action === 'increase' ? quantity + 1 : Math.max(1, quantity - 1);
    quantityValue.textContent = String(quantity);
  });
});
