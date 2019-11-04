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

#### Run ls command

First let us see more info for the system command

    Input :: <= system --help
    usage: remoteCLI remoteCLI [options] / [-h/--help] system [-h] {ls,pwd,cwd}

    positional arguments:
      {ls,pwd,cwd}  System command

    optional arguments:
      -h, --help    show this help message and exit


as we can see, the system command acceps one of `ls`,`cwd`,`pwd`.

If we run `system ls` we will get the content in the diretory that we are running the socket server.

    Input :: <= system ls
    Response for request: system ls
            .git
            README.md
            client_requests.py
            clprime.py
            getargs.py
            prime.py
            __pycache__
            .gitignore
    -


#### Get option completion

Double tab while in the cli to get the available options

    Input :: <= 
    clear   cwd     exit    ls      pwd     quit    system 


#### Add more commands

To add more commands, first edit `getargs.py` and append your new commands under the `set_args_list` method.

Next, edit `client_requests.py` and go at the end, to the part where we run the system commands and add your command

    try:
        for arg in self.args.keys():
            if self.args[arg] == 'ls':
                retdata = {'key': 'dict', 'value': []}
                for e in os.listdir():
                    retdata['value'].append(e)
            elif self.args[arg]  == 'cwd':
                retdata = {'key': 'text', 'value': os.getcwd()}
            elif self.args[arg]  == 'pwd':
                retdata = {'key': 'text', 'value': os.path.dirname(os.getcwd())}

        self.init_client_communication(retdata)


For example, let us say that you added a new optional argument in the `getargs.py` as shown below

    self.parser.add_argument('--dev',
            help="""Removes all kind of checks. Never run this with super user privileges. 
            It exists only for the experimental developing phase.""",
            action="store_true",
            default=False
    )

The `check_args` method in the `getargs.py` will retun this to the socket server: `dev: False` if you do not pass `--dev`
and `dev: True` if you pass `--dev`

We will add a new action for this optional argument that will simply send `Dev mode is on` to the client.

    try:
        for arg in self.args.keys():
            if arg == 'system':
                if self.args[arg] == 'ls':
                    retdata = {'key': 'dict', 'value': []}
                    for e in os.listdir():
                        retdata['value'].append(e)
                elif self.args[arg]  == 'cwd':
                    retdata = {'key': 'text', 'value': os.getcwd()}
                elif self.args[arg]  == 'pwd':
                    retdata = {'key': 'text', 'value': os.path.dirname(os.getcwd())}
            elif arg == 'dev':
                retdata = {'key': 'text', 'value': "Dev mode is on"}

        self.init_client_communication(retdata)

Now restart the server and client: `ctrl_c` on both terminals and start them again.

    ------------ RemoteCLI ------------

            * Socket Client *

    -----------------------------------

    Input :: <= --dev
    Dev mode is on
    Input :: <= 

