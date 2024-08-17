# NFL Schedule API
This API is used to update the NFL lines spreadsheet. I don't think anyone else uses it.

1. Get the schedule from a site and put it into `nfl-schedule-{year}-raw.json`
   - Possible site: https://fftoday.com/nfl/schedule.php
2. Run `load_schedule.py` to convert from the raw format to a CSV
    - Make sure to update `file_name`, `csv_file_name`, and `season` variables to match the year
3. Update `main.py` to handle the next year (there's probably other logic that needs to be included)
   - Update the `max_year` variable
4. Test locally
   - `functions-framework-python.exe --target=get_schedule_http`
5. Deploy the function to the cloud
```bash
gcloud functions deploy nfl_schedule_api \
--runtime=python38 \
--region=us-central1 \
--source=. \
--entry-point=get_schedule_http \
--trigger-http \
--allow-unauthenticated
```

### Notes:
- There may be a way to append the newer schedule to the main CSV.