const fs = require('fs');
const csv = require('csv-parser');

// Read the CSV file
fs.createReadStream('advertising_budget_and_sales.csv')
  .pipe(csv())
  .on('data', (row) => {
    // Add the sales value to the total
    totalSales += parseFloat(row['Sales ($)']);
  })
  .on('end', () => {
    console.log(`Total Sales: $${totalSales.toFixed(2)}`);
  });

let totalSales = 0;
