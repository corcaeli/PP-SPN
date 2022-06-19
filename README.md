# PPSPN
Privacy preserving Sum-Product-Networks

## Running on docker
The client and member of out network can be started with docker. 
* Ensure to install [Docker](https://docs.docker.com/get-docker/) at your machine (at Windows we prefer the WSL2 backend).
* For running the network local at your machine create a docker network overlay via 
```
docker network create --driver=overlay --attachable spn_overlay
```

* Use the dockerfiles for manager and member to build docker images 
```
docker build -t manager_build -f dockerfile_manager .
OR
docker build -t member_build  -f dockerfile_member .
```
at Windows you can use the `manager_build.ps1` and `member_build.ps1` for this. 

* After building the images we can run them with 
```
docker run --rm --name manager --network spn_overlay --ip 10.0.1.10 -e CONFIG_FILE_LOCATION="./ressources/config/config.ini" manager_build
OR
docker run --rm --name member$ID --network spn_overlay --ip 10.0.1.1$ID -e CONFIG_FILE_LOCATION="./ressources/config/config.ini" -e ID_OF_MEMBER="$ID" member_build
```
where $ID is the id of the member you want to run. At windows you can use `manager_run.ps1` and `member_run.ps1 [ID]` for this.

* You can close a running docker image with 
```
docker stop manager
OR
docker stop member$ID
```
at Windows you can use the `manager_stop.ps1` and `member_stop.ps1` scripts.

## Reproduce experimental results
The datasets used can be found at https://github.com/arranger1044/DEBD. For bnetflix, baudio, jester and nltcs the used config files can be found at [ressources/config](./ressources/config) the required data are already included in [ressources/input](./ressources/input) for those datasets.

For reproducing the experimental results we recommend to use docker. At Windows you can just:
* change the name of the config you want to run in [ressources/config](./ressources/config) to `config.ini`
* Rebuild docker images with `network_build.ps1` (which just builds manager and member images)
* Run the network with `network_start.ps1 [Amount IDs]` where [Amount IDs] is the amount of members used in the config file (they have to match)
* After running you can see the work beeing done in the window of the Manager, Docker can be used to analyse ressource usage during and after the run
* To close all members and the manager you can use the `network_stop.ps1 [Amount IDs]` script, where [Amount IDs] is the amount of members used in the config file

## Configuration
Its important for the network to run correct, that the IP adress of each member is correct set in the `config.ini`.

### General section
In this section are settings, used by all members and the manager.

| name                  | type      | meaning |
| ---                   | ---       | ---     |
| prim_number           | Integer   | The primnumber used as base for the galois field used for en- and decryption   |
| joint_random_zero_additive_minimum | Integer | The minimal value a share of zero can have as additive share |
| d_multiplyer | Integer | Used to realize a approximated real value division, so it kinda determins the precision of divisions. Precision is roughly log_10(`d_multiplyer`)//2 -1 |
| additive_sharing_over_integer_max_secret | Integer | The greatest allowed value to be encrypt as shares over integer |
| additive_sharing_over_integer_allowed_bit_length_of_secret | Integer | The allowd bit-length of a value to be encrypted as shares over integer |
| additive_sharing_over_integer_security_parameter | Integer | Adds some randomnes or increases range a value is taken randomly from to increase security |
| load_spn_weights      | Boolean   | If set to true, the network loads the weights of the spn from the file specified by `spn_weights_file_path`
| save_spn_weights      | Boolean   | If set to true, the network saves the weights of the spn to the file specified by `spn_weights_file_path`

### ID sections
Each ID section is of pattern `ID_x`, where x should be identical to the id in the section itself.

| name                  | type      | meaning |
| ---                   | ---       | ---     |
| id                    | Integer   | Id of the member/manager this section is about, used for en- and decryption aswell |
| ip4                   | x.x.x.x   | The ip4 adress of this member/manager |
| port                  | Integer   | Port used for the communication with the network |
| name                  | String    | Just the name for this member/manager, not used for calculations and comunications |
| latency               | Integer   | The delay this member/manager has at sending/receiving a message, the values unit is milliseconds (ms) |
| private_evaluation    | Boolean   | If set true, the first x lines of the file specified by `private_data_for_evaluation_file_path` are evaluated. Where x is specified by `private_evaluation_amount_lines_to_evaluate` |
| private_evaluation_amount_lines_to_evaluate | Integer | The amount of line which should be evaluated of the file specified by `private_data_for_evaluation_file_path`. Only invoked when `private_evaluation` is set to True |
| private_data_file_path | String   | The filepath of the private data used for training the weights of the spn. |
| spn_file_path         | String    | The filepath of the spn structure, the format is the equation-format of the SPFlow framework |
| spn_weights_file_path  | String   | The filepath of the weights of the spn. Those should be in polynomial shares and not as clear values |
| private_data_for_evaluation_file_path | String | The filepath of the private input, used for evaluation. Only used if `private_evaluation` is set true. |



## Installing (old)
For running the `main-member.py` or `main-manager.py` you have to install the following python packages:

```
pip install nest-asyncio galois torch scipy tqdm sympy matplotlib networkx lark
```

python should be 3.8.1 or 3.9.x but maybe other versions work too.

## Running (old)
In the folder of the cloned repository you can start the manager by
```
[path to python] ./main-manager.py ./ressources/config/config.ini
```

For a member you have to add the "id" of the member you are (or you just want to start) behind the config file path
```
[path to python] ./main-member.py ./ressources/config/config.ini [id number]
```
