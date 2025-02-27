package stepdefinitions;

import io.cucumber.java.en.*;
import org.junit.Assert;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;

import io.github.bonigarcia.wdm.WebDriverManager;

public class GoogleSearchSteps {
    WebDriver driver;

    @Given("the user is on the Google homepage")
    public void the_user_is_on_the_google_homepage() {
        //System.setProperty("webdriver.chrome.driver", "/Users/shalini/Documents/chromedriver"); // Change path accordingly
        WebDriverManager.chromedriver().setup();

        ChromeOptions options = new ChromeOptions();
        options.addArguments("--headless"); // Run Chrome in headless mode
        options.addArguments("--disable-gpu");

        // launching chrome driver
        driver = new ChromeDriver(options);
        driver.get("https://www.google.com");
    }

    @When("the user searches for {string}")
    public void the_user_searches_for(String keyword) {
        WebElement searchBox = driver.findElement(By.name("q"));
        searchBox.sendKeys(keyword);
        searchBox.submit();
    }

    @Then("search results should contain {string}")
    public void search_results_should_contain(String keyword) {
        String pageSource = driver.getPageSource();
        Assert.assertTrue("Search results contain the keyword!", pageSource.contains(keyword));
        driver.quit();
    }

    @Then("no search results should be displayed")
    public void no_search_results_should_be_displayed() {
        boolean noResultsMessageDisplayed = driver.findElements(By.xpath("//*[contains(text(), 'did not match any documents')]")).size() > 0;
        Assert.assertTrue("Search results were found when none were expected!", noResultsMessageDisplayed);
        driver.quit();
    }
    
}
