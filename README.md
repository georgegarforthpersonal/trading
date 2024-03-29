# 1 Setup

## 1.1 Build the Docker image

Build your Docker image with docker build as shown below. Run this command from your project's root directory.
The tag configures the docker push command to push the image to a specific location. It can be broken down as follows:

```bash
docker image build \
--platform linux/amd64 \
--tag us-central1-docker.pkg.dev/trading-416814/trading/1.0:tag2 \
.
```

## 1.2 Run the Docker image locally

Run the image using docker run in interactive mode (-i).

```bash
docker run --rm -it \
us-central1-docker.pkg.dev/trading-416814/trading/1.0:tag2
```

## 1.3 Push the Docker image to Google Container Registry

We've confirmed our Docker image works. Now we need to push it to our Cloud Artifact repository. Do that with docker push

```bash
docker push \
us-central1-docker.pkg.dev/trading-416814/trading/1.0:tag2
```

## 1.4 Deploy the Docker image to Cloud Run

Now we have our image in the repository. We can deploy it to Cloud Run.

- Go th the Cloud Run dashboard
- Click on the JOBS tab
- Click CREATE JOB
- Select the image we just uploaded to Artifact Registry
- Fill out the remaining fields as you see fit, or leave the defaults in place
- Check the box that says Execute job immediately

# Useful Resources

- https://www.practiceprobs.com/blog/2022/12/15/how-to-schedule-a-python-script-with-docker-and-google-cloud/#__tabbed_1_1