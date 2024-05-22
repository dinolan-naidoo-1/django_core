# Django API assessment 

This demo project showcases two endpoints:

1. POST - processFile: This endpoint enables users to upload an Excel file containing transactional data. Upon upload, the data undergoes validation and is subsequently stored in the database.
#
2. GET - retrieveRows: This endpoint permits users to retrieve existing transaction records for the year 2020.
 
#
## Getting Started

- Clone repository to your local machine 


cd into the root folder (e.g: Dockerfile path) and run
```bash
docker build . 
```

Start containers with
```bash
docker compose up 
```
- If you receive an error **ModuleNotFound**. Try `docker compose up --build`


To log in to the admin panel, first create a user:
```bash
python manage.py createsuperuser
```

At this point you can navigate to
`http://localhost:8000/admin` and use the details you just created.
#
## Testing processFile endpoint

- Download the Django_Test_Sheet attached in the email
- Navigate to `http://localhost:8000/app/processFile/`
- Upload the test sheet 
- You should receive a message: 'Successfully uploaded data'
- Navigate to `http://localhost:8000/admin` 
- Confirm that the data was uploaded successfuly
#
## Testing retrieveRow endpoint

1.
- For simplicity, you can use the following:
- `http://localhost:8000/app/retrieveRows/?country=DE&date=2020/02/03` & hit enter
- Confirm that the correct data is returned
#
2.
- The next step is to add a currency (note this uses a mock function)
- `http://localhost:8000/app/retrieveRows/?country=DE&date=2020/02/03?currency=GBP` & hit enter
- You should see the currency, input amount and net amount change
#
3.
- To test a non-existing record use the following (date changed):
- `http://localhost:8000/app/retrieveRows/?country=DE&date=2023/03/03`
- Confirm that you receive `No items found for the specified date and country`
#
4. 
- To test the date validation use the following: 
- `http://localhost:8000/app/retrieveRows/?country=DE&date=2023-03-03`
- Confirm that you receive `Invalid date format. Use YYYY/MM/DD`
#
## Run Tests
- You can use the following to run the test files. Once again I've kept this simple. For future reference, the tests could be run via a cloud run or github action. 
```bash
python manage.py test
```
