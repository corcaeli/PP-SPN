# PPSPN
Privacy preserving Sum-Product-Networks

## Installing
For running the `main-member.py` or `main-manager.py` you have to install the following python packages:

```
pip install nest-asyncio galois torch scipy tqdm sympy matplotlib networkx lark
```

python should be 3.8.1 or 3.9.x but maybe other versions work too.

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

## Running
In the folder of the cloned repository you can start the manager by
```
[path to python] ./main-manager.py ./ressources/config/config.ini
```

For a member you have to add the "id" of the member you are (or you just want to start) behind the config file path
```
[path to python] ./main-member.py ./ressources/config/config.ini [id number]
```