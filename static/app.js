document.addEventListener('DOMContentLoaded', function () {
    const brothSelect = document.getElementById('broth');
    const proteinSelect = document.getElementById('protein');
    const confirmationDiv = document.getElementById('confirmation');
    
    fetch('/broths', {
        headers: {
            'x-api-key': 'ZtVdh8XQ2U8pWI2gmZ7f796Vh8GllXoN7mr0djNf'
        }
    })
    .then(response => response.json())
    .then(data => {
        data.forEach(broth => {
            const option = document.createElement('option');
            option.value = broth.id;
            option.textContent = broth.name;
            brothSelect.appendChild(option);
        });
    });

    fetch('/proteins', {
        headers: {
            'x-api-key': 'ZtVdh8XQ2U8pWI2gmZ7f796Vh8GllXoN7mr0djNf'
        }
    })
    .then(response => response.json())
    .then(data => {
        data.forEach(protein => {
            const option = document.createElement('option');
            option.value = protein.id;
            option.textContent = protein.name;
            proteinSelect.appendChild(option);
        });
    });

    document.getElementById('order-form').addEventListener('submit', function (event) {
        event.preventDefault();

        const order = {
            brothId: brothSelect.value,
            proteinId: proteinSelect.value
        };

        fetch('/order', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'x-api-key': 'ZtVdh8XQ2U8pWI2gmZ7f796Vh8GllXoN7mr0djNf'
            },
            body: JSON.stringify(order)
        })
        .then(response => response.json())
        .then(data => {
            confirmationDiv.textContent = `Order placed! Your order ID is ${data.id}`;
        })
        .catch(error => {
            confirmationDiv.textContent = 'Error placing order.';
        });
    });
});
