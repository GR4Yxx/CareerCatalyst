from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

def get_jobs(keyword, location, num_pages):
    """
    Scrape LinkedIn jobs based on keyword and location
    """
    # Initialize empty list to store job details
    job_list = []
    
    # Loop through the number of pages to scrape
    for page in range(num_pages):
        # Calculate the start parameter for pagination
        start = page * 25
        
        # Construct the URL with filters
        url = f"https://www.linkedin.com/jobs/search/?keywords={keyword}&location={location}&start={start}"
        
        # Send HTTP request
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        
        # Parse the response
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all job cards
        jobs = soup.find_all('div', class_='base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card')
        
        # Loop through each job card
        for job in jobs:
            try:
                # Extract job title
                title = job.find('h3', class_='base-search-card__title').text.strip()
                
                # Extract company name
                company = job.find('h4', class_='base-search-card__subtitle').text.strip()
                
                # Extract job location
                location = job.find('span', class_='job-search-card__location').text.strip()
                
                # Extract job link
                link_element = job.find('a', class_='base-card__full-link')
                link = link_element.get('href') if link_element else 'No link available'
                
                # Extract posted date
                date_posted = job.find('time', class_='job-search-card__listdate').get('datetime') if job.find('time', class_='job-search-card__listdate') else 'No date available'
                
                # Create a dictionary for the job
                job_data = {
                    'Title': title,
                    'Company': company,
                    'Location': location,
                    'Date Posted': date_posted,
                    'Link': link
                }
                
                # Add the job data to our list
                job_list.append(job_data)
                
            except AttributeError:
                # Skip if there's an error extracting data
                continue
        
        # Sleep to avoid being blocked
        time.sleep(2)
    
    # Convert the list to a DataFrame
    jobs_df = pd.DataFrame(job_list)
    return jobs_df

# Example usage:
if __name__ == "__main__":
    # Get jobs for "software engineer" in "United States"
    jobs = get_jobs("software engineer", "United States", 3)
    
    # Save to CSV
    jobs.to_csv("linkedin_jobs.csv", index=False)
    
    # Display first few results
    print(jobs.head())