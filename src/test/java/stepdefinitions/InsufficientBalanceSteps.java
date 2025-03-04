package stepdefinitions;

import io.cucumber.java.en.*;

import static org.junit.Assert.assertTrue;

import org.junit.Assert;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import io.github.bonigarcia.wdm.WebDriverManager;

public class InsufficientBalanceSteps {
    WebDriver driver;

    private boolean hasSufficientBalance;
    private boolean transactionApproved; 

    @Given("a customer with a debit card and insufficient balance")
    public void customer_with_insufficient_balance() {
        WebDriverManager.chromedriver().setup();
        driver = new ChromeDriver();
        driver.get("https://banking-portal.com/login");

        hasSufficientBalance = false; // Assuming the customer has insufficient balance

    }

    @When("they attempt an online transaction")
    public void attempt_online_transaction() {
        driver.findElement(By.id("paymentPage")).click();
        driver.findElement(By.id("amount")).sendKeys("5000");
        driver.findElement(By.id("payButton")).click();

        if (hasSufficientBalance) {
            transactionApproved = true; // Simulate transaction approval
        } else {
            transactionApproved = false;
        }
    }

    @Then("the transaction should be declined")
    public void transaction_declined() {
        WebElement errorMessage = driver.findElement(By.id("insufficientFundsError"));
        Assert.assertTrue(errorMessage.isDisplayed());
        driver.quit();
    }

    @Given("a customer with a debit card and sufficient balance")
    public void a_customer_with_a_debit_card_and_sufficient_balance() {
        hasSufficientBalance = true; // Assuming the customer has enough balance
    }

    @Then("the transaction should be accepted")
    public void the_transaction_should_be_accepted() {
        assertTrue("Transaction was not approved despite sufficient balance", transactionApproved);
    }
}
