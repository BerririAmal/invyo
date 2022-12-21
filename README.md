# Test
This repository contains a script, a notebook, a dockerfile, and other dependencies to perform the task provided in the test statement.

To execute:
- [test20221221.ipynb](https://github.com/berririAm/invyo/blob/master/test20221221.ipynb) allows to browse the povided dependencies and return a file named "askedFile.csv" by specifing an address on line [21](https://github.com/berririAm/invyo/blob/master/test20221221.ipynb#L21).
- [test.py](https://github.com/berririAm/invyo/blob/master/test.py) represents a script encapsulated in a REST API using Flask; the REST API allows to send a warehouse address using the IP address and port provided by the API and return a file named "askedFile.csv".
    ```sh
    $ python test.py
    ```
- To run the docker, use the following command and open in a Web Browser the IP Address of the docker with a warehouse address:
    ```sh
    $ sudo docker run -p 50001:50001 -v $(pwd):/app testinvyo
    ```