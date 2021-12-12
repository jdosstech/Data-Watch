# Data Watch

Data Watch is a desktop application for monitoring cryptocurrencies and the stock market.

## Build and Run the Desktop Application

To build the frontend for Data Watch, first clone the repository:

> git clone https://github.com/jdosstech/Data-Watch

Next, install the dependencies:

> cd frontend  
> yarn install

Finally, to build and run Data Watch, run the command:

> yarn start

## Build and Run the Docker Image

To build the Docker image, run the following command (this example uses the name `simple_server`, but you can name it whatever you want):

> docker build . -t simple_server

To run the container, use the command:

> docker run -p 8000:8000 simple_server

To run it in the background, add the `-d` flag:

> docker run -d -p 8000:8000 simple_server
