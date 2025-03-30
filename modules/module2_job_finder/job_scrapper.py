import requests
import json
import pandas as pd
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def get_usajobs(keyword, location, results_per_page=25):
    """
    Fetch job listings from USAJobs API
    """
    # Get credentials from environment variables
    email = os.getenv('USAJOBS_EMAIL')
    api_key = os.getenv('USAJOBS_API_KEY')
    
    # Check if credentials are available
    if not email or not api_key:
        raise ValueError("Missing API credentials. Check your .env file.")
    
    # Your API credentials from developer.usajobs.gov
    headers = {
        'Host': 'data.usajobs.gov',
        'User-Agent': email,
        'Authorization-Key': api_key
    }
    
    # Build the API URL
    base_url = 'https://data.usajobs.gov/api/search'
    params = {
        'Keyword': keyword,
        'LocationName': location,
        'ResultsPerPage': results_per_page
    }
    
    # Make the request
    response = requests.get(base_url, headers=headers, params=params)
    
    # Check if request was successful
    if response.status_code == 200:
        data = response.json()
        jobs = []
        
        # Extract job information
        for job in data.get('SearchResult', {}).get('SearchResultItems', []):
            job_data = job.get('MatchedObjectDescriptor', {})
            
            # Extract job details
            position = job_data.get('PositionTitle', 'No title')
            organization = job_data.get('OrganizationName', 'No organization')
            location_info = job_data.get('PositionLocationDisplay', 'No location')
            
            # Extract job description
            job_description = job_data.get('QualificationSummary', 'No description')
            
            # Extract application URL
            apply_url = job_data.get('ApplyURI', [''])[0] if job_data.get('ApplyURI') else 'No link'
            
            # Extract date posted
            publication_date = job_data.get('PublicationStartDate', 'No date')
            
            # Add to jobs list
            jobs.append({
                'Title': position,
                'Company': organization,
                'Location': location_info,
                'Date Posted': publication_date,
                'Link': apply_url,
                'Description': job_description
            })
        
        # Convert to DataFrame
        jobs_df = pd.DataFrame(jobs)
        return jobs_df
    else:
        print(f"Error: {response.status_code}")
        return pd.DataFrame()

# Example usage
if __name__ == "__main__":
    # Get software engineering jobs in Washington DC
    jobs = get_usajobs("Data Analyst", "Washington DC")
    
    # Save results to CSV
    jobs.to_csv("usajobs_listings.csv", index=False)
    
    # Display first few results
    if not jobs.empty:
        print(jobs[['Title', 'Company', 'Location']].head())
        print(f"Total jobs found: {len(jobs)}")
    else:
        print("No jobs found or API error occurred.")