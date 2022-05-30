# django-aws-eb-cookie-cutter
A template for deploying a python Django application to AWS Elastic Beanstalk.

# Directions

1. The virtual environment for this application is called eb_virt. The project name is mysite and the app name is main. Activate the virtual environment by typing the below in the command line:

`source eb-virt/bin/activate`

Then cd to the project directory and install the dependencies in the requirements.txt. Note that this project requires python 3.8. If your project requires any other libraries, add them to the requirements.txt before pip installing.

`cd mysite`
`pip install -r requirements.txt`

This template uses the default sqlite3 database. If this is deployed with Django > 2.1 to AWS EB, then following error may occur:

`deterministic=True requires SQLite 3.8.3 or higher`
 

This seems to be an issue I’ve only experienced with AWS EB, and the easiest way to bypass this is to use Django 2.1. 

2. Once all packages are successfully installed, add a file called config.json to the second level mysite directory (same level as settings.py). Within this file, add the following json:

`{
    "SECRET_KEY": “<a random string that you decide>”,
    "DEBUG": 1,
    "ALLOWED_HOSTS": ["127.0.0.1", ""]
}`
 

Whilst in development, keep DEBUG to 1. Once deployed, this should be changed to 0. We will come back to what should be populated within the ALLOWED_HOSTS.

If you have decided to rename your project to something other than mysite, then the snippet below that is found in .ebextensions > django.config should also be updated:

`option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: <your_name>.wsgi:application`
    
3. If you have not installed the EB CLI, follow the instructions in the AWS GitHub repo.

Then run the following commands in the mysite directory level (same level as the .ebextensions folder is located). Note that this has been pulled from the AWS documentation.

`eb init -p python-3.8 django-tutorial`

`## Replace django-tutorial with whatever you want your EB application to be called.`

`eb create django-env`

`## Replace django-env with whatever you want your EB environment to be called.`

4. Navigate to the AWS Elastic Beanstalk terminal in the web browser. You should see your environment created once the command has finished running, with a url to the right hand side.

Click on the url and you should be directed to a django debug page, stating that the url should be added to ALLOWED_HOSTS. Go back to your config.json file and add this url into the ALLOWED_HOSTS list, surrounded by quotation marks.

In the command line again, type `eb deploy` to redeploy the application with the correctly configured allowed hosts.

5. Click on the url again within the AWS terminal (or type eb open in the command line) and you should be redirected to a correctly loaded page.

It is worth noting now that this project uses scss files as the static stylesheets.

style.scss imports the other scss files, and is then converted to a single style.css file by a Visual Studio Code extension called Live Sass Compiler (there are various IDE extensions that do the same). You will see in header.html that style.css is imported as the style sheet.

When you want to make changes to the design, either continue using scss styling that are compiled by the Live Sass Compiler or just ensure that the css style sheets are contained within static/main/css/ and correctly referenced by the html files.

6. We are now going to configure the website so it uses a custom domain name. AWS has a Domain Name System called Route 53 which I purchased my domain name through. You can transfer existing domain names to Route 53, but you have to have owned the domain name for at least 60 days.

Once you have registered/transferred a domain to Route 53, create a hosted zone from it.

Select your hosted zone and create a record. Change the slider to ‘Alias’ and select an Elastic Beanstalk environment alias, then choose the AWS region associated with your EB environment. Finally, select the environment itself that you created in the previous step.

Select ‘Add another record’ and then repeat these steps but add ‘www’ to the subdomain box at the top. The select create records.

In your config.json file, add these 2 domain names in the ALLOWED_HOSTS list. Redeploy the application by typing ‘eb deploy’ in the command line.

Typing this domain name in your browser should now direct you to your django application. It may take a few minutes to register.

7. You may have noticed that in your browser the application uses the HTTP protocol (port 80) for incoming traffic by default. In this step we will allow HTTPS traffic and also redirect HTTP to HTTPS by default.

Firstly, you need to register for a SSL certificate - and AWS has (another) service for that! Navigate to the AWS Certificate Manager and then select ‘Request’ -> ‘Request a public certificate’.

Then enter your domain name in the box at the top. You can also request certificates for additional formats such as

* `www.<domain_name>.com`
* `*.<domain_name>.com`
* etc.

Choose DNS validation and click ‘Request’. Navigate back to your certificates and you should see a new entry with a status of ‘Pending Validation’. Select this record, and then choose ‘Create records in Route 53’ (assuming you have followed the steps above and your domain is registered in Route 53). Create the records and your certificate should be validated.

Head back to Elastic Beanstalk and select your environment. Select ’Configuration’ on the left hand side and find the ‘Load Balancer’ section.

Click the edit button and then add a listener. Configure the listener as per below, but choose the SSL certificate that you have just created.

* Listener Port 443
* Listener Protocol HTTPS
* Instance Port 80
* Instance Protocol HTTP

Once you have added and applied, your application should allow HTTPS connections. You can test this by typing the below into your browser:

`https://www.<your_domain>.com`

or

`https://<your_domain>.com`

However, you will notice that if you just type your domain into the browser, it will not auto-redirect to HTTPS. To fix this, go into the settings.py of your project and uncomment out the section of code in lines 82 to 95.

This is the code that allows HHTPS auto-redirect, but it only executes when the project is in production (i.e. DEBUG == False/0). Change DEBUG to 0 in your config.json file to change to production mode. Then redeploy by running ‘eb deploy’ in the command line.

Note: the reason we only want this code to run in production is because the devlopement server (localhost) does not support HTTPS. i.e. there is nowhere to redirect to in development mode. 

Once redeployed, type your domain name into the browser and you should be directed to your website, with a HTTPS connection. I recommend clearing your browser history/cache to test and ensure that the application is actually redirecting and isn’t just remembering from when you manually typed in ‘https’.

8. You now have a django application in production. There is a simple model configured in this template that allows a photo and mock ‘post’ to be created in the admin page. Create a super user by typing the below in the command line and then following the instructions. 

`python manage.py createsuperuser`
 

Create a post by switching your mode back to development (setting DEBUG to 1 in django.config) and then running python manage.py runserver. Navigate to the admin page by going to http://127.0.0.1:8000/admin/ in your browser and clicking ‘Add’ next to Project.

The model is configured with ckeditor so there is a rich text uploading field. You can display images in this field, by selecting the image icon in the ‘Project Content’ field and then choosing an image to upload. There is a slight issue here whereby the image appears as a red error box and doesn’t appear in the editor box itself, but it should upload okay within the actual web page.

Any images you upload in the rich text uploading field should be automatically saved to:

`mysite/static/main/img/article_content_photos`
 

Any images uploaded using the button in the ‘Project Image’ field at the bottom are displayed as the display image for the post. They should be automatically saved to:

`mysite/static/main/img/article_photos`
 

Check that the post has been uploaded in development server. Then change your DEBUG mode back to 0, and type ‘eb deploy’ in the command line. Confirm that it has been uploaded in production.

Any time you upload something, push the changes to GitHub so there is a record of the source code. 
