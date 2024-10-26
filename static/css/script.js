const meals = [
    {
        name: 'Classic Burger',
        image: 'https://via.placeholder.com/250',
        description: 'Juicy beef patty, fresh lettuce, tomato, cheese and our special sauce.',
        price: '$6.99'
    },
    {
        name: 'Chicken Sandwich',
        image: 'https://via.placeholder.com/250',
        description: 'Crispy chicken breast with lettuce, tomato and mayo on a fresh bun.',
        price: '$5.99'
    },
    {
        name: 'Veggie Wrap',
        image: 'https://via.placeholder.com/250',
        description: 'Fresh vegetables wrapped in a soft tortilla with hummus and spices.',
        price: '$4.99'
    },
    {
        name: 'Cheese Fries',
        image: 'https://via.placeholder.com/250',
        description: 'Crispy fries topped with melted cheese and savory bacon bits.',
        price: '$3.99'
    }
];

// Dynamically load the meals into the section
const mealSection = document.getElementById('mealSection');

meals.forEach(meal => {
    const mealCard = document.createElement('div');
    mealCard.classList.add('meal-card');

    mealCard.innerHTML = `
        <img src="${meal.image}" alt="${meal.name}" class="meal-image">
        <div class="meal-info">
            <h3>${meal.name}</h3>
            <p>${meal.description}</p>
            <p class="price">${meal.price}</p>
            <button>Add to Cart</button>
        </div>
    `;

    mealSection.appendChild(mealCard);
});



const meals1 = {
    beverages: [
        {
            name: 'Coca Cola',
            image: 'https://via.placeholder.com/250',
            description: 'Classic refreshing soda.',
            price: '$1.99'
        },
        {
            name: 'Lemonade',
            image: 'https://via.placeholder.com/250',
            description: 'Freshly squeezed lemonade.',
            price: '$2.49'
        }
    ],
    sweets: [
        {
            name: 'Chocolate Cake',
            image: 'https://via.placeholder.com/250',
            description: 'Rich and moist chocolate cake.',
            price: '$3.99'
        },
        {
            name: 'Ice Cream',
            image: 'https://via.placeholder.com/250',
            description: 'Creamy vanilla ice cream.',
            price: '$2.99'
        }
    ],
    platters: [
        {
            name: 'BBQ Platter',
            image: 'https://via.placeholder.com/250',
            description: 'Grilled chicken, ribs, and sausages.',
            price: '$9.99'
        },
        {
            name: 'Seafood Platter',
            image: 'https://via.placeholder.com/250',
            description: 'Shrimp, fish, and crab served with rice.',
            price: '$12.99'
        }
    ],
    snacks: [
        {
            name: 'French Fries',
            image: 'https://via.placeholder.com/250',
            description: 'Crispy golden fries.',
            price: '$2.49'
        },
        {
            name: 'Nachos',
            image: 'https://via.placeholder.com/250',
            description: 'Tortilla chips with cheese and jalapeños.',
            price: '$3.49'
        }
    ],
    others: [
        {
            name: 'Salad',
            image: 'https://via.placeholder.com/250',
            description: 'Fresh garden salad with dressing.',
            price: '$4.99'
        },
        {
            name: 'Breadsticks',
            image: 'https://via.placeholder.com/250',
            description: 'Soft and warm breadsticks.',
            price: '$3.99'
        }
    ]
};

// Function to dynamically load meals based on category
function filterCategory(category) {
    const mealSection = document.getElementById('mealSection');
    mealSection.innerHTML = ''; // Clear current meals

    meals[category].forEach(meal => {
        const mealCard = document.createElement('div');
        mealCard.classList.add('meal-card');

        mealCard.innerHTML = `
            <img src="${meal.image}" alt="${meal.name}" class="meal-image">
            <div class="meal-info">
                <h3>${meal.name}</h3>
                <p>${meal.description}</p>
                <p class="price">${meal.price}</p>
                <button>Add to Cart</button>
            </div>
        `;

        mealSection.appendChild(mealCard);
    });
}

// Load beverages by default
window.onload = () => filterCategory('beverages');
