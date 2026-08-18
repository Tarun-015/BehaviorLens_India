INSERT INTO industries (industry_name, description)
VALUES
(
    'Food Delivery',
    'Online food ordering and delivery platforms'
),
(
    'Quick Commerce',
    'Fast delivery platforms for groceries and everyday products'
),
(
    'E-Commerce',
    'Online marketplaces and digital commerce platforms'
),
(
    'Digital Payments / FinTech',
    'Digital payment, financial technology and credit platforms'
),
(
    'EdTech',
    'Online education, learning and exam preparation platforms'
),
(
    'Ride-Hailing / Mobility',
    'App-based transportation and ride-hailing services'
),
(
    'Travel / Transport Booking',
    'Online travel, flight, hotel and bus booking platforms'
)
ON CONFLICT (industry_name) DO NOTHING;