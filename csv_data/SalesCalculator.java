import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class SalesCalculator {
    public static void main(String[] args) {
        String csvFile = "advertising_budget_and_sales.csv";
        double totalSales = 0.0;

        try (BufferedReader br = new BufferedReader(new FileReader(csvFile))) {
            // Skip the header row
            br.readLine();

            String line;
            while ((line = br.readLine()) != null) {
                String[] values = line.split(",");
                double sales = Double.parseDouble(values[3].trim());
                totalSales += sales;
            }

            System.out.println("Total Sales: $" + totalSales);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}