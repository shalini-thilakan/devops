package stepdefinitions;

import io.cucumber.java.en.*;
import org.junit.Assert;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import io.github.bonigarcia.wdm.WebDriverManager;

public class DebitCardActivationSteps {
    WebDriver driver;

    @Given("a customer with an inactive debit card")
    public void customer_with_inactive_debit_card() {
        WebDriverManager.chromedriver().setup();
        driver = new ChromeDriver();
        driver.get("https://banking-portal.com/login");
        driver.findElement(By.id("username")).sendKeys("testUser");
        driver.findElement(By.id("password")).sendKeys("testPass");
        driver.findElement(By.id("loginButton")).click();
    }

    @When("they activate the card via net banking")
    public void activate_card_net_banking() {
        driver.findElement(By.id("debitCardMenu")).click();
        driver.findElement(By.id("activateCard")).click();
    }

    @Then("the card should be activated successfully")
    public void card_activated_successfully() {
        WebElement successMessage = driver.findElement(By.id("activationSuccess"));
        Assert.assertTrue(successMessage.isDisplayed());
        driver.quit();
    }
}
