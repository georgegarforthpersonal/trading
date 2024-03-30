# 1 Setup

How to delpoy Streamlit app to Google Cloud Run

## 1.1 Build the Docker image

The first step is to build the Docker image. This Docker command builds an image
from the Dockerfile in the current directory, targeting the Linux AMD64 platform,
and tags the resulting image with `us-central1-docker.pkg.dev/trading-416814/trading-dashboard/1.0:tag5.`
The tag configures the docker push command to push the image to GCP

```bash
docker build . --platform linux/amd64 -t us-central1-docker.pkg.dev/trading-416814/trading-dashboard/1.0:tag5
```
## 1.2 Run the Docker image locally

We should test that the docker container runs locally before
we push it to GCP. Note that this image won't run locally with the
`--platform linux/amd64` flag. Remove this and rebuild to test locally.

```bash
docker run -p 8080:8080 -t us-central1-docker.pkg.dev/trading-416814/trading-dashboard/1.0:tag4
```

For simple local development just use
```bash
streamlit run /Users/georgegarforth/code/trading/src/target_app.py
```

## 1.3 Push the Docker image to Google Container Registry

We've confirmed our Docker image works. Now we need to push it to our Cloud Artifact repository.
Do that with docker push

```bash
docker push us-central1-docker.pkg.dev/trading-416814/trading-dashboard/1.0:tag5
```

## 1.4 Deploy the Docker image to Cloud Services

- Find Google Cloud Run
- Select “Create Service”
- Select the container image for deployment.
- Check the box that says “Allow unauthenticated invocations” when setting up your service (for public access)
- Go to the URL provided to see your app

# Useful Resources

- https://medium.com/@faizififita1/how-to-deploy-your-streamlit-web-app-to-google-cloud-run-ba776487c5fe
- https://github.com/streamlit/streamlit/issues/4842
- https://cloud.google.com/run/docs/troubleshooting#container-failed-to-start

