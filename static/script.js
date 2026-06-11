async function load() {
    let res = await fetch('/api/products');
    let products = await res.json();

    let html = '';

    if (products.length === 0) {
        html = '<p>No products added</p>';
    } else {
        html = '<table border="1"><tr><th>Name</th><th>Qty</th><th>Price</th><th>Total</th></tr>';

        let grand = 0;

        for (let p of products) {
            grand += p.total;

            html += `<tr>
                <td>${p.name}</td>
                <td>${p.qty}</td>
                <td>₹${p.price}</td>
                <td>₹${p.total}</td>
            </tr>`;
        }

        html += `</table><p><b>Grand Total: ₹${grand}</b></p>`;
    }

    document.getElementById('report').innerHTML = html;
}


// Add new product
async function add() {
    let name = document.getElementById('name').value.trim();
    let qty = parseInt(document.getElementById('qty').value);
    let price = parseFloat(document.getElementById('price').value);

    // Simple validation
    if (!name || isNaN(qty) || isNaN(price) || qty <= 0 || price <= 0) {
        alert("Enter valid data");
        return;
    }

    await fetch('/api/products', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, qty, price, type: "physical" })
    });

    // Clear input fields
    document.getElementById('name').value = '';
    document.getElementById('qty').value = '';
    document.getElementById('price').value = '';

    load(); // reload data
}


// Reset all products
async function resetAll() {
    if (confirm("Delete all products?")) {
        await fetch('/api/reset', { method: 'POST' });
        load();
    }
}


// Button connections
document.getElementById('addBtn').onclick = add;
document.getElementById('resetBtn').onclick = resetAll;

// Load data when page opens
load();