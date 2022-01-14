
$host.UI.RawUI.WindowTitle = "Stop for 13 member"


$i=1
while($i -lt 14) {
  Set-PSDebug -Trace 0
  Write-Host "Stopping member$i"
  start pwsh (".\member_stop.ps1 $i")
  $i++
}








