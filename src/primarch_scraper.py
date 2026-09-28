import json
import time
import argparse
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from send2trash import send2trash
import logging

def setup_logging():
    '''Configures logging for Selenium-related errors.'''
    logging.basicConfig(
        filename='selenium_error.log',
        level=logging.ERROR,
        format='%(asctime)s:%(levelname)s:%(message)s'
    )

class WebScraper:
    '''global class for web scraping operations'''  
    def __init__(self, headless=True, browser_type="firefox"):
        self.headless = headless
        self.browser_type = browser_type
        self.driver = self.setup_driver()
    
    def setup_driver(self):
        '''Configuring and returning a selenium webdriver'''
        if self.browser_type.lower() == "firefox":
            options = Options()
            if self.headless:
                options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            return webdriver.Firefox(options=options)
        else:
            raise ValueError(f"Unsupported browser type: {self.browser_type}")
    
    def fetch_page_source(self, url, wait_time=5):
        '''Fetches page source HTML from a URL after waiting for page load.'''
        try:
            self.driver.get(url)
            time.sleep(wait_time) # Let the page load
            return self.driver.page_source
        except ConnectionRefusedError:
            logging.exception("Connection refused error")
            raise
        except TimeoutError:
            logging.exception("Timeout error")
            raise
    
    def extract_cell_text(self, cells, index):
        '''Extracts and returns text or link text from a specific cell index.'''
        if len(cells) > index:
            link = cells[index].find('a')
            return link.text.strip() if link else cells[index].text.strip()
        return "Unknown"
    
    def close(self):
        '''Closes the Selenium driver if open.'''
        if self.driver:
            self.driver.quit()


class PrimarchScraper(WebScraper):
    '''Special class for scraping Primarch data from Warhammer 40K wiki'''
    def find_primarch_table(self, soup):
        tables = soup.find_all('table')
        for table in tables:
            if table.find_all('tr') and (
                'Legion' in table.text or 
                'Primarch' in table.text or
                'Alpha Legion' in table.text
            ):
                return table
        return None
    
    def extract_primarch_data(self, table):
        '''Parses the Primarch table and returns extracted data as a list of dicts.'''
        primarch_data = []
        for row in table.find_all('tr')[1:]:
            cells = row.find_all('td')
            if len(cells) >= 3:
                primarch_info = {
                    "legion_number": cells[0].text.strip() if len(cells) > 0 else "Unknown",
                    "primarch": self.extract_cell_text(cells, 1),
                    "legion_name": self.extract_cell_text(cells, 2),
                    "world_of_rediscovery": self.extract_cell_text(cells, 3)
                }
                primarch_data.append(primarch_info)
        return primarch_data
    
    def scrape(self, url):
        '''Main scraping function to extract Primarch data from the given URL.'''
        print(f"Fetching data from {url}")
        page_source = self.fetch_page_source(url, wait_time=5)
        soup = BeautifulSoup(page_source, 'html.parser')
        
        primarch_table = self.find_primarch_table(soup)
        if not primarch_table:
            print("Could not find a table with Primarch data.")
            return None   
        return self.extract_primarch_data(primarch_table)


def save_to_json(data, filename='primarch_data.json'):
    ''' If file exists, moving it to trash before overwriting '''
    if os.path.exists(filename):
        send2trash(filename)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to {filename}")


def parse_arguments():
    '''Parsing command-line arguments for scraper configuration.'''
    parser = argparse.ArgumentParser(description='Scrape Primarch data from Warhammer 40K wiki')
    parser.add_argument('--no-headless', action='store_true',
                        help='Run browser in visible mode (not headless)')
    parser.add_argument('--output', type=str, default='primarch_data.json',
                        help='Output JSON file name (default: primarch_data.json)')
    parser.add_argument('--browser', type=str, default='firefox',
                        help='Browser type (default: firefox)')
    return parser.parse_args()


def main():
    '''Main control function for the Primarch scraping program.'''
    setup_logging()
    args = parse_arguments()
    url = "https://warhammer40k.fandom.com/wiki/Primarch"  
    scraper = None
    try:
        # Create scraper instance - showing how to use the specialized class
        scraper = PrimarchScraper(headless=not args.no_headless, browser_type=args.browser)
        primarch_data = scraper.scrape(url)
        if primarch_data:
            save_to_json(primarch_data, filename=args.output)
            print(f"Successfully scraped data for {len(primarch_data)} Primarchs.")        
    except ConnectionRefusedError:
        print("Connection refused. Please check your internet connection.")
    except TimeoutError:
        print("Request timed out. Please try again later.")
    except ValueError as e:
        print(f"Configuration error: {e}")
    except Exception:
        print("An error occurred. For more information, check the log file.")
        logging.exception("Unhandled exception occurred:")
    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")
    finally:
        if scraper:
            scraper.close()


if __name__ == "__main__":
    main()