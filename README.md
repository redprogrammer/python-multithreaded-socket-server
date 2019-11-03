# Python Multithreaded Socket Server

Python multithreaded socket server with remote cli and argparse example.

### Start the server

To start the server issue:

    python3 prime.py

Expected output

    INFO (MainThread) Defining Socket Server
    INFO (MainThread) Address, protocol Family and socket type
    INFO (MainThread) Binding socket 0.0.0.0 55557
    INFO (MainThread) Socket created successfully.
    INFO (MainThread) Socket now listening at 55557

If you want to enable debug mode, start the server with `debug` parameter


    python3 prime.py debug
    
 
### Start the client

The clinet requires the hostname of the server as a parameter

    python3 clprime.py localhost


Expected welcome output


    ------------ RemoteCLI ------------

            * Socket Client *

    -----------------------------------

    Input :: <= 
    

#### View Help

To view help issue:

    Input :: <= --help
 
 
Example output

    ------------ RemoteCLI ------------

            * Socket Client *

    -----------------------------------

    Input :: <= --help
    usage: remoteCLI remoteCLI [options] / [-h/--help]

    ----------------------------------------------------------------------------
    remoteCLI: Remote cli command options.
    ----------------------------------------------------------------------------

    optional arguments:
      -h, --help  Show this help message and exit.

    System Commands:
      {system}

    For more information about each option, please see man remoteCLI.1 This
    program is distributed under GPL-2 license

    Input :: <= 


#### Get option completion

Double tab while in the cli to get the available options

    Input :: <= 
    clear   cwd     exit    ls      pwd     quit    system 

