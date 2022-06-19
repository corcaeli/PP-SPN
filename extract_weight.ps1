

$datasetname= $args[0]
$ID= $args[1]

docker cp "member${ID}:/ppspn_env/ressources/input/$datasetname/spn_weights_$ID.in" "./extracted_output/$datasetname/"