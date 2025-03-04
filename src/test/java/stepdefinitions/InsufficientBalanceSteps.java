package stepdefinitions;

import io.cucumber.java.en.Given;
import io.cucumber.java.en.When;
import io.cucumber.java.en.Then;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import static org.junit.Assert.assertTrue;
import static org.junit.Assert.assertFalse;

public class InsufficientBalanceSteps {

    private WebDriver driver;
    private double balance;

    @Given("a customer with a debit card and {string} balance")
    public void a_customer_with_a_debit_card_and_balance(String balanceType) {
        // Initialize WebDriver
        driver = new ChromeDriver();
        driver.get("https://www.example.com/login"); // Replace with actual URL

        // Simulate login
        driver.findElement(By.id("username")).sendKeys("testuser");
        driver.findElement(By.id("password")).sendKeys("securepassword");
        driver.findElement(By.id("loginButton")).click();

        // Navigate to account page and get balance
        WebElement balanceElement = driver.findElement(By.id("accountBalance"));
        balance = Double.parseDouble(balanceElement.getText().replace("$", ""));

        if (balanceType.equalsIgnoreCase("insufficient")) {
            assertTrue("Balance is not insufficient!", balance < 100); // Ensure balance is low
        } else if (balanceType.equalsIgnoreCase("sufficient")) {
            assertTrue("Balance is not sufficient!", balance >= 100); // Ensure enough funds
        }
    }

    @When("they attempt an online transaction")
    public void they_attempt_an_online_transaction() {
        driver.get("https://www.example.com/checkout"); // Replace with actual URL

        // Enter transaction details
        driver.findElement(By.id("cardNumber")).sendKeys("4111111111111111"); // Sample valid Visa card
        driver.findElement(By.id("cvv")).sendKeys("123");
        driver.findElement(By.id("expiryDate")).sendKeys("12/26");
        driver.findElement(By.id("payButton")).click();
    }

    @Then("the transaction should be {string}")
    public void the_transaction_should_be(String expectedOutcome) {
        if (expectedOutcome.equalsIgnoreCase("accepted")) {
            WebElement successMessage = driver.findElement(By.id("successMessage"));
            assertTrue("Transaction was not approved", successMessage.isDisplayed());
        } else if (expectedOutcome.equalsIgnoreCase("declined")) {
            WebElement errorMessage = driver.findElement(By.id("errorMessage"));
            assertTrue("Transaction was not declined", errorMessage.isDisplayed());
        }

        // Close the browser
        driver.quit();
    }
}
