// static/js/caisse.js

document.addEventListener('DOMContentLoaded', function() {
  const searchInput = document.getElementById('product-search');
  const searchBtn = document.getElementById('search-btn');
  const productList = document.getElementById('product-list');
  const cartList = document.getElementById('cart-items');
  const cartCount = document.getElementById('cart-count');
  const subtotalEl = document.getElementById('cart-subtotal');
  const taxEl = document.getElementById('cart-tax');
  const totalEl = document.getElementById('cart-total');
  const paymentModeBtns = document.querySelectorAll('[name="payment_mode"]');
  const cashFields = document.getElementById('cash-fields');
  const cashReceivedInput = document.getElementById('cash-received');
  const finalizeBtn = document.getElementById('finalize-sale');
  const emptyCartBtn = document.getElementById('empty-cart');

  let cart = [];

  // Recherche de produits (placeholder AJAX)
  searchBtn.addEventListener('click', function(e) {
    e.preventDefault();
    const term = searchInput.value.trim().toLowerCase();
    // TODO: Remplacer par appel AJAX vers votre API produits
    productList.innerHTML = '<li class="list-group-item text-center text-muted">Recherche non implémentée</li>';
  });

  // Ajouter un produit au panier
  productList.addEventListener('click', function(e) {
    const btn = e.target.closest('.add-to-cart');  // Ligne 9 : écoute des clicks sur .add-to-cart
    if (!btn) return;
    const sku = btn.dataset.sku;
    const name = btn.dataset.name;
    const price = parseFloat(btn.dataset.price);
    const existing = cart.find(item => item.sku === sku);
    if (existing) {
      existing.qty++;
    } else {
      cart.push({ sku, name, price, qty: 1 });
    }
    renderCart();
  });

  // Vider le panier
  emptyCartBtn.addEventListener('click', function() {
    if (confirm('Vider entièrement le panier ?')) {
      cart = [];
      renderCart();
    }
  });

  // Changement de mode de paiement
  paymentModeBtns.forEach(rb => {
    rb.addEventListener('change', function() {
      if (this.value === 'CASH') {
        cashFields.style.display = '';
      } else {
        cashFields.style.display = 'none';
        cashReceivedInput.value = '';
      }
    });
  });

  // Finaliser la vente
  finalizeBtn.addEventListener('click', function() {
    if (cart.length === 0) {
      alert('Le panier est vide.');
      return;
    }
    const mode = document.querySelector('[name="payment_mode"]:checked').value;
    let cashReceived = 0;
    if (mode === 'CASH') {
      cashReceived = parseFloat(cashReceivedInput.value) || 0;
      if (cashReceived < calculateTotal()) {
        alert('Montant en espèces insuffisant.');
        return;
      }
    }
    const data = { items: cart, payment_mode: mode, cash_received: cashReceived };
    fetch('/core/caisse/checkout/', {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCookie('csrftoken'),
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
    .then(resp => resp.json())
    .then(json => {
      if (json.success) {
        window.location.href = json.redirect_url;
      } else {
        alert(json.error || 'Erreur lors de la finalisation.');
      }
    });
  });

  // Rendu du panier
  function renderCart() {
    cartList.innerHTML = '';
    if (cart.length === 0) {
      cartList.innerHTML = '<li class="list-group-item text-center text-muted">Le panier est vide<br>Ajoutez des produits pour commencer</li>';
    } else {
      cart.forEach(item => {
        const li = document.createElement('li');
        li.className = 'list-group-item d-flex justify-content-between align-items-center';
        li.innerHTML = `
          ${item.name} x${item.qty}
          <span>${(item.price * item.qty).toFixed(2)} €</span>
        `;
        cartList.append(li);
      });
    }
    cartCount.textContent = cart.reduce((sum, i) => sum + i.qty, 0);
    const subtotal = cart.reduce((sum, i) => sum + i.price * i.qty, 0);
    const tax = subtotal * 0.2;
    const total = subtotal + tax;
    subtotalEl.textContent = subtotal.toFixed(2) + ' €';
    taxEl.textContent = tax.toFixed(2) + ' €';
    totalEl.textContent = total.toFixed(2) + ' €';
  }

  function calculateTotal() {
    const sub = parseFloat(subtotalEl.textContent) || 0;
    const tax = parseFloat(taxEl.textContent) || 0;
    return sub + tax;
  }

  // Récupérer le cookie CSRF
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      document.cookie.split(';').forEach(c => {
        const [k,v] = c.trim().split('=');
        if (k === name) cookieValue = decodeURIComponent(v);
      });
    }
    return cookieValue;
  }
});
