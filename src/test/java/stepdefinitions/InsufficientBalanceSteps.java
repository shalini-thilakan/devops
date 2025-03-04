package stepdefinitions;

import io.cucumber.java.en.*;
import org.junit.Assert;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import io.github.bonigarcia.wdm.WebDriverManager;

public class InsufficientBalanceSteps {
    WebDriver driver;

    @Given("a customer with a debit card and insufficient balance")
    public void customer_with_insufficient_balance() {
        WebDriverManager.chromedriver().setup();
        driver = new ChromeDriver();
        driver.get("https://banking-portal.com/login");
    }

    @When("they attempt an online transaction")
    public void attempt_online_transaction() {
        driver.findElement(By.id("paymentPage")).click();
        driver.findElement(By.id("amount")).sendKeys("5000");
        driver.findElement(By.id("payButton")).click();
    }

    @Then("the transaction should be declined")
    public void transaction_declined() {
        WebElement errorMessage = driver.findElement(By.id("insufficientFundsError"));
        Assert.assertTrue(errorMessage.isDisplayed());
        driver.quit();
    }
}
