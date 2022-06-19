$AmountMembers= $args[0]
$datasetname= $args[1]

$ID=1
while($ID -lt ($AmountMembers + 1)) {
  start pwsh (".\extract_weight.ps1 $datasetname $ID")
  $ID++
}