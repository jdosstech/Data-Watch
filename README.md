# Build The Docker Image
docker build . -t simple_server
# Run The Docker Image
docker run -p 8000:8000 simple_server