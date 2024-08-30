# PostGIS-REST-API


### GETTING STARTED

1. To run this application you need to have installed docker and docker-compose, 
if you don't have it already, please visit this sites for further instruction:  
    - [docker](https://docs.docker.com/ee/supported-platforms/)  
    - [docker-compose](https://github.com/Yelp/docker-compose/blob/master/docs/install.md)  
2. If you have docker applications installed and you are able to use [make](https://www.gnu.org/software/make/) type this commands to build docker container:  
`make run`  
or  
`docker-compose build && docker-compose up`
3. At this point you should be able to access project at [localhost](http://localhost:8000)
4. To run tests type:  
```make test```  
or  
```docker-compose exec web bash -c "python manage.py test"```
### API
Available endpoints: 
```
api/ points/ [name='point-list-create']
api/ point/<int:pk>/ [name='point-detail']
api/ linestrings/ [name='linestring-list-create']
api/ linestring/<int:pk>/ [name='linestring-detail']
api/ polygons/ [name='polygon-list-create']
api/ polygon/<int:pk>/ [name='polygon-detail']
api/ polygon/<int:pk>/intersection [name='polygon-intersection']
api/ join_lines/ [name='join-lines']
swagger<format>/ [name='schema-json']
swagger/ [name='schema-swagger-ui']
```
[swagger documentation](http://localhost:8000/swagger)

Normally secrets would be hidden in .env file, however here are passed in docker-compose `environment` 
to simplify process of building this project
