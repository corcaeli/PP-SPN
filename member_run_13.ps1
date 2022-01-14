
$host.UI.RawUI.WindowTitle = "Run up for 13 member"

$i=1
while($i -lt 14) {
  Set-PSDebug -Trace 0
  Write-Host "Starting run script for member $i"
  start pwsh (".\member_run.ps1 $i")
  $i++
}








