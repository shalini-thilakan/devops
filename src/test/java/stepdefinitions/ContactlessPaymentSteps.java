package stepdefinitions;

import io.cucumber.java.en.*;
import org.junit.Assert;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import io.github.bonigarcia.wdm.WebDriverManager;

public class ContactlessPaymentSteps {
    WebDriver driver;

    @Given("a customer with a debit card enabled for contactless payments")
    public void customer_with_contactless_payments() {
        WebDriverManager.chromedriver().setup();
        driver = new ChromeDriver();
        driver.get("https://banking-portal.com/login");
    }

    @When("they make a transaction below the limit")
    public void transaction_below_limit() {
        driver.findElement(By.id("contactlessPayment")).click();
        driver.findElement(By.id("amount")).sendKeys("1500");
        driver.findElement(By.id("payButton")).click();
    }

    @Then("the transaction should be approved without a PIN")
    public void transaction_approved_without_pin() {
        WebElement successMessage = driver.findElement(By.id("transactionSuccess"));
        Assert.assertTrue(successMessage.isDisplayed());
        driver.quit();
    }
}
