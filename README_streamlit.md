# 1 Setup

## 1.1 Build the Docker image

Build your Docker image with docker build as shown below. Run this command from your project's root directory.
The tag configures the docker push command to push the image to a specific location. It can be broken down as follows:

```docker build . -t tag1```


```bash
docker build . -t us-central1-docker.pkg.dev/trading-416814/trading-dashboard/1.0:tag3
```
## 1.2 Run the Docker image locally

Run the image using docker run in interactive mode (-i).

```docker run -p 8501:8501 tag1```

```bash
docker run -p 8080:8080 -t us-central1-docker.pkg.dev/trading-416814/trading-dashboard/1.0:tag3
```

## 1.3 Push the Docker image to Google Container Registry

We've confirmed our Docker image works. Now we need to push it to our Cloud Artifact repository. Do that with docker push

```bash
docker push us-central1-docker.pkg.dev/trading-416814/trading-dashboard/1.0:tag3
```

## 1.4 Deploy the Docker image to Cloud Services

In the Navigation Menu of your Google Cloud page find Google Cloud Run. Select “Create Service”. Google Cloud Run should automatically recognize the container you uploaded so you can select it for deployment.
Make sure to check the box that says “Allow unauthenticated invocations” when setting up your service. This allows the public to access your url.
Once you configured your service to your preferences you can then click “Create” in order to deploy.
Depending on the size of your project it may take a while. When the deployment process is finished you will be provided a public url to view and share your Web App!

# Useful Resources

- https://medium.com/@faizififita1/how-to-deploy-your-streamlit-web-app-to-google-cloud-run-ba776487c5fe
- https://github.com/streamlit/streamlit/issues/4842
- https://cloud.google.com/run/docs/troubleshooting#container-failed-to-start


# What currently works

## Containerising something

```bash
docker build . -t tag1
```

```bash
docker run -p 8501:8501 tag1
```

Then go to http://localhost:8501/ (not what's printed in terminal)

## Running the app that I want (without docker)

```bash
streamlit run /Users/georgegarforth/code/trading/src/target_app.py
```