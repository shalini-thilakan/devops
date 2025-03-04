package stepdefinitions;

import io.cucumber.java.en.*;
import org.junit.Assert;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import io.github.bonigarcia.wdm.WebDriverManager;

public class PinEntrySteps {
    WebDriver driver;

    @Given("a customer with an active debit card")
    public void customer_with_active_debit_card() {
        WebDriverManager.chromedriver().setup();
        driver = new ChromeDriver();
        driver.get("https://banking-portal.com/login");
    }

    @When("they enter an incorrect PIN three times")
    public void enter_incorrect_pin_three_times() {
        for (int i = 0; i < 3; i++) {
            driver.findElement(By.id("pinEntry")).sendKeys("1234");
            driver.findElement(By.id("submitButton")).click();
        }
    }

    @Then("the card should be temporarily blocked")
    public void card_should_be_blocked() {
        WebElement blockMessage = driver.findElement(By.id("cardBlockedMessage"));
        Assert.assertTrue(blockMessage.isDisplayed());
        driver.quit();
    }
}
