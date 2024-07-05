
import pandas as pd
import aioboto3
import json
from app.core.config import settings

def validate_and_clean_csv(file_path):
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)

        # Ensure there is at least one record after removing rows with empty 'keyword'
        if df.empty:
            raise ValueError("CSV file must contain at least one valid record.")

        # Ensure the columns are exactly {keyword, search_engine, country, location}
        required_columns = ['keyword', 'search_engine', 'device', 'country', 'location']
        if list(df.columns) != required_columns:
            raise ValueError(f"CSV columns do not match required columns: {required_columns}")

        # Remove rows where 'keyword' is empty
        df = df.dropna(subset=['keyword'])

        # Fill empty 'search_engine' and 'device' with 'google' and 'desktop'
        df.fillna({'search_engine': 'google'}, inplace=True)
        df.fillna({'device': 'desktop'}, inplace=True)

        # Ensure 'search_engine' is one of 'google', 'bing', 'yahoo'; replace invalid values with 'google'
        valid_search_engines = ['google', 'bing', 'yahoo']
        df['search_engine'] = df['search_engine'].apply(lambda x: x if x in valid_search_engines else 'google')

        # Ensure 'device' is either 'desktop' or 'mobile'; replace invalid values with 'desktop'
        valid_devices = ['desktop', 'mobile']
        df['device'] = df['device'].apply(lambda x: x if x in valid_devices else 'desktop')

        # # You can add more sophisticated keyword validation logic here if needed
        # def is_valid_seo_keyword(keyword):
        #     # Placeholder for actual validation logic
        #     return True

        # # Filter out rows with invalid SEO keywords
        # df = df[df['keyword'].apply(is_valid_seo_keyword)]

        # Convert the cleaned dataframe to a JSON string
        # cleaned_data_json = df.to_json(orient='records')

        # # Save the JSON string to a file
        # keyword_file_name = gen_keyword_file_name(landscape_id)
        # output_file_path = 'storage/' + keyword_file_name
        # with open(output_file_path, 'w') as json_file:
        #     json_file.write(cleaned_data_json)
        return df[['keyword', 'search_engine', 'device', 'country']]
    except Exception as e:
        raise ValueError(f"Failed to validate and clean CSV file: {e}")    


# A function that will take the dataframe and divide into chunks of 1000
def divide_chunks(ids_list, n):
    # looping till length l
    for i in range(0, len(ids_list), n):
        yield ids_list[i:i + n]

async def save_file_s3(keyword_file_name):
    session = aioboto3.Session()
    try:
        async with session.client('s3') as s3_client:
            await s3_client.upload_file('storage/'+ keyword_file_name, settings.AWS_BUCKET_NAME, keyword_file_name)
    except Exception as e:
        raise ValueError(f"Failed to save file to S3: {e}")

def gen_keyword_file_name(landscape_id):
    return f'keywords_{landscape_id}.json'